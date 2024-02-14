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
        "name": "Spaghetti Carbonara",
        "ingredients": ["spaghetti", "kiaulienos šoninė", "kiaušiniai", "parmezano sūris", "juodieji pipirai"],
        "process": "Išvirkite spaghetti. Kiaulienos šoninę apkepinkite, sumaišykite su kiaušiniais, parmezano sūriu ir pipirais. Sumaišykite su makaronais.",
        "average_cost": "5"
    },
    {
        "name": "Pizza Margherita",
        "ingredients": ["pica padas", "pomidorų padažas", "mozzarella sūris", "bazilikai", "alyvuogių aliejus"],
        "process": "Iškočiokite picos padą, patepkite pomidorų padažu, užberkite mozzarella sūriu, bazilikais ir aptilkite alyvuogių aliejumi. Kepkite 10-12 minučių.",
        "average_cost": "7"
    },
    {
        "name": "Paella",
        "ingredients": ["ryžiai", "vištienos gabaliukai", "jūros gėrybės", "žaliosios žirneliai", "raudonieji paprikos", "ciberžolė"],
        "process": "Vištieną ir jūros gėrybes apkepinkite, pridėkite ryžius, žaliuosius žirnelius, paprikas ir ciberžolę. Troškinkite iki ryžių suminkštėjimo.",
        "average_cost": "10"
    },
    {
        "name": "Lasagne",
        "ingredients": ["lasanjos lakštai", "malta mėsa", "pomidorų padažas", "bešamelio padažas", "parmezano sūris"],
        "process": "Kaitinkite orkaitę. Paruoškite maltos mėsos ir pomidorų padažą. Kiekvieną lasanjos sluoksnį patepkite mėsos padažu, bešamelio padažu ir parmezano sūriu. Kepkite 30 minučių.",
        "average_cost": "8"
    },
    {
        "name": "Bruschetta",
        "ingredients": ["batonas", "pomidorai", "česnakas", "bazilikai", "alyvuogių aliejus"],
        "process": "Batoną supjaustykite riekelėmis ir paskrudinkite. Ant viršaus dėkite smulkintus pomidorus, česnaką, bazilikus ir apšlakstykite alyvuogių aliejumi.",
        "average_cost": "4"
    },
    {
        "name": "Gazpacho",
        "ingredients": ["pomidorai", "agurkai", "žaliosios paprikos", "svogūnai", "česnakas", "alyvuogių aliejus", "balzaminis actas"],
        "process": "Visus ingredientus sutrinkite į vientisą masę. Atvėsinkite ir patiekite šaltą.",
        "average_cost": "6"
    },
    {
        "name": "Tiramisu",
        "ingredients": ["savoiardi sausainiai", "kava", "mascarpone sūris", "kiaušiniai", "cukrus", "kakava milteliai"],
        "process": "Sausainius pamirkykite kavoje. Sumaišykite mascarpone sūrį, kiaušinius ir cukrų. Sluoksniuokite sausainius ir kremą. Apibarstykite kakava.",
        "average_cost": "9"
    },
    {
    "name": "Spaghetti Carbonara",
    "ingredients": ["spaghetti", "kiaulienos šoninė", "kiaušiniai", "parmezano sūris", "juodieji pipirai"],
    "process": "Išvirkite spaghetti. Kiaulienos šoninę apkepinkite, sumaišykite su kiaušiniais, parmezano sūriu ir pipirais. Sumaišykite su makaronais.",
    "average_cost": "5"
  },
  {
    "name": "Pizza Margherita",
    "ingredients": ["pica padas", "pomidorų padažas", "mozzarella sūris", "bazilikai", "alyvuogių aliejus"],
    "process": "Iškočiokite picos padą, patepkite pomidorų padažu, užberkite mozzarella sūriu, bazilikais ir aptilkite alyvuogių aliejumi. Kepkite 10-12 minučių.",
    "average_cost": "7"
  },
  {
    "name": "Paella",
    "ingredients": ["ryžiai", "vištienos gabaliukai", "jūros gėrybės", "žaliosios žirneliai", "raudonieji paprikos", "ciberžolė"],
    "process": "Vištieną ir jūros gėrybes apkepinkite, pridėkite ryžius, žaliuosius žirnelius, paprikas ir ciberžolę. Troškinkite iki ryžių suminkštėjimo.",
    "average_cost": "10"
  },
  {
    "name": "Lasagne",
    "ingredients": ["lasanjos lakštai", "malta mėsa", "pomidorų padažas", "bešamelio padažas", "parmezano sūris"],
    "process": "Kaitinkite orkaitę. Paruoškite maltos mėsos ir pomidorų padažą. Kiekvieną lasanjos sluoksnį patepkite mėsos padažu, bešamelio padažu ir parmezano sūriu. Kepkite 30 minučių.",
    "average_cost": "8"
  },
  {
    "name": "Bruschetta",
    "ingredients": ["batonas", "pomidorai", "česnakas", "bazilikai", "alyvuogių aliejus"],
    "process": "Batoną supjaustykite riekelėmis ir paskrudinkite. Ant viršaus dėkite smulkintus pomidorus, česnaką, bazilikus ir apšlakstykite alyvuogių aliejumi.",
    "average_cost": "4"
  },
  {
    "name": "Gazpacho",
    "ingredients": ["pomidorai", "agurkai", "žaliosios paprikos", "svogūnai", "česnakas", "alyvuogių aliejus", "balzaminis actas"],
    "process": "Visus ingredientus sutrinkite į vientisą masę. Atvėsinkite ir patiekite šaltą.",
    "average_cost": "6"
  },
  {
    "name": "Tiramisu",
    "ingredients": ["savoiardi sausainiai", "kava", "mascarpone sūris", "kiaušiniai", "cukrus", "kakava milteliai"],
    "process": "Sausainius pamirkykite kavoje. Sumaišykite mascarpone sūrį, kiaušinius ir cukrų. Sluoksniuokite sausainius ir kremą. Apibarstykite kakava.",
    "average_cost": "9"
  },
  {
    "name": "Risotto",
    "ingredients": ["ryžiai", "svogūnai", "vyšniniai pomidorai", "baltasis vynas", "sultinys", "parmezano sūris"],
    "process": "Svogūnus ir pomidorus apkepinkite, įpilkite vyno. Pridėkite ryžius, sultinį ir troškinkite. Pabaigoje įmaišykite parmezano sūrį.",
    "average_cost": "7"
  },
  {
    "name": "Frittata",
    "ingredients": ["kiaušiniai", "pienas", "parmezano sūris", "svogūnai", "daržovės", "alyvuogių aliejus"],
    "process": "Išplakite kiaušinius su pienu ir parmezano sūriu. Svogūnus ir daržoves apkepinkite. Kiaušinių mišinį supilkite ant daržovių ir kepkite orkaitėje.",
    "average_cost": "6"
  },
  {
    "name": "Churros",
    "ingredients": ["miltai", "vanduo", "cukrus", "alyva", "cukrus", "cinamonas"],
    "process": "Miltus sumaišykite su vandeniu ir užvirkite. Formuokite churros ir kepkite alyvoje. Apibarstykite cukrumi ir cinamonu.",
    "average_cost": "5"
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
    recipe['id'] = str(uuid.uuid4())
    recipe['imageUrl'] = image_url
    doc_ref.push(recipe)
