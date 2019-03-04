from pyykov import Pyykov

class DescriptionGenerator:
    def __init__(self):
        descriptions = open('descriptions.txt', 'r').read().split('\n')
        self.__markovGenerator = Pyykov(2)
        self.__markovGenerator.set_source(descriptions)
    def generate_description(self, phrases):
        description = ''
        for i in range(phrases):
            description += self.__markovGenerator.generate_phrase()
            if i != phrases - 1:
                description += '  '
        return description