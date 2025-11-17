from typing import Iterable

from model.Node import Node

class NaiveBayesModel:
    def __init__(self, train: Iterable[Node], test: Iterable[Node]):
        self.__database = {}
        self.__train = train
        self.__test = test
        self.__emotion_array = [0] * 6

    def get_database(self):
        return self.__database

    def add_database_param(self, word: str, emotion_array: Iterable):
        if word not in self.__database:
            self.__database[word] = [0] * 6
        self.__database[word] = emotion_array

    def fit(self):
        for node in self.__train:
            for word in node.get_phrase():
                if word not in self.__database:
                    self.__database[word] = [0] * 6
                self.__database[word][node.get_emotion()] += 1

        self.__emotion_array = self.get_total_emotion()


    def get_total_emotion(self):
        sums = [0] * 6
        for elem in self.__database:
            sums = [sums[i] + self.__database[elem][i] for i in range(0, 6)]

        return sums

    def predict(self, text: str):
        words = text.lower().split()

        total_words = sum(self.__emotion_array)
        result = [1] * 6

        for emotion in range(6):
            for word in words:
                if word in self.__database:
                    count = self.__database[word][emotion]
                else:
                    count = 0

                naive = (count + 1) / (self.__emotion_array[emotion] + total_words)
                result[emotion] *= naive

        return result.index(max(result))





