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

doc_ref = db.reference("/maxima")
doc_ref.delete()
doc_ref = db.reference("/maxima")

URL = "https://www.maxima.lt/akcijos"
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
r = requests.get(url=URL, headers=headers)
soup = BeautifulSoup(r.content, 'html5lib')
products = []
recipeProducts = []
sections = soup.find(
    'div', attrs={'data-offersfilter-target': 'offersWrapper'})

for section in sections.findAll('section'):
    productCategory = section.find('h2')
    category = " ".join(productCategory.text.split())
    for cards in section.findAll('div', attrs={'data-controller': 'offerCard'}):
        for card in cards:
            product = {}
            recipeProduct = {}
            if isinstance(card, Tag):
                product['id'] = str(uuid.uuid4())
                product['category'] = category
                recipeProduct['category'] = category
                productImage = card.find('img', attrs={'class': 'swiper-lazy'})
                product['imageUrl'] = productImage['data-src']
                productTitle = card.find(
                    'h4', attrs={'class': 'text-truncate'})
                product['title'] = " ".join(productTitle.text.split())
                recipeProduct['title'] = " ".join(productTitle.text.split())
                priceEur = card.find('div', attrs={'class': 'price-eur'})
                priceCents = card.find('span', attrs={'class': 'price-cents'})
                # if len(priceEur) != 0 and len(priceCents) != 0:
                product['priceEur'] = priceEur.text
                recipeProduct['priceEur'] = priceEur.text
                product['priceCents'] = priceCents.text

                dateTo = card.find(
                    'p', attrs={'class': 'offer-dateTo-wrapper'})
                product['dateTo'] = " ".join(dateTo.text.split())

                xIcons = card.findAll('img', attrs={'class': 'x-icon'})
                if xIcons:
                    product['xIcons'] = len(xIcons)

                discount = card.find('div', attrs={'class': 'discount-icon'})
                product['discount'] = " ".join(discount.text.split())

                specifics = card.find(
                    'div', attrs={'class': 'offer-bottom-icon-wrapper'})

                specImg = specifics.find('img')
                if specImg != None:
                    options = {}
                    options['market'] = 'maxima'
                    if specImg.attrs['title'] == 'AČIŪ':
                        options['spec'] = 'card'
                    else:
                        options['spec'] = 'mobile'
                    product['specImg'] = options

                try:
                    priceOld = card.find('div', attrs={'class': 'price-old'})
                    if (priceOld != None):
                        product['oldPrice'] = " ".join(priceOld.text.split())
                except NameError:
                    print()

                products.append(product)
                recipeProducts.append(recipeProduct)
                doc_ref.push(product)

json_object = json.dumps(recipeProducts, ensure_ascii=False, indent=2)
with open('maxima-recipes-data.json', 'w', encoding='utf-8') as f:
    f.write(json_object)
