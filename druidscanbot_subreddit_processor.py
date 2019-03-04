import re

class DruidscanbotSubredditProcessor:
    def process(self, druidscanbotSubreddit):
        return [x for x in druidscanbotSubreddit.hot(limit=20) if not re.match(
            r'.*www\.reddit\.com.*', x.url, re.M | re.I)]