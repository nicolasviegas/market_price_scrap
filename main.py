import os
import datetime
import logging
import json
import time

import yaml
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome

coto = 'https://www.cotodigital3.com.ar/sitios/cdigi/'
dia = 'https://diaonline.supermercadosdia.com.ar/'


product = 'yerba canarias'
lista_productos = []

def search_product(chrome, market):
    # go to the main page
    chrome.get(market)

    if market == coto:
        logging.info("Mirando precios en el COTO")
        # wait until the page has loaded
        WebDriverWait(chrome, 5).until(EC.presence_of_element_located((By.ID, "formLimpiaSesion")))
        # set the email
        user_field = chrome.find_element('id', 'atg_store_searchInput')
        user_field.send_keys(product)

        chrome.find_element(By.ID, "atg_store_searchSubmit").click()

        WebDriverWait(chrome, 5).until(EC.presence_of_element_located((By.ID, "listview")))

        chrome.find_element(By.XPATH, './/span[@class="span_productName"]').click()

        WebDriverWait(chrome, 5).until(EC.presence_of_element_located((By.XPATH, './/span['
                                                                                 '@class="atg_store_productPrice"]')))

        for element in chrome.find_elements(By.XPATH, './/span[@class="atg_store_newPrice"]'):
            print(element.text)
            price = element.text
            if price != '':
                logging.info(f"El precio de {product} es: {price}")

        #logging.info("El precio de la yerba es:", price)
        #time.sleep(5)


def add_product_list():
    with open('lista.txt', 'r') as file:
        data = file.read()
        lista_productos.append(data)
        print(lista_productos)


def main(iters=0):
    logging.info("--------------------------------------------------------")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")

    service = Service(log_path='/dev/null')

    try:
        browser = Chrome(options=options, service=service)
    except Exception as e:
        logging.error(f'error while creating the browser: {e}')
        browser.quit()
        exit()

    try:
        #add_product_list()
        search_product(browser, coto)
    except TimeoutException:
        browser.quit()


if __name__ == "__main__":

    fmt = "%(asctime)s [%(threadName)s]: %(message)s"
    today = datetime.date.today()
    filename = today.strftime(f"{os.path.dirname(os.path.abspath(__file__))}/logs/%d_%m_%Y.log")
    logging.basicConfig(
        filename=filename,
        format=fmt,
        level=logging.INFO,
        datefmt="%H:%M:%S"
    )

    main()
   # login()