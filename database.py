import os

class Database:
    def __init__(self, filepath):
        self.__filepath = filepath
        if not os.path.isfile(self.__filepath):
            self.__posts_replied_to = []
        else:
            with open(self.__filepath, 'r') as f:
                self.__posts_replied_to = list(
                    filter(None, f.read().split('\n')))

    def postsRepliedTo(self):
        return self.__posts_replied_to
    def add_post_id_to_replied(self, postId):
        self.__posts_replied_to.append(postId)

    def save(self):
        with open(self.__filepath, 'w') as f:
            for post_id in set(self.__posts_replied_to):
                f.write(post_id + '\n')