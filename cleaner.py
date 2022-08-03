import re

class TextCleaner:
    def text_cleaning(self, text):
        text = re.sub("[^A-Za-z ]","",text)
        text = re.sub(' +', ' ', text)
        return text.lower()