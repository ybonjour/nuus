__author__ = 'Yves Bonjour'

import redis
import re


def create_newsletter_store():
    redis_db = redis.Redis("localhost", 6379)
    return RedisNewsletterStore(redis_db)


class RedisNewsletterStore(object):
    def __init__(self, redis):
        self.redis = redis

    def store_email(self, email):
        self.redis.sadd(self._key_newsletter(), email)

    def _key_newsletter(self):
        return "newsletter"


def is_valid(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)