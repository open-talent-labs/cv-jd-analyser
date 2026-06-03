"""
API 路由定义。

职责：
  - POST /analyze       提交简历 + JD 进行分析（异步任务）
  - GET  /result/{id}   查询分析结果
  - GET  /health        服务健康检查
"""
import logging
import hashlib
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from src.core.tasks import analyze_resume_jd, health_check

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health")
async def health():
    """健康检查：验证 API 服务状态。"""
    return {
        "status": "ok",
        "service": "cv-jd-analyser",
    }


@router.post("/analyze", summary="提交简历与 JD 进行匹配分析")
async def analyze(
    jd_text: str = Form(..., description="职位描述文本"),
    resume: UploadFile = File(..., description="简历 PDF 文件"),
):
    """
    异步分析简历与 JD 的匹配度。

    流程：
      1. 接收简历 PDF 和 JD 文本
      2. 提交到 Celery Worker 后台处理
      3. 立即返回 task_id，前端轮询结果

    使用方式（curl）：
        curl -X POST http://localhost:8000/analyze \\
          -F "jd_text=职位描述内容" \\
          -F "resume=@/path/to/resume.pdf"
    """
    # 读取上传的简历文件
    resume_content = await resume.read()

    # 生成文件哈希作为去重标识
    file_hash = hashlib.md5(resume_content).hexdigest()

    # 异步提交任务给 Celery Worker
    task = analyze_resume_jd.delay(
        resume_content=resume_content.decode("utf-8", errors="ignore"),
        jd_text=jd_text,
    )

    logger.info(
        "分析任务已提交: task_id=%s, file=%s, hash=%s",
        task.id, resume.filename, file_hash,
    )

    return {
        "task_id": task.id,
        "status": "pending",
        "message": "分析任务已提交，请通过 GET /result/{task_id} 查询结果",
    }


@router.get("/result/{task_id}", summary="获取分析结果")
async def get_result(task_id: str):
    """
    根据 task_id 轮询获取异步分析结果。

    返回状态：
      - pending:   任务排队中或正在处理
      - completed: 分析完成，返回完整结果
      - failed:    分析失败，返回错误信息
    """
    task = analyze_resume_jd.AsyncResult(task_id)

    if task.state == "PENDING":
        return {"status": "pending", "message": "任务排队中，请稍后查询"}
    elif task.state == "STARTED":
        return {"status": "processing", "message": "分析进行中，请稍候"}
    elif task.state == "SUCCESS":
        return {"status": "completed", "result": task.result}
    elif task.state == "FAILURE":
        return {
            "status": "failed",
            "error": str(task.info) if task.info else "未知错误",
        }
    else:
        return {"status": task.state.lower(), "message": str(task.info)}


@router.get("/health/worker", summary="检测 Worker 状态")
async def health_worker():
    """向 Celery Worker 发送一个健康检查任务。"""
    task = health_check.delay()
    return {
        "task_id": task.id,
        "status": "sent",
        "message": "健康检查已发送，请稍后查询结果",
    }
