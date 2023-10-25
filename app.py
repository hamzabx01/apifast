from fastapi import FastAPI
from fastapi.responses import FileResponse
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json, os

app = FastAPI()

@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.get("/data/{id}")
def read_data(id: str):
  url = r'https://www.emploi-public.ma/ar/index.asp?p='
  start = 1
  data = []
  break_loop = False
  while True:
    response = requests.get(url + str(start))
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.select_one('body > main > div > div > div.card.mt-3.mb-3 > div > div > table > tbody')
    tr = table.find_all('tr')
    for i in tr:
      atag = i.select_one('td:nth-child(3) > a')
      datetag = i.select_one('td:nth-child(2)').text
      dateTody = datetime.now().strftime("%d/%m/%Y")
      datediff = datetime.strptime(dateTody, "%d/%m/%Y") - datetime.strptime(datetag, "%d/%m/%Y")
      if datediff.days == int(id):
        break_loop = True
        break
      data.append([datetag, atag.text, "https://www.emploi-public.ma/ar/" + atag['href']])
    if break_loop: break
    start += 1
    data.remove(data[-1])
  return data
