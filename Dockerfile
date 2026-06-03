FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖（部分 Python 包需要编译）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 先拷贝依赖文件，利用 Docker 层缓存加速构建
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝项目源码
COPY . .

EXPOSE 8000

# 默认启动 API 服务（docker-compose 中 worker 会覆盖 CMD）
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
