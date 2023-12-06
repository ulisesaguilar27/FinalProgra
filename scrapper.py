import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrapper_ofertas(num_paginas=6):
    s = Service(ChromeDriverManager().install())
    opc = Options()
    opc.add_argument("--window-size=1020,1200")
    url = "https://www.mercadolibre.com.mx/ofertas?container_id=MLM779363-1#origin=qcat&filter_position=1"

    datos = {"Nombre": [], "Precio": [], "Descuento": [],"Tipo":[],"Envio":[]}

    navegador = webdriver.Chrome(service=s, options=opc)

    for pagina in range(1,num_paginas + 1):
        navegador.get(url)

        time.sleep(5)
        soup = BeautifulSoup(navegador.page_source, 'html.parser')
        productos = soup.find_all("div", attrs={"class": "promotion-item__description"})


        for producto in productos:
            nombre = producto.find("p", attrs={"class": 'promotion-item__title'})
            precio = producto.find("span",attrs ={"class": 'andes-money-amount__fraction'})
            descuento = producto.find("span", attrs={"class": 'promotion-item__discount-text'})
            tipo = producto.find("span",attrs={"class":'promotion-item__today-offer-text'})
            envio = producto.find("span", attrs={"class": 'promotion-item__pill'})


            datos["Nombre"].append(nombre.text.strip() if nombre else "")
            datos["Precio"].append(precio.text.strip() if precio else "")
            datos["Descuento"].append(descuento.text.strip() if descuento else "")
            datos["Tipo"].append(tipo.text.strip() if tipo else "Regular")
            datos["Envio"].append(envio.text.strip() if envio else "Envio Regular")

        if pagina < num_paginas:
            li = navegador.find_element(By.CLASS_NAME, "andes-pagination__button.andes-pagination__button--next")
            next_page_button = li.find_element(By.TAG_NAME, "a")
            url = next_page_button.get_attribute("href")
            #next_page_button = navegador.find_element(By.XPATH, "//li[@class='andes-pagination__button.andes-pagination__button--next']")
            #next_page_button.click()
        else:
            break

    dataDf = pd.DataFrame(datos)
    dataDf.to_csv("datasets/mercado.csv")
