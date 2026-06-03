# cv-jd-analyser

AI 赋能的简历与职位描述深度匹配分析引擎。

## 项目结构

```
cv-jd-analyser/
├── .github/workflows/   # CI/CD 自动化流水线
├── docker-compose.yml   # Docker 编排（API + Worker + Redis）
├── Dockerfile           # 容器镜像
├── src/
│   ├── main.py          # FastAPI 应用入口
│   ├── worker.py        # Celery Worker 入口
│   ├── celery_app.py    # Celery 应用配置
│   ├── api/             # API 路由层
│   │   └── routes.py    #   - POST /analyze  /result/{id}  /health
│   ├── core/            # 核心业务逻辑
│   │   ├── tasks.py     #   Celery 异步任务定义
│   │   ├── cache.py     #   Redis 缓存封装
│   │   └── matcher.py   #   匹配逻辑（待实现）
│   └── utils/           # 工具函数
│       └── parser.py    #   简历解析（待实现）
├── tests/               # 单元测试
├── scripts/             # 脚本工具
├── requirements.txt     # 依赖管理
└── .env.example         # 环境变量模板
```

## 架构设计

```
HTTP 请求 -> FastAPI (API) -> Celery Task -> Redis Broker
                                            -> Worker 消费任务
                                                 -> PDF 解析
                                                 -> Embedding 匹配
                                                 -> LLM Agent 分析
                                                 -> 结果写入 Redis
用户轮询 <- task_id <- 立即返回
```

## 快速开始

### Docker 方式（推荐）

```bash
# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 OPENAI_API_KEY

# 一键启动所有服务（API + Worker + Redis）
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

### 本地开发方式

```bash
# 需要先启动 Redis（本地或 Docker）
docker run -d -p 6379:6379 redis:7-alpine

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，将 REDIS_URL 改为 redis://localhost:6379/0

# 终端 1：启动 API 服务
uvicorn src.main:app --reload

# 终端 2：启动 Worker
celery -A src.celery_app worker --loglevel=info --concurrency=2
```

## API 文档

启动后访问 http://localhost:8000/docs 查看 Swagger 交互式文档。

| 方法 | 路径 | 说明 |
|------|------|------|
| GET  | /health | 服务健康检查 |
| GET  | /health/worker | Worker 连通性检查 |
| POST | /analyze | 提交简历 + JD 进行匹配分析（异步） |
| GET  | /result/{task_id} | 轮询获取分析结果 |

使用示例：

```bash
# 提交分析
curl -X POST http://localhost:8000/analyze \
  -F "jd_text=职位描述内容..." \
  -F "resume=@/path/to/简历.pdf"

# 返回 {"task_id": "xxx", "status": "pending"}

# 轮询结果
curl http://localhost:8000/result/xxx
# 返回 {"status": "completed", "result": {...}}
```

## 功能特性

- PDF 简历解析与结构化信息抽取
- 简历与 JD 语义匹配评分
- 多 Agent 深度分析（HR 视角 / Tech Lead 视角 / Career Coach 视角）
- 支持本地 LLM 推理加速（vLLM / TensorRT-LLM）
- 异步任务队列，支持横向扩展 Worker
- Redis 缓存，减少重复 LLM 调用
- Docker 容器化一键部署
- CI/CD 自动化测试与代码规范检查
