import requests
import json
import html5lib
import uuid
from bs4 import BeautifulSoup, Tag
import firebase_admin
from firebase_admin import credentials, db
import validators

cred = credentials.Certificate(
    # Windows
    # "C:\\Users\\tager\\Desktop\\scrap\\service-key.json"
    # MAC
    "/Users/vaidas/Documents/scrape/service-key.json"
)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://akcijoslt-8862e-default-rtdb.europe-west1.firebasedatabase.app/'
})

doc_ref = db.reference("/lidl")
doc_ref.delete()
doc_ref = db.reference("/lidl")

lidlUrl = 'https://www.lidl.lt'
URL = "https://www.lidl.lt/c/visos-sios-savaites-akcijos/a10025491?channel=store&tabCode=Current_Sales_Week"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
r = requests.get(url=URL, headers=headers)
soup = BeautifulSoup(r.content, 'html5lib')
products = []
unique_sweets = []
soupList = soup.findAll('div', attrs={'class': 'ATheHeroStage__TabPanels'})
sectionTag = soupList[0].findAll('section')

for navLink in sectionTag[0].findAll('div', attrs={'class': 'ATheHeroStage__Offer'}):
    l = navLink.find('a')
    link = l['href']
    valid = validators.url(link)
    if valid == True:
        continue
    else:
        newLink = lidlUrl + link
        request = requests.get(url=newLink, headers=headers)

    soupIn = BeautifulSoup(request.content, 'html5lib')

    for section in soupIn.findAll('section', attrs={'data-selector': 'GRID'}):
        
        additionalTitle = l.find(
            'strong', attrs={'class': 'ATheHeroStage__Headline'})
        category = section.find(
            'li', attrs={'class': 'ACampaignGrid__item--for-two'})
        categoryName = ''
        if isinstance(category, Tag):
            categoryTitle = category.find(
                'h2', attrs={'class', 'ATape__Headline'})
            if categoryTitle:
                categoryName = " ".join(categoryTitle.text.split())
            else:
                categoryName = " ".join(additionalTitle.text.split())

        else:
            categoryName = " ".join(
                additionalTitle.text.split())

        for cardProduct in section.findAll('li', attrs={'class': 'ACampaignGrid__item--product'}):
            if isinstance(cardProduct, Tag):
                product = {}
                # product['id'] = str(uuid.uuid4())
                product['category'] = categoryName
                data = cardProduct.find(
                    'div', attrs={'class': 'detail__grids'})
                parsedData = json.loads(data['data-grid-data'])
                # print(json.dumps(parsedData, indent=4))
                product['imageUrl'] = parsedData[0]['image']
                product['title'] = parsedData[0]['fullTitle']
                if parsedData[0]['ribbons']:
                    product['dateTo'] = parsedData[0]['ribbons'][0]['text']
                else:
                    product['dateTo'] = ''
                # description
                if parsedData[0]['price']['basePrice'] is None:
                    product['description'] = ''
                else:
                    product['description'] = parsedData[0]['price']['basePrice']['text']
                # discount
                if parsedData[0]['price']['discount'] is None:
                    product['discount'] = ''
                else:
                    product['discount'] = parsedData[0]['price']['discount']['discountText']
                # old price
                if parsedData[0]['price']['oldPrice'] is None:
                    product['oldPrice'] = ''
                else:
                    product['oldPrice'] = str(parsedData[0]['price']['oldPrice'])
                # current price
                if parsedData[0]['price']['price'] is None:
                    product['priceEur'] = ''
                else:
                    product['priceEur'] = str(parsedData[0]['price']['price'])

                products.append(product)
                doc_ref.push(product)


# this is for creating JSON file.
# json_object = json.dumps(products, ensure_ascii=False, indent=2)
# with open('lidl.json', 'w', encoding='utf-8') as f:
#     f.write(json_object)
