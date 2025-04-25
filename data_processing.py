import json
from bs4 import BeautifulSoup
import re

with open("page.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Находим все блоки с отзывами
comments = [] # Список для хранения отзывов
review_blocks = soup.find_all("div", class_="app-catalog-1mg14ol-ContentWrapper--StyledContentWrapper") # Находим все блоки с отзывами

# Убираем лишние пробелы и переносы строк
def clean_text(text):
    if text:
        # Убираем все символы новой строки, символы возврата каретки, и заменяем несколько пробелов на один
        text = re.sub(r'[\n\r]+', ' ', text)  # Заменяем все переносы строк и возвраты каретки на пробелы
        text = re.sub(r'\s+', ' ', text)  # Заменяем все виды пробельных символов (включая несколько пробелов) на один
        return text.strip()  # Убираем лишние пробелы в начале и в конце
    return 

# Обрабатываем все блоки с отзывами
for block in review_blocks: 
    advantages = block.find("h5", string="Достоинства")
    disadvantages = block.find("h5", string="Недостатки")
    comment_text = block.find("h5", string="Комментарий")
    
    # Извлекаем текст отзыва из соответствующих элементов
    review = {
        "Достоинства": clean_text(advantages.find_next("span").text) if advantages else "Не указано",
        "Недостатки": clean_text(disadvantages.find_next("span").text) if disadvantages else "Не указано",
        "Комментарий": clean_text(comment_text.find_next("span").text) if comment_text else "Не указано",
    }
    
    # Добавляем отзыв в список
    comments.append(review)

# Сохраняем в JSON
with open("comments.json", "w", encoding="utf-8") as json_file:
    json.dump(comments, json_file, ensure_ascii=False, indent=4)

print("Комментарии сохранены в comments.json")