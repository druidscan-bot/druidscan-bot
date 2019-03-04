import unittest
from druidscanbot_subreddit_processor import DruidscanbotSubredditProcessor

class DruidscanbotSubredditProcessorTest(unittest.TestCase):
    def setUp(self):
        self.druidscanbotSubredditProcessor = DruidscanbotSubredditProcessor()
    
    def test_process_subreddit_properly_extracts_urls(self):
        posts = self.generate_posts('imgur.com/fakeurl', 1)
        imagePosts = self.druidscanbotSubredditProcessor.process(MockDruidscanbotCirclejerkSubreddit(posts))
        self.assertEqual('imgur.com/fakeurl', imagePosts[0].url)
    
    def test_process_subreddit_ignores_urls_from_reddit(self):
        posts = self.generate_posts('www.reddit.com/fakeurl', 1)
        imagePosts = self.druidscanbotSubredditProcessor.process(MockDruidscanbotCirclejerkSubreddit(posts))
        self.assertEqual(0, len(imagePosts))

    def test_process_subreddit_only_gets_top_20_posts(self):
        posts = self.generate_posts('imgur.com/fakeurl', 100)
        imagePosts = self.druidscanbotSubredditProcessor.process(MockDruidscanbotCirclejerkSubreddit(posts))
        self.assertEqual(20, len(imagePosts))
    
    def generate_posts(self, url, amount):
        posts = []
        for _ in range(amount):
            posts.append(MockPost(url))
        return posts

class MockDruidscanbotCirclejerkSubreddit:
    def __init__(self, posts):
        self.__posts = posts
    def hot(self, limit):
        return self.__posts[:limit]

class MockPost:
    def __init__(self, url):
        self.url = url

if __name__ == '__main__':
    unittest.main()