from flask import Flask
from telegram import Bot
import requests
from bs4 import BeautifulSoup
import asyncio

app = Flask(__name__)


# Reemplaza 'TOKEN' con el token de tu bot
bot_token = '5886565362:AAGsgna7zxL6NnX1Q1YlpWZEoeowOgv8cro'

# Crea una instancia del bot
bot = Bot(token=bot_token)

# Reemplaza 'CHAT_ID' con el chat_id del destinatario
chat_id = '1060503116'
url_apple = 'https://www.falabella.com/falabella-cl/category/cat40052/Computadores?facetSelected=true&f.product.brandName=apple' 
url_tecnologia = 'https://www.falabella.com/falabella-cl/category/cat7090034/Tecnologia' 
page_count = 10

@app.route('/ofertas', methods=['GET'])
def enviar_mensaje():
    async def process_pages(url):
        for page in range(1, page_count + 1):
            page_url = f'{url}?page={page}' if page > 1 else url
            response = requests.get(page_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            texto_buscar=''
            clase_buscar='discount-badge-item'
            descuentos = soup.find_all(class_='jsx-200723616 search-results-4-grid grid-pod') 
            precios = soup.find_all(class_='prices-0') #prices-0
            for descuento in descuentos:
                html =f"<html><body> {descuento} </body></html>"
                soup_descuento = BeautifulSoup(html, 'html.parser')
                elemento = soup_descuento.find(class_='discount-badge-item')
                if elemento is not None:
                    porcentaje_descuento=elemento.text.replace('%','').replace('-','')
                    if texto_buscar in descuento.text:
                        if int(porcentaje_descuento) > 60:
                            print(f'{descuento.text}  ')
                            chat_id = '-1001971382154'
                            await bot.send_message(chat_id=chat_id, text=descuento.text) 

    asyncio.run(process_pages(url_tecnologia))
    asyncio.run(process_pages(url_apple))

    return 'Mensajes enviados'

if __name__ == '__main__':
    app.run()
