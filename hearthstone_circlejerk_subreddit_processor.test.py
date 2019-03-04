import unittest
from hearthstone_circlejerk_subreddit_processor import HearthstoneCirclejerkSubredditProcessor

class HearthstoneCirclejerkSubredditProcessorTests(unittest.TestCase):
    def setUp(self):
        self.hearthstoneCirclejerkSubredditProcessor = HearthstoneCirclejerkSubredditProcessor() 
    def test_processes_subreddit_properly_with_no_bracketed_texts(self):
        newSubmissions = self.generate_submissions(self.generate_comments("text without brackets", 1), 20)
        hotSubmissions = self.generate_submissions(self.generate_comments("text without brackets", 1), 20)
        mockHearthstoneCirclejerkSubreddit = MockHearthstoneCirclejerkSubreddit(newSubmissions, hotSubmissions)
        self.assertEqual([], self.hearthstoneCirclejerkSubredditProcessor.process(mockHearthstoneCirclejerkSubreddit))

    def test_process_subreddit_properly_with_bracketed_texts(self):
        newSubmissions = self.generate_submissions(self.generate_comments("text without brackets", 1), 20)
        hotSubmissions = self.generate_submissions(self.generate_comments("text with [[brackets]]", 1), 3)
        mockHearthstoneCirclejerkSubreddit = MockHearthstoneCirclejerkSubreddit(newSubmissions, hotSubmissions)
        commentsWithBracketedText = self.hearthstoneCirclejerkSubredditProcessor.process(mockHearthstoneCirclejerkSubreddit)
        self.assertEqual(3, len(commentsWithBracketedText))
        self.assertEqual(["brackets"], commentsWithBracketedText[0].bracketedTexts)
        self.assertEqual(["brackets"], commentsWithBracketedText[1].bracketedTexts)
        self.assertEqual(["brackets"], commentsWithBracketedText[2].bracketedTexts)

    def test_process_subreddit_properly_with_posts_in_hot_and_new(self):
        newSubmissions = self.generate_submissions(self.generate_comments("test with [[brackets]]", 1), 1)
        hotSubmissions = self.generate_submissions(self.generate_comments("test with [[brackets]]", 1), 1)
        mockHearthstoneCirclejerkSubreddit = MockHearthstoneCirclejerkSubreddit(newSubmissions, hotSubmissions)
        commentsWithBracketedText = self.hearthstoneCirclejerkSubredditProcessor.process(mockHearthstoneCirclejerkSubreddit)
        self.assertEqual(2, len(commentsWithBracketedText))
        self.assertEqual(["brackets"], commentsWithBracketedText[0].bracketedTexts)
        self.assertEqual(["brackets"], commentsWithBracketedText[1].bracketedTexts)

    def test_process_subreddit_properly_with_posts_that_have_multiple_bracketed_text(self):
        newSubmissions = self.generate_submissions(self.generate_comments("[[bracketsOne]] [[bracketsTwo]]", 1), 1)
        hotSubmissions = self.generate_submissions(self.generate_comments("text without brackets", 1), 20)
        mockHearthstoneCirclejerkSubreddit = MockHearthstoneCirclejerkSubreddit(newSubmissions, hotSubmissions)
        commentsWithBracketedText = self.hearthstoneCirclejerkSubredditProcessor.process(mockHearthstoneCirclejerkSubreddit)
        self.assertEqual(1, len(commentsWithBracketedText))
        self.assertEqual(["bracketsOne", "bracketsTwo"], commentsWithBracketedText[0].bracketedTexts)
    
    def test_process_subreddit_properly_with_posts_that_have_multiple_children(self):
        newSubmissions = self.generate_submissions(self.generate_comments("[[brackets]]", 10), 1)
        hotSubmissions = self.generate_submissions(self.generate_comments("[[brackets]]", 10), 1)
        mockHearthstoneCirclejerkSubreddit = MockHearthstoneCirclejerkSubreddit(newSubmissions, hotSubmissions)
        commentsWithBracketedText = self.hearthstoneCirclejerkSubredditProcessor.process(mockHearthstoneCirclejerkSubreddit)
        self.assertEqual(20, len(commentsWithBracketedText))
        
    def test_process_subreddit_ignores_posts_beyond_30th_post(self):
        newSubmissions = self.generate_submissions(self.generate_comments("[[brackets]]", 1), 100)
        hotSubmissions = self.generate_submissions(self.generate_comments("[[brackets]]", 1), 100)
        mockHearthstoneCirclejerkSubreddit = MockHearthstoneCirclejerkSubreddit(newSubmissions, hotSubmissions)
        commentsWithBracketedText = self.hearthstoneCirclejerkSubredditProcessor.process(mockHearthstoneCirclejerkSubreddit)
        self.assertEqual(60, len(commentsWithBracketedText))

    def test_process_subreddit_ignores_duplicate_posts(self):
        submissions = self.generate_submissions(self.generate_comments("[[brackets]]", 1), 10)
        newSubmissions = submissions
        hotSubmissions = submissions
        mockHearthstoneCirclejerkSubreddit = MockHearthstoneCirclejerkSubreddit(newSubmissions, hotSubmissions)
        commentsWithBracketedText = self.hearthstoneCirclejerkSubredditProcessor.process(mockHearthstoneCirclejerkSubreddit)
        self.assertEqual(10, len(commentsWithBracketedText))

    def generate_comments(self, text, amount):
        comments = []
        for _ in range(amount):
            comments.append(MockComment(text))
        return comments
    def generate_submissions(self, comments, amount):
        submissions = []
        for _ in range(amount):
            submissions.append(MockSubmission(comments))
        return submissions

class MockHearthstoneCirclejerkSubreddit:
    def __init__(self, newSubmissions, hotSubmissions):
        self.__newSubmissions = newSubmissions
        self.__hotSubmissions = hotSubmissions
    def new(self, limit):
        return self.__newSubmissions[:limit]
    def hot(self, limit):
        return self.__hotSubmissions[:limit]

class MockSubmission:
    def __init__(self, comments):
        self.comments = MockComments(comments)

class MockComments:
    def __init__(self, comments):
        self.__comments = comments
    def replace_more(self, limit):
        return
    def list(self):
        return self.__comments

class MockComment:
    def __init__(self, commentText):
        self.body = commentText

if __name__ == '__main__':
    unittest.main()