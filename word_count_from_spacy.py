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
# Вызов анализа
def analyze_reviews(json_path: str, top_n: int = 10) -> list[tuple[str, int]]:
    try:
        # with open("citilink_reviews_1472659_125.json", "r", encoding="utf-8") as file:
        #     reviews_data = json.load(file)
        with open(json_path, "r", encoding="utf-8") as file:
            reviews_data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {json_path} не найден.")
    except json.JSONDecodeError:
        raise ValueError(f"Файл {json_path} не является корректным JSON.")        

    # # Объединяем все отзывы в один список
    # reviews = [f"{r['Достоинства']} {r['Недостатки']} {r['Комментарий']}" for r in reviews_data]
    reviews = [
        f"{r.get('Достоинства', '')} {r.get('Недостатки', '')} {r.get('Комментарий', '')}"
        for r in reviews_data
    ]
    # Подсчет частотности слов
    word_freqs = Counter()
    for review in reviews:
        word_freqs.update(preprocess_text(review))
    return word_freqs.most_common(top_n)
    # print(word_freqs.most_common(top_n))
    
    
# Пример использования
# if __name__ == "__main__":
#     top_words = analyze_reviews("citilink_reviews_1472659_125.json", top_n=10)
#     for word, count in top_words:
#         print(f"{word}: {count}")