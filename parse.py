from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time as t

def main():
    start_time = t.time()
    options = ChromeOptions()
    options.add_argument("--headless=new")  
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--blink-settings=imagesEnabled=false")
    driver = webdriver.Chrome(options=options)
    wait=WebDriverWait(driver, 5)
    
    try:
        driver.get("https://www.citilink.ru")
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Поиск по товарам']")))
        
        tovar = input('Введите текст: ').replace('"', '').replace('\\', '')
        reviews_limit_input = input("Сколько отзывов хотите получить? Введите число или 'all': ").strip()
        
        # Определяем режим: all или ограниченное число
        is_all = reviews_limit_input.lower() == "all"
        reviews_limit = None if is_all else int(reviews_limit_input) if reviews_limit_input.isdigit() else None

        if not is_all and reviews_limit is None:
            print("Некорректный ввод. Завершение.")
            return
        
        elem = driver.find_element(By.XPATH, "//input[@placeholder = 'Поиск по товарам']")
        elem.send_keys(tovar)
        elem.send_keys(Keys.ENTER)
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/product/')]")))
        elem = driver.find_element(By.XPATH, "//a[contains(@href, '/product/')]")
        driver.execute_script("arguments[0].click();", elem)
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/otzyvy/')]")))
        elem = driver.find_element(By.XPATH, "//a[contains(@href, '/otzyvy/')]")
        driver.execute_script("arguments[0].click();", elem)
        
        # Проверка на отсутствие отзывов
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Для этого товара пока нет отзывов']")))
            print("Отзывов на этот товар пока нет.")
            return
        except:
            pass

        # Ожидание появления кнопки "Показать ещё"
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//button[span[text()='Показать ещё']]")))
        except:
            pass

        # Цикл кликов
        clicks = 0
        max_clicks = None if is_all else max((reviews_limit - 5) // 5, 0)
            
        while True:
            try:
                if max_clicks is not None and clicks >= max_clicks:
                    break
                elem = wait.until(EC.presence_of_element_located((By.XPATH, "//button[span[text()='Показать ещё']]")))
                elem = driver.find_element(By.XPATH, "//button[span[text()='Показать ещё']]")
                driver.execute_script("arguments[0].click();", elem)  
                clicks += 1
                t.sleep(1) 
            except Exception:
                print("Элемент 'Показать ещё' не найден, все отзывы загружены.")
                break
            
        # Подсчёт уникальных отзывов
        soup = BeautifulSoup(driver.page_source, "html.parser")
        review_blocks_raw = soup.find_all("div", class_="app-catalog-1mg14ol-ContentWrapper--StyledContentWrapper")

        unique_reviews = []
        seen_texts = set()

        for block in review_blocks_raw:
            text = block.get_text(strip=True)
            if text not in seen_texts:
                seen_texts.add(text)
                unique_reviews.append(block)

        actual_reviews = len(unique_reviews)
        duplicates_count = len(review_blocks_raw) - actual_reviews

        if reviews_limit is not None and actual_reviews < reviews_limit:
            print(f"Внимание: у товара всего {actual_reviews} уникальных отзывов, "
                  f"вместо запрошенных {reviews_limit}. Сохраняю всё, что есть.")
        else:
            print(f"Загружено {actual_reviews} уникальных отзывов.")
            
        if duplicates_count > 0:
            print(f"Пропущено дубликатов: {duplicates_count}")

        # Сохраняем страницу
        with open ("page.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        print('HTML-страница сохранена в файле page.html')
        
    finally:
        driver.quit()
        end_time = t.time()  #Окончание работы
        print(f"Парсинг отзывов выполнился за {round(end_time - start_time, 2)} секунд.")    
    
if __name__ == "__main__":
    main()