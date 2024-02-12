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
# Your JSON data
data = [
    {
      "name": "Braškių ir špinatų salotos",
      "ingredients": ["Braškės", "Ledinių salotų", "Dryžuotieji pomidorai"],
      "process": "Supjaustykite braškes ir pomidorus. Sumaišykite su plėšytomis ledinėmis salotų lapais. Padažui naudokite lengvą vyno acto ir aliejaus užpilą.",
      "cost": "5.97 EUR"
    },
    {
      "name": "Grilintos vištienos su keptomis daržovėmis",
      "ingredients": ["Vištienos ketvirčiai", "Brokolis", "Spalvotųjų paprikų mišinys", "Baklažanai", "Saldžiosios bulvės"],
      "process": "Grilinkite vištieną. Kepkite supjaustytas daržoves su alyvuogių aliejumi ir prieskoniais iki suminkštėjimo.",
      "cost": "10.65 EUR"
    },
    {
      "name": "Vegetariškas troškinys",
      "ingredients": ["Brokolis", "Baklažanai", "Dryžuotieji pomidorai", "Raudonosios saldžiosios paprikos"],
      "process": "Troškinkite daržoves keptuvėje su sojos padažu ir česnaku. Patiekite su rudaisiais ryžiais arba kinoą.",
      "cost": "7.64 EUR"
    },
    {
      "name": "Kepta lašiša su garintomis daržovėmis",
      "ingredients": ["Lašiša", "Brokolis", "Morkos", "Fenkelis"],
      "process": "Kepkite lašišos filė su citrina ir krapais. Garinkite brokolį, supjaustytas morkas ir fenkelį iki suminkštėjimo.",
      "cost": "Priklauso nuo lašišos kainos"
    },
    {
      "name": "Sveikos vištienos salotos",
      "ingredients": ["Vištienos ketvirčiai", "Ledinių salotų", "Obuoliai 'Granny Smith'", "Saliero stiebai"],
      "process": "Išvirkite ir suplėšykite vištieną. Sumaišykite su supjaustytomis salotomis, obuoliais ir salieru. Padažui naudokite graikišką jogurtą.",
      "cost": "6.18 EUR"
    },
    {
      "name": "Keptų burokėlių ir fetos sūrio salotos",
      "ingredients": ["Virti burokėliai", "Dryžuotieji pomidorai", "Ridikėliai", "Feta sūris"],
      "process": "Supjaustykite burokėlius ir ridikėlius. Sumaišykite su pomidorais ir sutrupintu feta sūriu. Padažui naudokite alyvuogių aliejų ir balzaminį actą.",
      "cost": "5.56 EUR"
    },
    {
      "name": "Kiaušinių ir špinatų pusryčių suktinukas",
      "ingredients": ["Rudi vištų kiaušiniai", "Švieži špinatai", "Viso grūdo suktinukai"],
      "process": "Išplakite kiaušinius ir sumaišykite su pakepintais špinatais. Patiekite viso grūdo suktinuke.",
      "cost": "3.37 EUR"
    },
    {
      "name": "Daržovių omletas",
      "ingredients": ["Rudi vištų kiaušiniai", "Švieži špinatai", "Saladžiųjų paprikų", "Svogūnų laiškai"],
      "process": "Iškepkite omletą iš kiaušinių, špinatų, supjaustytų saldžiųjų paprikų ir svogūnų laiškų. Patiekite su viso grūdo duona.",
      "cost": "3.57 EUR"
    },
    {
      "name": "Saldžiųjų bulvių ir avinžirnių karijus",
      "ingredients": ["Saldžiosios bulvės", "Konservuoti avinžirniai", "Svogūnai", "Konservuoti pomidorai"],
      "process": "Virinkite kubeliais supjaustytas saldžiąsias bulves, avinžirnius, svogūnus ir pomidorus su karijų prieskoniais. Patiekite su rudaisiais ryžiais.",
      "cost": "4.26 EUR"
    },
    {
      "name": "Obuolių ir riešutų salotos",
      "ingredients": ["Obuoliai 'Granny Smith'", "Riešutai", "Saliero stiebai", "Natūralus jogurtas"],
      "process": "Sumaišykite supjaustytus obuolius, riešutus ir salierą. Padažui naudokite natūralų jogurtą sumaišytą su trupučiu medaus.",
      "cost": "Priklauso nuo riešutų kainos"
    }
]

def get_image_url(query):
    url = rf'https://www.google.no/search?q={query}&client=opera&hs=cTQ&source=lnms&tbm=isch&sa=X&safe=active&ved=0ahUKEwig3LOx4PzKAhWGFywKHZyZAAgQ_AUIBygB&biw=1920&bih=982'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    page = requests.get(url, headers=headers).text
    soup = BeautifulSoup(page, 'html.parser')

    for raw_img in soup.find_all('img'):
        link = raw_img.get('src')
        if link and link.startswith("https://"):
            return link
        pass

doc_ref = db.reference("/maxima_recipes")
doc_ref.delete()
doc_ref = db.reference("/maxima_recipes")

# Add image URLs to your data
for recipe in data:
    image_url = get_image_url(recipe['name'])
    recipe['imageUrl'] = image_url
    doc_ref.push(recipe)
