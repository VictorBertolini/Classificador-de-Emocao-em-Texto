from typing import Iterable

from model.NaiveBayesModel import NaiveBayesModel

class StringToModelMapper:
        def map_string_to_model(self, lines: Iterable, model: NaiveBayesModel):
            for line in lines:
                line = line.strip().split(",")
                model.add_database_param(line[0], [int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5]), int(line[6])])
