# Classificador de Sentimentos com Naive Bayes (Feito do Zero)

Este projeto implementa, do zero, um classificador de sentimentos baseado em **Naive Bayes**, utilizando uma base de dados do Kaggle.
O modelo é capaz de analisar textos curtos e classificá-los em **6 emoções** distintas:

* 😢 Sadness
* 😄 Joy
* ❤️ Love
* 😡 Anger
* 😨 Fear
* 😲 Surprise

O foco principal é **educacional**, mostrando como funciona um classificador probabilístico sem o uso de bibliotecas de machine learning como scikit-learn.

---

# Objetivo

O objetivo deste repositório é demonstrar, de maneira clara e didática, como construir um modelo de classificação de sentimentos usando apenas:

* Python puro
* Pré-processamento manual
* Contagem de frequências
* Probabilidades do Naive Bayes
* Organização em classes e arquitetura modular

Ideal para quem está aprendendo NLP e quer entender **como as coisas funcionam por baixo dos panos**.

---

# Como executar

### 1 - Instalar dependências

```
pip install openpyxl
```

### 2 Rode o programa:

```
python main.py
```

Você verá o menu:

```
===== Sentiment Analysis =====
1 - Treinar modelo
2 - Ver acurácia do modelo
3 - Usar modelo pré-treinado
```

---

# 🔧 Como o projeto funciona

Abaixo está uma explicação detalhada do pipeline.

---

## **1. Carregamento dos dados**

Utilizamos a classe `Excel` para ler o arquivo emotions.xlsx:

```python
data = Excel("emotions.xlsx").get_data()
```

Cada linha do Excel vira um objeto `Node` contendo:

* a frase
* a emoção correspondente

---

## **2. Divisão em treino e teste**

Os dados são embaralhados e divididos conforme o padrão:

* **80% treino**
* **20% teste**

```python
trainNodes, testNodes = do_train_test_split(nodes)
```

---

## **3. Pré-processamento**

Cada frase passa por:

1. **lowercase**
2. **divisão em palavras**
3. **remoção de stopwords**

Isso é feito na classe `Node`:

```python
self.__phrase = phraseManipulator.to_lower(self.__phrase)
self.__phrase = phraseManipulator.split_phrase(self.__phrase)
self.__phrase = stopWordCutter.cut_stop_word_from_line(self.__phrase)
```

---

## **4. Treinamento do Naive Bayes**

O modelo percorre todas as palavras do set de treino e constrói um dicionário:

```
"love":  [5, 120, 80, 2, 0, 3]
          ↑   ↑   ↑
         Sad Joy Love ...
```

Cada posição da lista representa a frequência da palavra em cada emoção.

Trecho essencial:

```python
for word in node.get_phrase():
    if word not in self.__database:
        self.__database[word] = [0] * 6
    self.__database[word][node.get_emotion()] += 1
```

Ao final, é calculado o total de palavras de cada emoção.

---

**Fundamentos Matemáticos**

O modelo usa o algoritmo **Naive Bayes**, que basicamente tenta descobrir **qual sentimento tem a maior chance de gerar as palavras da frase que o usuário digitou**.

**A ideia central é:**

> *"Para cada emoção, veja o quão provável é que ela gere as palavras da frase. No final, escolho a emoção com maior probabilidade."*

Para isso, usamos uma conta chamada **probabilidade condicional**.

---

## **Probabilidade de uma palavra aparecer em um sentimento**

Durante o treinamento, contamos quantas vezes cada palavra aparece em cada emoção:
```
love → [5, 120, 80, 2, 0, 3]
         ↑   ↑   ↑
       Sad Joy Love ...
```
> Nesse exemplo a palava `love` apareceu 5 vezes em frases tristes, 120 em frases alegres, 80 em amorosas, etc

Com isso, calculamos:

$$
P(W|S) = \frac{\text{count}(W,S) + 1}{\text{Total}_S + \text{Total}_{\text{palavras}}}
$$

Essa é a probabilidade da palavra **W** aparecer dentro do sentimento **S**. Usamos "+1" para evitar divisão por zero — isso se chama **suavização de Laplace**.

---

## **Combinando todas as palavras da frase**

Se a frase tem várias palavras, calculamos a probabilidade de cada uma pertencer ao sentimento S e multiplicamos:

$$
R_S = P(W_1|S) \times P(W_2|S) \times \cdots \times P(W_n|S)
$$

Esse número final representa o "quão compatível" a frase é com aquele sentimento.

---

## **Escolha da emoção final**

Depois de fazer isso para:
- Sadness
- Joy  
- Love
- Anger
- Fear
- Surprise

Escolhemos a emoção com o maior valor:

$$
\text{Emotion} = \arg\max_S (R_S)
$$

Ou seja: **a emoção mais provável segundo o Naive Bayes**.



---

# Sobre Stemming (e por que não foi usado)

Foi implementado um teste com o **PorterStemmer** da NLTK:

* Ele reduz palavras para raízes como:

  * *loving → love*
  * *happiness → happi*
  * *crying → cri*

Embora funcione bem em muitos contextos, **neste modelo o stemming reduziu a acurácia** de:

```
68–70% (sem stemming)
↓
65% (com stemming)
```

### **Por quê?**

Porque o PorterStemmer perde muita informação semântica e gera tokens que não existem no vocabulário original:

```
happy → happi
happiness → happi
```

Como o modelo depende **exclusivamente de contagens exatas das palavras**, ele deixa de reconhecer palavras importantes, o que reduz a precisão.

Por isso, o projeto utiliza **palavras originais**, apenas normalizadas e com stopwords removidas.

---

# Acurácia obtida

Em média, o modelo obtém:

```
Acurácia: 68% – 70%
```

Isso é esperado para um Naive Bayes simples com foco no viés educativo.

---

# 💬 Como usar o modelo (opção 3)

Depois de treinar ou carregar o `params.txt`, você pode digitar frases:

```
Digite um texto: I'm loving it
Sentimento detectado: Love
```

---

