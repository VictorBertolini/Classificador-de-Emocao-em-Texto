from random import sample
from typing import Iterable

from repository.Excel import *
from model.NaiveBayesModel import NaiveBayesModel
from mappers.StringToNodeMapper import StringToNodeMapper
from repository.TextFile import TextFile
from mappers.StringToModelMapper import StringToModelMapper
from string_manipulators.PhraseManipulator import PhraseManipulator
from string_manipulators.StopWordCutter import StopWordCutter

def print_emotion(emotion):
    emotions = ["Sadness", "Joy", "Love", "Anger", "Fear", "Surprise"]
    print(emotions[emotion])

def get_excel_data(excel: Excel) -> Iterable:
    return excel.get_data()

def map_string_to_nodes(lines: Iterable[str]):
    mapper = StringToNodeMapper()
    nodes = []

    for line in lines:
        nodes.append(mapper.map_string_to_node(line))

    return nodes

def do_train_test_split(nodes):
    size = len(nodes)
    shuffle_index = sample(population = range(0, size), k = size)
    nodes = [nodes[i] for i in shuffle_index]

    trainNodes = nodes[:round(size * 0.8)]
    testNodes = nodes[round(size * 0.8):]

    return trainNodes, testNodes

def clean_nodes(nodes):
    mapper = StringToNodeMapper()
    pm = PhraseManipulator()
    sw = StopWordCutter()

    sw.get_stop_words_from_txt("stopwords.txt")
    return mapper.map_node_cleaning(nodes, pm, sw)

def load_trained_model(file_name="params.txt"):
    model = NaiveBayesModel([], [])
    mapper = StringToModelMapper()
    txt = TextFile(file_name)

    lines = txt.get_database_lines_from_txt()
    mapper.map_string_to_model(lines, model)

    # recalcular totais
    model._NaiveBayesModel__emotion_array = model.get_total_emotion()
    return model


def option_train_model():
    print("\n===== TREINAR MODELO =====")

    data = get_excel_data(Excel("emotions.xlsx"))
    nodes = map_string_to_nodes(data)
    nodes = clean_nodes(nodes)

    train, test = do_train_test_split(nodes)

    model = NaiveBayesModel(train, test)
    model.fit()

    txt = TextFile("params.txt")
    txt.save_model(model)

    print("Modelo treinado e salvo com sucesso!")

def option_model_accuracy():
    print("\n===== TESTAR ACURÁCIA DO MODELO =====")

    data = get_excel_data(Excel("emotions.xlsx"))
    nodes = map_string_to_nodes(data)
    nodes = clean_nodes(nodes)

    train, test = do_train_test_split(nodes)

    model = NaiveBayesModel(train, test)
    model.fit()

    score = 0
    for node in test:
        words = node.get_phrase()
        text = " ".join(words)
        predicted = model.predict(text)

        if predicted == node.get_emotion():
            score += 1

    accuracy = score / len(test)
    print(f"Acurácia do modelo: {accuracy * 100:.2f}%")
    return accuracy

def option_use_model():
    print("\n===== USAR O MODELO =====")
    model = load_trained_model("params.txt")

    pm = PhraseManipulator()
    sw = StopWordCutter()
    sw.get_stop_words_from_txt("stopwords.txt")

    while True:
        text = input("\nDigite um texto (em inglês) (ou 'sair' para sair): ")

        if text.lower() == "sair":
            break

        text = pm.to_lower(text)
        words = pm.split_phrase(text)
        words = sw.cut_stop_word_from_line(words)

        processed = " ".join(words)

        emotion = model.predict(processed)

        print("Sentimento detectado:", end=" ")
        print_emotion(emotion)



def main():
    while True:
        print("===== Sentiment Analysis =====")
        print("1 - Treinar modelo")
        print("2 - Ver acurácia do modelo")
        print("3 - Usar modelo pré-treinado (digitar frases)")
        print("4 - Sair")
        option = input("Escolha uma opção: ")

        if option == "1":
            option_train_model()
        elif option == "2":
            option_model_accuracy()
        elif option == "3":
            option_use_model()
        elif option == '4':
            break
        else:
            print("Opção inválida.")


main()














