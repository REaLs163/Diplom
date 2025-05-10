import requests
import json
import re
import time as t


def extract_product_id(url):
    match = re.search(r'/product/.+-(\d+)/', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Не удалось извлечь product_id из ссылки.")

def clean_text(text):
    if text and isinstance(text, str) and text.strip():
        text = re.sub(r'[\n\r]+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    return "Не указано"

def get_citilink_reviews(product_id, page=1, per_page=5):
    url = 'https://www.citilink.ru/graphql/'

    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'origin': 'https://www.citilink.ru',
        'referer': f'https://www.citilink.ru/product/{product_id}/otzyvy/?page={page}',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }

    query = """
    query($filter1:Catalog_ProductFilterInput!$input2:UGC_OpinionsInput!){
        product_b6304_0d594:product(filter:$filter1){
            opinions_03450_3ec12:opinions(input:$input2){
                payload{
                    items{ 
                        pros 
                        cons 
                        text  
                    }
                }
                pageInfo{
                    page 
                    perPage 
                    totalItems 
                    totalPages 
                    hasNextPage 
                    hasPreviousPage
                }
            }
        }
    }
    """

    variables = {
        "filter1": {"id": product_id},
        "input2": {
            "pagination": {
                "page": page,
                "perPage": per_page
            },
            "withGroup": True
        }
    }

    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка запроса: {response.status_code}")
        return None

def get_total_reviews_count(product_id):
    data = get_citilink_reviews(product_id, page=1, per_page=1)
    if data:
        page_info = data['data']['product_b6304_0d594']['opinions_03450_3ec12']['pageInfo']
        return page_info['totalItems']
    else:
        raise Exception("Не удалось получить общее количество отзывов.")

def collect_reviews(product_url, total_reviews_needed, per_page=5):
    start_time = t.time()
    product_id = extract_product_id(product_url)

    total_available = get_total_reviews_count(product_id)
    print(f"Всего отзывов на сайте: {total_available}")

    if total_reviews_needed > total_available:
        print(f"Запрошено {total_reviews_needed} отзывов, но доступно только {total_available}.")
        total_reviews_needed = total_available

    collected_reviews = []
    page = 1

    while len(collected_reviews) < total_reviews_needed:
        remaining_reviews = total_reviews_needed - len(collected_reviews)
        current_per_page = min(per_page, remaining_reviews)

        data = get_citilink_reviews(product_id, page, current_per_page)

        if data:
            items = data['data']['product_b6304_0d594']['opinions_03450_3ec12']['payload']['items']
            if not items:
                print("Больше отзывов нет.")
                break

            for item in items:
                cleaned_review = {
                    "Достоинства": clean_text(item.get("pros", "")),
                    "Недостатки": clean_text(item.get("cons", "")),
                    "Комментарий": clean_text(item.get("text", ""))
                }
                collected_reviews.append(cleaned_review)

            if not data['data']['product_b6304_0d594']['opinions_03450_3ec12']['pageInfo']['hasNextPage']:
                print("Достигнут конец отзывов на сайте.")
                break

            page += 1
        else:
            print("Ошибка при получении данных.")
            break
    
    filename = f'citilink_reviews_{product_id}_{len(collected_reviews)}.json'
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(collected_reviews, json_file, ensure_ascii=False, indent=4)

    end_time = t.time()
    print(f"Отзывы сохранены в файл: {filename}")
    print(f"Парсинг отзывов выполнился за {round(end_time - start_time, 2)} секунд.")


# ---- Ввод данных пользователем ----
# product_link = input("Введите ссылку на товар Citilink: ").strip()
# try:
#     count_of_reviews = int(input("Сколько отзывов собрать?: ").strip())
#     collect_reviews(product_link, total_reviews_needed=count_of_reviews)
# except ValueError:
#     print("Ошибка: количество отзывов должно быть целым числом.")