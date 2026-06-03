"""
Celery Worker 启动入口。

生产环境启动方式：
    celery -A src.celery_app worker --loglevel=info --concurrency=2

开发调试时可在此文件下直接运行：
    python src/worker.py
"""
import sys
from src.celery_app import celery_app

if __name__ == "__main__":
    argv = [
        "worker",
        "--loglevel=info",
        "--concurrency=2",
    ]
    celery_app.worker_main(argv)
