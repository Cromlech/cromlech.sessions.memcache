# -*- coding: utf-8 -*-

from cromlech.session import SessionHandler
from cromlech.marshallers import PickleMarshaller


class MemcacheSessionHandler(SessionHandler):
    """Memcached based HTTP session.
    """

    def __init__(self, memcache, delta, prefix='session:',
                 marshaller=PickleMarshaller):
        self.delta = delta  # timedelta in seconds.
        self.memcache = memcache
        self.marshaller = marshaller
        self.prefix = prefix

    def get(self, sid):
        key = self.prefix + sid
        data = self.memcache.get(key)
        if data is None:
            return self.new()
        if self.memcache.deserializer is None:
            return self.marshaller.loads(data)
        return data  # already readable

    def set(self, sid, session):
        key = self.prefix + sid
        assert isinstance(session, dict)
        if self.memcache.serializer is None:
            data = self.marshaller.dumps(session)
        else:
            data = session  # will be marshalled
        self.memcache.set(key, data, expire=self.delta)

    def clear(self, sid):
        key = self.prefix + sid
        self.memcache.delete(key)

    def touch(self, sid):
        key = self.prefix + sid
        self.memcache.touch(key, expire=self.delta)
