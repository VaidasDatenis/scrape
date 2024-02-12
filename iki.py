import requests
import json
import uuid
import html5lib
from bs4 import BeautifulSoup, Tag
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate(
    # Windows
    # "C:\\Users\\tager\\Desktop\\scrap\\service-key.json"
    # MAC
    "/Users/vaidas/Documents/scrape/service-key.json"
)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://akcijoslt-8862e-default-rtdb.europe-west1.firebasedatabase.app/'
})

doc_ref = db.reference("/iki")
doc_ref.delete()
doc_ref = db.reference("/iki")

URL = "https://iki.lt/akcijos/savaites-akcijos/"
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
r = requests.get(url=URL, headers=headers)
soup = BeautifulSoup(r.content, 'html5lib')
products = []
sections = soup.find('div', attrs={'data-content': 'filter-categories'})
links = sections.findAll('a', attrs={'class', 'cursor-pointer'})
# print('1 --- ', links)
for link in links:
    linkCategory = link.find('span')
    print(" ".join(linkCategory.text.split()))
    # print('2 --', link)
    # print(link.attrs['href'])
    linkUrl = link.attrs['href']
    # print('3 url --- ', linkUrl)
    linkRequest = requests.get(url=linkUrl, headers=headers)
    linkSoup = BeautifulSoup(linkRequest.content, 'html5lib')
    cards = linkSoup.findAll(
        'div', attrs={'class': 'tag_class-savaites-akcijos'})
    for card in cards:
        if isinstance(card, Tag):
            product = {}
            product['id'] = str(uuid.uuid4())
            product['category'] = " ".join(linkCategory.text.split())
            cardTitle = card.find('p', attrs={'class': 'akcija_title'})
            product['title'] = " ".join(cardTitle.text.split())
            cardDescription = card.find('p', attrs={'class': 'akcija_description'})
            product['description'] = " ".join(cardDescription.text.split())
            cardImg = card.find('img', attrs={'class': 'card-img-top webpexpress-processed'})
            if cardImg['src'] is not None:
                product['imageUrl'] = cardImg['src']
            else:
                product['imageUrl'] = 'https://e7.pngegg.com/pngimages/829/733/png-clipart-logo-brand-product-trademark-font-not-found-logo-brand.png'
            cardPromo = card.find(
                'div', attrs={'class': 'promo_price'})
            if isinstance(cardPromo, Tag):
                options = {}
                promoCard = card.find(
                    'div', attrs={'class': 'promo_price_tag tag_iki-premija'})
                options['market'] = 'iki'
                options['spec'] = 'card'
                product['specImg'] = options

            cardDiscount = card.find(
                'div', attrs={'class': 'promo_price_meta'})
            if isinstance(cardDiscount, Tag):
                product['discount'] = " ".join(cardDiscount.text.split())
            cardMain = card.find('div', attrs={'class': 'promo_price_main'})
            if isinstance(cardMain, Tag):
                cardPrice = cardMain.find('span', attrs={'class': 'main'})
                cardCents = cardMain.find('span', attrs={'class': 'sub'})
                product['priceEur'] = cardPrice.text
                product['priceCents'] = cardCents.text
            cardDate = card.find(
                'p', attrs={'class': 'm-0 w-100 akcija_description text-center'})
            product['dateTo'] = " ".join(cardDate.text.split())
            cardOld = card.find('div', attrs={'class': 'promo_price_old'})
            if isinstance(cardOld, Tag):
                cardPriceOld = cardOld.find('span', attrs={'class': 'main'})
                cardCentsOld = cardOld.find('span', attrs={'class': 'sub'})
                product['oldPrice'] = "%s, %s" % (
                    cardPriceOld.text, cardCentsOld.text)

            products.append(product)
            doc_ref.push(product)


# this is for creating JSON file.
# json_object = json.dumps(products, ensure_ascii=False, indent=2)
# with open('iki.json', 'w', encoding='utf-8') as f:
#     f.write(json_object)
