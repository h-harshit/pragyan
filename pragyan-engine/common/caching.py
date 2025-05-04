class CacheManager:
    def __init__(self, conn):
        self.conn = conn

    def get(self, key):
        value = self.conn.get(key)
        return value if value else None

    def set(self, key, value, ttl=None):
        self.conn.set(key, value, ex=ttl)

    def invalidate(self, key):
        self.conn.delete(key)
