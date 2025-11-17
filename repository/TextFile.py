from model.NaiveBayesModel import *
import os

class TextFile:
    def __init__(self, filename):
        if not filename.endswith(".txt"):
            filename += ".txt"
        self.__name = os.path.join("data", filename)

    def get_name(self):
        return self.__name

    def save_model(self, model: NaiveBayesModel):
        try:
            with open(self.__name, mode="w", encoding="utf-8") as file:
                file.write("Word, Sadness, Joy, Love, Anger, Fear, Surprise")

                db = model.get_database()
                for key in db.keys():
                    line = f"{key},{db[key][0]},{db[key][1]},{db[key][2]},{db[key][3]},{db[key][4]},{db[key][5]}"
                    file.write("\n" + line)

        except Exception as e:
            print(e)

    def get_database_lines_from_txt(self):
        try:
            with open(self.__name, mode="r", encoding="utf-8") as file:
                lines = file.readlines()
                lines.pop(0) # Header

        except Exception as e:
            print(e)

        return lines
