"""
Redis 缓存层。

提供统一的缓存接口，用于：
  - 缓存分析结果，避免重复调用 LLM
  - 缓存 Embedding 向量，加速匹配
  - 存储任务状态

通过环境变量 REDIS_URL 配置连接地址。
"""
import os
import json
import logging
import redis

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

try:
    redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    logger.info("Redis 连接成功: %s", REDIS_URL)
except redis.ConnectionError:
    logger.warning("Redis 不可用，缓存功能将降级（返回 None）")
    redis_client = None


class Cache:
    """轻量级缓存封装，调用方无需关心 Redis 连接细节。"""

    @staticmethod
    def get(key: str):
        """获取缓存值（JSON 反序列化）。"""
        if redis_client is None:
            return None
        try:
            val = redis_client.get(key)
            return json.loads(val) if val else None
        except Exception as e:
            logger.warning("缓存读取失败: %s", e)
            return None

    @staticmethod
    def set(key: str, value, ttl: int = 3600) -> bool:
        """设置缓存值（JSON 序列化），默认 1 小时过期。"""
        if redis_client is None:
            return False
        try:
            redis_client.setex(key, ttl, json.dumps(value, ensure_ascii=False))
            return True
        except Exception as e:
            logger.warning("缓存写入失败: %s", e)
            return False

    @staticmethod
    def delete(key: str) -> bool:
        """删除缓存。"""
        if redis_client is None:
            return False
        try:
            redis_client.delete(key)
            return True
        except Exception as e:
            logger.warning("缓存删除失败: %s", e)
            return False

    @staticmethod
    def exists(key: str) -> bool:
        """检查 key 是否存在。"""
        if redis_client is None:
            return False
        try:
            return bool(redis_client.exists(key))
        except Exception:
            return False


cache = Cache()
