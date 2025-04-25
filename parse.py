from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time as t

def main():
    start_time = t.time()
    options = ChromeOptions()
    options.add_argument("--headless=new")  
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.citilink.ru")

    driver.get_screenshot_as_file("screenshot2.png")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Поиск по товарам']")))
    
    tovar = input('Введите текст: ')
    tovar1 = tovar.replace('"', '').replace('\\', '')
    
    elem = driver.find_element(By.XPATH, "//input[@placeholder = 'Поиск по товарам']")
    elem.send_keys(tovar1)
    elem.send_keys(Keys.ENTER)
    
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/product/')]")))
    elem = driver.find_element(By.XPATH, "//a[contains(@href, '/product/')]")
    driver.execute_script("arguments[0].click();", elem)
    
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/otzyvy/')]")))
    elem = driver.find_element(By.XPATH, "//a[contains(@href, '/otzyvy/')]")
    driver.execute_script("arguments[0].click();", elem)
    
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[span[text()='Показать ещё']]")))
    while True:
        try:
            elem = driver.find_element(By.XPATH, "//button[span[text()='Показать ещё']]")
            driver.execute_script("arguments[0].click();", elem)  
            t.sleep(1) 
        except Exception:
            print("Элемент 'Показать ещё' не найден, все отзывы загружены.")
            break
    
    with open ("page.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    print('HTML-страница сохранена в файле page.html')
    driver.quit()
    
    end_time = t.time()  #Окончание работы
    print(f"Парсинг отзывов выполнился за {round(end_time - start_time, 2)} секунд.")    
    
if __name__ == "__main__":
    main()