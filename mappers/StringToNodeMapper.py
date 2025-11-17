from typing import Iterable

from model.Node import Node
from string_manipulators.PhraseManipulator import PhraseManipulator
from string_manipulators.StopWordCutter import StopWordCutter


class StringToNodeMapper:
    def map_string_to_node(self, info: Iterable) -> Node:
        text = info[0]
        emotion = info[1]
        return Node(text, emotion)

    def map_node_cleaning(self, nodes, phraseManipulator: PhraseManipulator, stopWordCutter: StopWordCutter):
        for node in nodes:
            node.clean_and_prepare_node(phraseManipulator, stopWordCutter)
        return nodes