__author__ = 'Yves Bonjour'

import unittest

from Feeds import Feed
from Feeds import MemoryFeedStore
from Feeds import RedisFeedStore
from Feeds import Feeds
from FeedStoreMock import FeedStoreMock
import uuid
import redis


class FeedTest(unittest.TestCase):
    def test_equals_same_values(self):
        # Arrange
        feed1 = Feed("http://www.ethz.ch", "ETHZ")
        feed2 = Feed("http://www.ethz.ch", "ETHZ")

        # Act
        result = feed1 == feed2

        # Assert
        self.assertTrue(result)

    def test_equals_different_name(self):
        # Arrange
        feed1 = Feed("http://www.ethz.ch", "BFH")
        feed2 = Feed("http://www.ethz.ch", "ETHZ")

        # Act
        result = feed1 == feed2

        # Assert
        self.assertFalse(result)

    def test_equals_different_url(self):
        # Arrange
        feed1 = Feed("http://www.bfh.ch", "ETHZ")
        feed2 = Feed("http://www.ethz.ch", "ETHZ")

        # Act
        result = feed1 == feed2

        # Assert
        self.assertFalse(result)

    def test_equals_none(self):
        # Arrange
        feed1 = Feed("http://www.bfh.ch", "ETHZ")

        # Act
        result = feed1.__eq__(None)

        # Assert
        self.assertEqual(NotImplemented, result)

    def test_not_equals_same_values(self):
        # Arrange
        feed1 = Feed("http://www.ethz.ch", "ETHZ")
        feed2 = Feed("http://www.ethz.ch", "ETHZ")

        # Act
        result = feed1 != feed2

        # Assert
        self.assertFalse(result)

    def test_not_equals_different_name(self):
        # Arrange
        feed1 = Feed("http://www.ethz.ch", "BFH")
        feed2 = Feed("http://www.ethz.ch", "ETHZ")

        # Act
        result = feed1 != feed2

        # Assert
        self.assertTrue(result)

    def test_not_equals_different_url(self):
        # Arrange
        feed1 = Feed("http://www.bfh.ch", "ETHZ")
        feed2 = Feed("http://www.ethz.ch", "ETHZ")

        # Act
        result = feed1 != feed2

        # Assert
        self.assertTrue(result)

    def test_not_equals_none(self):
        # Arrange
        feed1 = Feed("http://www.bfh.ch", "ETHZ")

        # Act
        result = feed1.__ne__(None)

        # Assert
        self.assertEquals(NotImplemented, result)


class FeedStoreTest(object):
    def test_add_feed(self):
        # Arrange
        url = "http://www.ethz.ch"
        feed = Feed(url, "ETHZ")

        # Act
        self.store.add_feed(feed)

        # Assert
        urls = self.store.get_feed_urls()
        self.assertEquals(1, len(urls))
        self.assertIn(url, urls)

    def test_add_feed_twice(self):
        # Arrange
        url = "http://www.ethz.ch"
        feed = Feed(url, "ETHZ")
        self.store.add_feed(feed)

        # Act
        self.store.add_feed(feed)

        # Assert
        urls = self.store.get_feed_urls()
        self.assertEquals(1, len(urls))
        self.assertIn(url, urls)

    def test_add_two_different_feeds_twice(self):
        # Arrange
        url1 = "http://www.ethz.ch"
        feed1 = Feed(url1, "ETHZ")

        url2 = "http://www.bfh.ch"
        feed2 = Feed(url2, "BFH")

        self.store.add_feed(feed1)

        # Act
        self.store.add_feed(feed2)

        # Assert
        urls = self.store.get_feed_urls()
        self.assertEquals(2, len(urls))
        self.assertIn(url1, urls)
        self.assertIn(url2, urls)

    def test_get_feed_urls_no_urls(self):
        # Act
        urls = self.store.get_feed_urls()

        # Assert
        self.assertEquals(0, len(urls))

    def test_assign_feed(self):
        # Arrange
        url = "http://www.ethz.ch"
        feed = Feed(url, "ETHZ")
        self.store.add_feed(feed)

        user_id = uuid.uuid4()

        # Act
        self.store.assign_feed(user_id, feed)

        # Assert
        feeds = self.store.get_users_feeds(user_id)
        self.assertEquals(1, len(feeds))
        self.assertIn(feed, feeds)

    def test_assign_feed_not_existing_feed(self):
        # Arrange
        url = "http://www.ethz.ch"
        feed = Feed(url, "ETHZ")

        user_id = uuid.uuid4()

        # Act
        self.assertRaises(ValueError, self.store.assign_feed, user_id, feed)

    def test_assign_feed_two_feeds_same_user(self):
        # Arrange
        url1 = "http://www.ethz.ch"
        feed1 = Feed(url1, "ETHZ")
        self.store.add_feed(feed1)

        url2 = "http://www.bfh.ch"
        feed2 = Feed(url2, "BFH")
        self.store.add_feed(feed2)

        user_id = uuid.uuid4()

        # Act
        self.store.assign_feed(user_id, feed1)
        self.store.assign_feed(user_id, feed2)

        # Assert
        feeds = self.store.get_users_feeds(user_id)
        self.assertEquals(2, len(feeds))
        self.assertIn(feed1, feeds)
        self.assertIn(feed2, feeds)

    def test_assign_feed_two_feeds_to_different_users(self):
        # Arrange
        url1 = "http://www.ethz.ch"
        feed1 = Feed(url1, "ETHZ")
        self.store.add_feed(feed1)

        url2 = "http://www.bfh.ch"
        feed2 = Feed(url2, "BFH")
        self.store.add_feed(feed2)

        user_id1 = uuid.uuid4()
        user_id2 = uuid.uuid4()

        # Act
        self.store.assign_feed(user_id1, feed1)
        self.store.assign_feed(user_id2, feed2)

        # Assert
        feeds_user1 = self.store.get_users_feeds(user_id1)
        self.assertEquals(1, len(feeds_user1))
        self.assertIn(feed1, feeds_user1)

        feeds_user2 = self.store.get_users_feeds(user_id2)
        self.assertEquals(1, len(feeds_user2))
        self.assertIn(feed2, feeds_user2)

    def test_get_users_feed_user_with_no_feeds(self):
        # Arrange
        user_id = uuid.uuid4()

        # Act
        feeds = self.store.get_users_feeds(user_id)

        # Assert
        self.assertEquals(0, len(feeds))


class MemoryFeedStoreTest(FeedStoreTest, unittest.TestCase):
    def setUp(self):
        self.store = MemoryFeedStore()

class RedisFeedStoreTest(FeedStoreTest, unittest.TestCase):
    def setUp(self):
        self.redis = redis.Redis("localhost", 6379, db=2)
        self.redis.flushdb()
        self.store = RedisFeedStore(self.redis)

    def tearDown(self):
        self.redis.flushdb()


class FeedsTest(unittest.TestCase):
    def setUp(self):
        self.store_mock = FeedStoreMock()
        self.feeds = Feeds(self.store_mock)

    def test_add_feed(self):
        # Arrange
        feed = Feed("http://www.ethz.ch", "ETHZ")
        user_id = uuid.uuid4()

        # Act
        self.feeds.add_feed(feed, user_id)

        # Assert
        self.assertEquals(1, self.store_mock.num_method_calls("add_feed"))
        arguments_add = self.store_mock.get_arguments("add_feed")
        self.assertEquals(1, len(arguments_add))
        self.assertEquals(feed, arguments_add[0])

        self.assertEquals(1, self.store_mock.num_method_calls("assign_feed"))
        arguments_assign = self.store_mock.get_arguments("assign_feed")
        self.assertEquals(2, len(arguments_assign))
        self.assertEquals(user_id, arguments_assign[0])
        self.assertEquals(feed, arguments_assign[1])

    def test_get_feed_urls(self):
        # Arrange
        urls = ["http://www.ethz.ch"]
        self.store_mock.set_feed_urls(urls)

        # Act
        feed_urls = self.store_mock.get_feed_urls()

        # Assert
        self.assertEquals(urls, feed_urls)
        self.assertEquals(1, self.store_mock.num_method_calls("get_feed_urls"))


if __name__ == '__main__':
    unittest.main()
