import random
import string
from card_formatter import CardFormatter
from hearthstone_card_generator import CardGenerator, CardInformationDatabase

class PostGenerator:
    def __init__(self):
        self.__cardGenerator = CardGenerator(CardInformationDatabase())
        self.__cardFormatter = CardFormatter()
                        
    def generate_post_text(self, CommentWithBracketedTexts, imagePosts):
        postText = ''
        for bracketedText in CommentWithBracketedTexts.bracketedTexts:
            imagePost = random.choice(imagePosts)
            postText += self.__generate_post_description(bracketedText, imagePost.url, imagePost.permalink)
        postText += '[About](https://www.reddit.com/r/DruidscanBot/comments/9u0e36/how_this_works/)&nbsp;&nbsp;[Code for nerds](https://github.com/druidscan-bot/druidscan-bot)'
        return postText

    def __generate_post_description(self, name, imageUrl, postUrl):
        card = self.__cardGenerator.generate_random_card(name=name)
        expansion = ''.join(random.choice(string.ascii_lowercase) for _ in range(3)).upper()
        return self.__cardFormatter.format_card(card, imageUrl, postUrl, expansion)