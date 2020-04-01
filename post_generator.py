import random
import string
from card_formatter import CardFormatter
from hearthstone_card_generator import CardGenerator, CardInformationDatabase

class PostGenerator:
    def __init__(self, oger = False):
        self.__cardGenerator = CardGenerator(CardInformationDatabase())
        self.__cardFormatter = CardFormatter()
        self.__oger = oger
        self.__oger_url = "https://gamepedia.cursecdn.com/hearthstone_gamepedia/f/fd/Boulderfist_Ogre%2860%29.png?version=83eec8878f34ec78efa9a33c622d6c01"
                        
    def generate_post_text(self, CommentWithBracketedTexts, imagePosts):
        postText = ''
        for bracketedText in CommentWithBracketedTexts.bracketedTexts:
            imagePost = random.choice(imagePosts) if not self.__oger else ImagePostMock(self.__oger_url) 
            postText += self.__generate_post_description(bracketedText, imagePost.url, imagePost.permalink)
        if not self.__oger:
            postText += '[About](https://www.reddit.com/r/DruidscanBot/comments/9u0e36/how_this_works/)&nbsp;&nbsp;[Code for nerds](https://github.com/druidscan-bot/druidscan-bot)'
        return postText.rstrip()

    def __generate_post_description(self, name, imageUrl, postUrl):
        card = self.__cardGenerator.generate_random_card(name=name) if not self.__oger else self.__cardGenerator.get_card_information("Boulderfist Ogre")
        expansion = ''.join(random.choice(string.ascii_lowercase) for _ in range(3)).upper() if not self.__oger else "Basic"
        return self.__cardFormatter.format_card(card, imageUrl, postUrl, expansion)

class ImagePostMock:
    def __init__(self, url):
        self.url = url
        self.permalink = ''