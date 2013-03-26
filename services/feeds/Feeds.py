__author__ = 'Yves Bonjour'

import redis


class Feed(object):
    def __init__(self, url, name):
        # TODO: how to detect url equality (e.g. case-sensitive)
        self.url = url
        self.name = name

    def get_url(self):
        return self.url

    def get_name(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Feed):
            return self.url == other.url and self.name == other.name

        return NotImplemented

    def __ne__(self, other):
        are_equal = self.__eq__(other)
        if are_equal is NotImplemented:
            return are_equal

        return not are_equal


def create_feeds():
    redis_db = redis.Redis("localhost", 6379)
    store = RedisFeedStore(redis)
    return Feeds(store)


class Feeds(object):
    def __init__(self, store):
        self.store = store

    def add_feed(self, feed, user):
        self.store.add_feed(feed)
        self.store.assign_feed(user, feed)

    def get_feed_urls(self):
        return self.store.get_feed_urls()


class MemoryFeedStore(object):
    def __init__(self):
        self.feeds = {}
        self.users = {}

    def add_feed(self, feed):
        self.feeds[feed.url] = feed

    def assign_feed(self, user_id, feed):
        if feed.get_url() not in self.feeds:
            raise ValueError("Invalid feed")

        if user_id not in self.users:
            self.users[user_id] = []

        self.users[user_id].append(feed.get_url())

    def get_feed_urls(self):
        return self.feeds

    def get_users_feeds(self, user_id):
        return [self.feeds[url] for url in self.users.get(user_id, []) if url in self.feeds]


class RedisFeedStore(object):
    def __init__(self, redis):
        self.redis = redis

    def add_feed(self, feed):
        feed_dic = {"name": feed.name, "url": feed.get_url()}
        self.redis.hmset(self._key_feed(feed.get_url()), feed_dic)
        self.redis.sadd(self._key_urls(), feed.get_url())

    def assign_feed(self, user_id, feed):
        if not self.redis.exists(self._key_feed(feed.get_url())):
            raise ValueError("Invalid feed")

        self.redis.sadd(self._key_user(user_id), feed.get_url())

    def get_feed_urls(self):
        return self.redis.smembers(self._key_urls())

    def get_users_feeds(self, user_id):
        if not self.redis.exists(self._key_user(user_id)):
            return []

        feeds = []
        for url in self.redis.smembers(self._key_user(user_id)):
            d = self.redis.hgetall(self._key_feed(url))
            feeds.append(Feed(d["url"], d["name"]))

        return feeds

    def _key_feed(self, feed_url):
        return "feeds:feed:{feed}".format(feed=feed_url)

    def _key_urls(self):
        return "feeds:urls"

    def _key_user(self, user_id):
        return "feeds:user:{user_id}".format(user_id=user_id)