from string_manipulators.PhraseManipulator import PhraseManipulator
from string_manipulators.StopWordCutter import StopWordCutter


class Node:
    def __init__(self, phrase, emotion):
        self.__phrase = phrase
        self.__emotion = int(emotion)
        self.__occurence = [0] * 6

    def get_phrase(self):
        return self.__phrase

    def get_emotion(self):
        return self.__emotion

    def get_occurence(self):
        return self.__occurence

    def show(self):
        print(f"{self.__emotion} -> {self.__phrase}")

    def clean_and_prepare_node(self, phraseManipulator: PhraseManipulator, stopWordCutter: StopWordCutter):
        self.__phrase = phraseManipulator.to_lower(self.__phrase)
        self.__phrase = phraseManipulator.split_phrase(self.__phrase)
        self.__phrase = stopWordCutter.cut_stop_word_from_line(self.__phrase)
