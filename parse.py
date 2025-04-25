from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time as t

def main():
    driver = webdriver.Chrome()
    driver.set_window_size(1600, 1080)
    driver.get("https://www.citilink.ru")
    t.sleep(1)
    tovar = input('Введите текст: ')
    tovar1 = tovar.replace('"', '').replace('\\', '')

    elem = driver.find_element(By.XPATH, "//input[@placeholder = 'Поиск по товарам']")
    elem.send_keys(tovar1)
    elem.send_keys(Keys.ENTER)
    t.sleep(2)
    elem = driver.find_element(By.XPATH, "//a[contains(@href, '/product/')]")
    elem.send_keys(Keys.ENTER)
    t.sleep(1)
    elem = driver.find_element(By.XPATH, "//a[contains(@href, '/otzyvy/')]")
    elem.send_keys(Keys.ENTER)
    t.sleep(2)
    actions = ActionChains(driver)
    while True:
        try:
            elem = driver.find_element(By.XPATH, "//button[span[text()='Показать ещё']]")
        except Exception as e:
            print('Элемент не найден, скорее всего, страница загружена полностью')
            break
        actions.move_to_element(elem).perform()
        t.sleep(1)
        elem.send_keys(Keys.ENTER)
        t.sleep(2)
    with open ("page.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    print('HTML-страница сохранена в файле page.html')
    if driver:
        driver.quit()
        
if __name__ == "__main__":
    main()