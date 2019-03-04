import re
from comment_with_bracketed_texts import CommentWithBracketedTexts

class HearthstoneCirclejerkSubredditProcessor:
    def process(self, hearthstoneCirclejerkSubreddit):
        resultLimit = 30
        
        submissions = []
        for submission in hearthstoneCirclejerkSubreddit.new(limit=resultLimit):
            submissions.append(submission)
        for submission in hearthstoneCirclejerkSubreddit.hot(limit=resultLimit):
            if submission not in submissions:
                submissions.append(submission)

        commentsWithBracketedTexts = []
        for submission in submissions:
            for commentWithBracketedText in self.__extract_comments_with_bracketed_text_from_submission(submission):
                commentsWithBracketedTexts.append(commentWithBracketedText)
        return commentsWithBracketedTexts

    def __extract_comments_with_bracketed_text_from_submission(self, submission):
        commentsWithBracketedTexts = []
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            matches = re.findall(r'\\?\[\\?\[(.*?)\\?\]\\?\]', comment.body, re.M | re.I)
            if len(matches) != 0:
                commentsWithBracketedTexts.append(CommentWithBracketedTexts(comment, matches))
        return commentsWithBracketedTexts