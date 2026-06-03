import os
from celery import Celery

# 从环境变量读取 Redis 配置，开发环境默认指向 docker-compose 中的 redis 服务
BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(
    "cv_jd_analyser",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
)

celery_app.conf.update(
    # 任务序列化
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    # 时区
    timezone="Asia/Taipei",
    enable_utc=True,
    # 任务追踪
    task_track_started=True,
    task_ignore_result=False,
    # 可靠性：任务完成后才确认，防止 worker 崩溃时丢任务
    task_acks_late=True,
    # 每个 worker 一次只拿一个任务，避免大任务阻塞其他任务
    worker_prefetch_multiplier=1,
    # 任务软超时（秒），超时后 worker 会收到 SoftTimeLimitExceeded
    task_soft_time_limit=300,
    # 任务硬超时（秒），超时后直接终止
    task_time_limit=600,
    # 结果过期时间（秒）
    result_expires=86400,
)

# 自动发现注册的任务模块
celery_app.autodiscover_tasks(["src.core"])
