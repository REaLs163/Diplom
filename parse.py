import requests
import json
import re


def extract_product_id(url):
    match = re.search(r'/product/.+-(\d+)/', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Не удалось извлечь product_id из ссылки.")

def get_citilink_reviews(product_id, page=1, per_page=5):
    url = 'https://www.citilink.ru/graphql/'

    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'origin': 'https://www.citilink.ru',
        'referer': f'https://www.citilink.ru/product/{product_id}/otzyvy/?page={page}',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
    }

    query = """
    query($filter1:Catalog_ProductFilterInput!$input2:UGC_OpinionsInput!){
        product_b6304_0d594:product(filter:$filter1){
            opinions_03450_3ec12:opinions(input:$input2){
                payload{
                    items{
                        id 
                        creationDate 
                        pros 
                        cons 
                        text 
                        rating 
                        authorNickname 
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

def collect_reviews(product_url, total_reviews_needed=50, per_page=5):
    product_id = extract_product_id(product_url)
    collected_reviews = []
    page = 1

    while len(collected_reviews) < total_reviews_needed:
        data = get_citilink_reviews(product_id, page, per_page)

        if data:
            items = data['data']['product_b6304_0d594']['opinions_03450_3ec12']['payload']['items']
            if not items:
                break  # больше отзывов нет

            collected_reviews.extend(items)

            if not data['data']['product_b6304_0d594']['opinions_03450_3ec12']['pageInfo']['hasNextPage']:
                break  # нет следующей страницы
            page += 1
        else:
            break

    # обрезаем, если собрали больше отзывов чем нужно
    collected_reviews = collected_reviews[:total_reviews_needed]

    # Сохраняем в файл
    product_id_clean = product_id
    with open(f'citilink_reviews_{product_id_clean}.json', 'w', encoding='utf-8') as f:
        json.dump(collected_reviews, f, ensure_ascii=False, indent=4)

    # Печатаем
    for review in collected_reviews:
        print(f"Автор: {review.get('authorNickname', 'Аноним')}")
        print(f"Рейтинг: {review['rating']}/5")
        print(f"Дата: {review['creationDate']}")
        print(f"Достоинства: {review['pros']}")
        print(f"Недостатки: {review['cons']}")
        print(f"Комментарий: {review['text']}")
        print("-" * 20)

# Пример использования:
product_link = "https://www.citilink.ru/product/videokarta-palit-nvidia-geforce-rtx-4060-rtx4060-dual-oc-8gb-dual-gddr-1942195/"
count_of_reviews = 50  # сколько отзывов хотим

collect_reviews(product_link, total_reviews_needed=count_of_reviews)