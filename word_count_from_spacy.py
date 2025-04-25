import json
import re
import spacy
from collections import Counter

# Загружаем модель spaCy для русского языка
nlp = spacy.load("ru_core_news_sm")

# Функция обработки отрицаний ("не работает" "не_работает")
def handle_negation(text):
    return re.sub(r"\bне\s+([а-яА-ЯёЁ]+)", r"не_\1", text)

# Функция предобработки текста
def preprocess_text(text):
    text = text.lower()  # Приводим к нижнему регистру
    text = handle_negation(text)  # Обрабатываем отрицания
    text = re.sub(r"[^а-яА-ЯёЁ]", " ", text)  # Убираем знаки препинания

    doc = nlp(text)  # Обрабатываем текст в spaCy
    tokens = [
        token.lemma_ 
        for token in doc 
        if token.is_alpha and not token.is_stop and 
           (token.pos_ == "ADJ" or (token.pos_ == "VERB" and "Aspect=Imp" in token.morph))
    ]  # Лемматизация + фильтр по частям речи
    
    return tokens

with open("comments.json", "r", encoding="utf-8") as file:
    reviews_data = json.load(file)

# Объединяем все отзывы в один список
reviews = [f"{r['Достоинства']} {r['Недостатки']} {r['Комментарий']}" for r in reviews_data]

# Подсчет частотности слов
word_freqs = Counter()
for review in reviews:
    word_freqs.update(preprocess_text(review))

print(word_freqs.most_common(10))