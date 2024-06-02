import os
import json
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(options=options)
driver.get("https://www.wildberries.ru/")

time.sleep(2)
input_element = driver.find_element(By.ID, "searchInput")
input_element.send_keys("видеокарты")
input_element.send_keys(Keys.ENTER)

json_file = "json_file.json"
if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
    with open(json_file, "r", encoding="utf8") as jsf:
        catalogs = json.load(jsf)
else:
    catalogs = {}

def parse_and_save_data(cards):
    print("Переходим к собиранию и сохранению")
    for card in cards:
        try:
            url = card.find_element(By.XPATH, "./div/a").get_attribute('href')
            name = card.find_elemen (By.XPATH, "./div/a").get_attribute('aria-label')
            price_text = card.find_element(By.CLASS_NAME, "price_lower-price").text.replace(" ", "").strip()
            price, currency = int(price_text[:-1]), price_text[-1]
            date = str(datetime.date.today())
            min_str_fnd = "catalog/"
            max_str_fnd = "/detail.aspx"
            minr_id = url.rfind(min_str_fnd) + len(min_str_fnd)
            max_id = url.find(max_str_fnd)
            id = int(url[minr_id:max_id])
            if id not in catalogs:
                catalogs[id] = {}
            catalogs[id][date] = {"_id": id, "date": date, 'name': name, 'price': price, 'currency': currency, 'url': url}
        except Exception as e:
            print(f"Error processing card: {e}")
    with open(json_file, "w", encoding="utf8") as jsf:
        json.dump(catalogs, jsf, indent=4, ensure_ascii=False)

print("Начинаем обрабатывать сайт")
while True:
    try:
        wait = WebDriverWait(driver, 30)
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article[@id]")))

        last_count = 0
        while True:
            current_count = len(cards)
            driver.execute_script("window.scrollBy(0, 2000)")
            time.sleep(1.5)
            cards = driver.find_elements(By.XPATH, "//article[@id]")
            if len(cards) == last_count:
                break
            last_count = current_count

        parse_and_save_data(cards)

        try:
            next_button = driver.find_element(By.XPATH, "//a[@class='pagination-next pagination__next j-next-page']")
            next_button.click()
            time.sleep(2)
        except Exception as e:
            print("No more pages or next button not found:", e)
            break

    except Exception as e:
        print("Error during main loop:", e)
        break

driver.quit()