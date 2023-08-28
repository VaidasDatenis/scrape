import requests
import uuid
import json
import html5lib
from bs4 import BeautifulSoup, Tag
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate(
    "C:\\Users\\tager\\Desktop\\scrap\\service-key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://akcijoslt-8862e-default-rtdb.europe-west1.firebasedatabase.app/'
})
doc_ref = db.reference("/rimi")
# firestore_client = firestore.client()
# doc_ref = firestore_client.collection("rimi")
URL = "https://www.rimi.lt/e-parduotuve/lt/akcijos?page={}&pageSize=80"
rimiUrl = "https://www.rimi.lt"
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

filename = "rimi.json"
f = open(filename, "w", encoding='utf-8')

pagenum = 0
while True:
    pagenum += 1
    if pagenum == 35:
        break
    print(pagenum)
    r = requests.get(url=URL.format(pagenum), headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    products = []
    cards = soup.findAll('li', attrs={'class': 'product-grid__item'})
    for card in cards:
        product = {}
        if isinstance(card, Tag):
            product['id'] = str(uuid.uuid4())
            cardTitle = card.find(
                'div', attrs={'class': 'js-product-container'})
            product['title'] = cardTitle.get('data-gtms-banner-title')
            cardLink = card.find(
                'a', attrs={'class': 'card__url js-gtm-eec-product-click'})
            productLink = cardLink.get('href')
            rimiLink = rimiUrl+productLink
            linkRequest = requests.get(url=rimiLink, headers=headers)
            linkSoup = BeautifulSoup(linkRequest.content, 'html5lib')
            container = linkSoup.find(
                'div', attrs={'class': 'section-header__container'})
            if container:
                containerLink = container.findAll('a')
                product['category'] = " ".join(containerLink[0].text.split())
            cardImg = card.find('img')
            product['imageUrl'] = cardImg.get('src')
            cardPriceMain = card.find(
                'div', attrs={'class': 'price-tag card__price'})
            if cardPriceMain:
                cardPrice = cardPriceMain.find('span')
                cardCents = cardPriceMain.find('div')
                product['priceEur'] = cardPrice.text
                product['priceCents'] = " ".join(cardCents.text.split())
            try:
                cardOldPrice = card.find(
                    'div', attrs={'class': 'old-price-tag card__old-price'})
                if (cardOldPrice != None):
                    product['oldPrice'] = " ".join(
                        cardOldPrice.text.split())
            except NameError:
                print()

            cardSpecImgHeader = card.find(
                'div', attrs={'class': 'price-badge__header'})
            if cardSpecImgHeader != None:
                product['discount'] = " ".join(
                    cardSpecImgHeader.text.split())
                img = cardSpecImgHeader.find('img')
                if img:
                    product['specImg'] = img.get('src')
            cardSpecImgBody = card.find(
                'div', attrs={'class': 'price-badge__body'})
            if cardSpecImgBody != None:
                options = {}
                options['market'] = 'rimi'
                img = cardSpecImgBody.find('img')
                if img:
                    options['spec'] = 'card'
                # fix
                product['specImg'] = options
                cardBodyPrice = cardSpecImgBody.find(
                    'div', attrs={'class': 'price-badge__price'})
                cardPrice = cardBodyPrice.find('span')
                cardCents = cardBodyPrice.find('div')
                product['priceEur'] = cardPrice.text
                product['priceCents'] = " ".join(cardCents.text.split())

            cardDateTo = linkSoup.find('p', attrs={'class': 'notice'})
            if cardDateTo != None:
                product['dateTo'] = " ".join(cardDateTo.text.split())

            doc_ref.push(product)
            # json_object = json.dumps(product, ensure_ascii=False, indent=2)
            # with open(filename, "a", encoding='utf-8') as f:
            #     f.write(json_object + ",")
