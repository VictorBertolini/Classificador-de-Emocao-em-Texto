import os

class StopWordCutter:
    def __init__(self):
        self.__stop_words = []

    def get_stop_words_list(self):
        return self.__stop_words

    def get_stop_words_from_txt(self, filename="stopwords.txt"):
        path = os.path.join("data", filename)

        with open(file=path, mode="r", encoding="utf-8") as file:
            lines = file.readlines()
            self.__stop_words = [line.strip('\n') for line in lines]

    def cut_stop_word_from_line(self, words: list[str]):
        return [w for w in words if w not in self.__stop_words]

