from PIL import Image, ImageDraw, ImageFont
from telegram import Bot
import random
import string
import qrcode

def create_receipt(product_info):
    img = Image.new('RGB', (300, 600), color = 'white')
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
    fnt_big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
    d.text((img.width//2,10), "AresY3p Shop", font=fnt_big, fill=(0,0,0), anchor="mm")
    d.text((img.width//2,40), "SCONTRINO", font=fnt_big, fill=(0,0,0), anchor="mm")
    d.text((10,70), f"Nome prodotto: {product_info['name']}", font=fnt, fill=(0,0,0))
    d.text((10,90), f"Quantità: {product_info['quantity']}", font=fnt, fill=(0,0,0))
    d.text((10,110), f"Prezzo: {product_info['price']} euro", font=fnt, fill=(0,0,0))
    d.text((10,130), f"Metodo di pagamento: {product_info['payment_method']}", font=fnt, fill=(0,0,0))
    d.line((10,img.height//2+10,img.width-10,img.height//2+10), fill=(0,0,0), width=3)
    receipt_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    d.text((img.width//2,img.height//2+40), f"Codice {receipt_code}", font=fnt_big, fill=(0,0,0), anchor="mm")
    qr = qrcode.QRCode(version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4)
    qr.add_data(f"Nome prodotto: {product_info['name']}\nQuantità: {product_info['quantity']}\nPrezzo: {product_info['price']}\nMetodo di pagamento: {product_info['payment_method']}\nCodice di scontrino: {receipt_code}")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    img.paste(qr_img.resize((150,150)), (img.width//2-75,img.height-170))
    img.save('receipt.png')

def send_receipt_telegram(bot_token, chat_id):
    bot = Bot(bot_token)
    bot.send_photo(chat_id=chat_id, photo=open('receipt.png', 'rb'))

bot_token = 'qua metti il token del bot'
chat_id = 'qua metti l'id della persona/chat dove deve essere inviata la ricevuta'
product_name = input("Inserisci il nome del prodotto: ") 
product_quantity = int(input("Inserisci la quantità venduta: ")) 
product_price = float(input("Inserisci il prezzo del prodotto: ")) 
payment_method = input("Inserisci il metodo di pagamento: ")
product_info = {
    'name': product_name,
    'quantity': product_quantity,
    'price': product_price,
    'payment_method': payment_method
}
create_receipt(product_info)
send_receipt_telegram(bot_token, chat_id)

# NON MODIFICARE NULLA NEL CODICE (AMMENOCHè NON SAI QUELLO CHE FAI)
# CODICE CREATO INTERAMENTE DA @ARESY3P SU TELEGRAM
