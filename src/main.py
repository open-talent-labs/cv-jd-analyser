"""
cv-jd-analyser 应用入口。

启动方式（开发）：
    uvicorn src.main:app --reload

启动方式（Docker）：
    docker-compose up
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理：启动时检查依赖服务。"""
    logger.info("=" * 50)
    logger.info("cv-jd-analyser 启动中...")
    logger.info("API 文档: http://localhost:8000/docs")
    logger.info("=" * 50)
    yield
    logger.info("应用已关闭")


app = FastAPI(
    title="cv-jd-analyser",
    description="AI 赋能的简历与职位描述深度匹配分析引擎",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS 配置，允许前端开发时跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router)
