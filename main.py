import os.path
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
from pprint import pprint
import json
import codecs
from datetime import date

options = Options()
options.add_argument('start-maximized')
# options.add_argument('')

driver = webdriver.Chrome(options=options)

driver.get("https://www.wildberries.ru/")

# input = driver.find_element(By.XPATH, "//input[@id='searchInput']")
# https://www.wildberries.ru/catalog/173751665/detail.aspx?targetUrl=EX

time.sleep(2)
input = driver.find_element(By.ID, "searchInput")
input.send_keys("видеокарты")
input.send_keys(Keys.ENTER)
# time.sleep(2)

if os.path.exists("json_file.json"):
    if os.path.getsize('json_file.json'):
        with open("json_file.json", "r", encoding="utf8") as jsf:
            catalogs = json.load(jsf)
    else:
        catalogs = dict()
else:
    catalogs = dict()

while True:
    time.sleep(2)

    while True:
        wait = WebDriverWait(driver, timeout=30)
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article[@id]")))

        # time.sleep(0.1)
        # cards = driver.find_elements(By.XPATH, "//article[@id]") # 100
        print(len(cards))
        count = len(cards)
        driver.execute_script("window.scrollBy(0,2000)")
        time.sleep(1.5)
        cards = driver.find_elements(By.XPATH, "//article[@id]")
        if len(cards) == count:
            break

    # print(len(cards))
    # pprint(cards)
    for card in cards:
        # try:
        # price = card.find_element(By.XPATH, "//ins[@class='price__lower-price']").text
        url = card.find_element(By.XPATH, "./div/a").get_attribute('href')
        name = card.find_element(By.XPATH, "./div/a").get_attribute('aria-label')
        price =  card.find_element(By.CLASS_NAME, "price__lower-price").text.replace(" ","").strip()
        price, currency = int(price[:-1]) if price[:-1].isdigit() else price[:-1], price[-1]

        date_ = str(date.today())
        print(date_)

        # caralog = card.find_element(By.XPATH, "//a[@class='breadcrumbs__link']")
        # print(caralog)
        # TODO and GOTO
        # Traceback (most recent call last):
        #   File "main.py", line 58, in <module>
        #     caralog = card.find_element(By.CLASS_NAME, "breadcrumbs__link")
        #   File "venv\lib\site-packages\selenium\webdriver\remote\webelement.py", line 417, in find_element
        #     return self._execute(Command.FIND_CHILD_ELEMENT, {"using": by, "value": value})["value"]
        #   File "venv\lib\site-packages\selenium\webdriver\remote\webelement.py", line 395, in _execute
        #     return self._parent.execute(command, params)
        #   File "venv\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 347, in execute
        #     self.error_handler.check_response(response)
        #   File "venv\lib\site-packages\selenium\webdriver\remote\errorhandler.py", line 229, in check_response
        #     raise exception_class(message, screen, stacktrace)
        # selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".breadcrumbs__link"}
        #   (Session info: chrome=125.0.6422.113); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception

        min_str_fnd = "catalog/"
        max_str_fnd = "/detail.aspx"
        minr_id = url.rfind(min_str_fnd)+len(min_str_fnd)
        max_id = url.find(max_str_fnd)
        _id = int(url[minr_id:max_id])

        print(f"{_id = } {name = } {price = } {currency = } {url = }")

        # TODO AND GOTO ERROR
        try:
            if not catalogs[_id]:
                catalogs[_id] = {}
        except:
            catalogs[_id] = {}
        # TODO AND GOTO ERROR

        catalogs[_id] = {date_ : {"_id" : _id, "date" : date_, 'name': name, 'price': price, 'currency': currency, 'url': url}}
        # except Exception as e:
        #     print(e)

        # try:
        #     print(buttom.get_attribute("href"))
        # except Exception as e:
        #     print(e)

        if not os.path.exists("json_file.json"):
            open("json_file.json", "w", encoding="utf8")

        with open("json_file.json", "w", encoding="utf8") as jsf:
            # https://stackoverflow.com/questions/46080224/convert-python-escaped-unicode-sequences-to-utf-8
            jsf.write(json.dumps(catalogs, indent=4, ensure_ascii=False))



    try:
        # buttom = driver.find_element(By.CLASS_NAME, "paginator-next")
        button = driver.find_element(By.XPATH, "//a[@class='pagination-next pagination__next j-next-page']")
        button.click()
        # actions = ActionChains(driver)
        # actions.move_to_element(button).click()
        # actions.perform()
    except:
        break


print()