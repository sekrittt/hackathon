# from websearch import WebSearch as web

# for page in web('ООО "АГРОПЛАЗМА"').pages:
#     print(page)
import os, requests, re, validators, json
from bs4 import BeautifulSoup
import pandas as pd
from fuzzywuzzy import process
os.system('clear')

excel_1 = pd.read_excel('1. Компании.xlsx')
excel_2 = pd.read_excel('2. Продукты_new.xlsx')
excel_3 = pd.read_excel('3. Отрасли.xlsx')
excel_4 = pd.read_excel('4. Технологии.xlsx')

help_branch = pd.read_excel('Справочник. Отрасли и подотрасли.xlsx')
help_tech = pd.read_excel('Справочник. Технологии.xlsx')

cache = {}

with open('./cache.json', encoding='utf-8') as f:
    cache = json.loads(f)

def format_help_tech(d: pd.DataFrame):
    branches = {}
    for index, row in d.iterrows():
        if index == 0:
            continue

        if row[1] in branches:
            if row[3] in branches[row[1]]:
                branches[row[1]][row[3]].append(row[5])
                continue
            branches[row[1]][row[3]] = [
                    row[5]
                ]
            continue
        branches[row[1]] = {
                row[3]: [
                        row[5]
                    ]
                }
    return branches

def format_help_branches(d: pd.DataFrame):
    branches = {}
    for index, row in d.iterrows():
        if index == 0 or index == 1:
            continue

        if row[0] in branches:
            branches[row[0]].append(row[1])
            continue
        branches[row[0]] = [
                row[1]
            ]
    return branches

help_tech_formatted = format_help_tech(help_tech)
help_branch_formatted = format_help_branches(help_branch)

def get_text_from_site(url: str):
    try:

        site = requests.get(re.sub(r'https\:\/\/', 'http://', url))
        site.encoding = site.apparent_encoding
        html = BeautifulSoup(site.text, 'html.parser')

        text = re.sub(r'\s+', ' ', html.get_text())
        return text
    except Exception as e:
        return None

def check_techs(one, two, three):
    global help_tech_formatted
    if one in help_tech_formatted:
        if two in help_tech_formatted[one]:
            if three in help_tech_formatted[one][two]:
                return True
    return False
def check_branches(one, two):
    global help_branch_formatted
    if one in help_branch_formatted:
        if two in help_branch_formatted[one]:
            return True
    return False

def url_validate(url: str):
    if len(re.findall(r"^https?:\\/\\/(?:www\\.)?[-a-zA-Zа-яА-ЯёЁ0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Zа-яА-ЯёЁ0-9()@:%_\\+.~#?&\\/=]*)$", url)) > 0:
        return True
    if len(re.findall(r"^[-a-zA-Zа-яА-ЯёЁ0-9@:%._\\+~#=]{1,256}\\.[а-яА-ЯёЁa-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Zа-яА-ЯёЁ0-9()@:%_\\+.~#?&\\/=]*)$", url)) > 0:
        return True
    return False

def check_have_name_in_site(name: str, site_text: str):
    print(name)
    if name.lower() in site_text.lower():
        return True
    m = re.match(r'".+?"', name)
    if not m is None and m[0].lower() in site_text.lower():
        return True
    return False

result: dict[str, dict[str, str]] = {}
for index, row in excel_1.iterrows():
    if index == 0:
        continue
    site: str = row[7]
    # if not validators.url(site):
    r = {
        'valid_url': True,
        'valid_techs': True,
        'valid_branch': True,
        'site_is_available': True,
        'acc_desc': 0,
        'acc_name': 0,
        'have_name_in_site': False
    }
    if site.lower() == 'не указано' or site == 'н/д' or site == '-':
        print('Invalid url!', site)
        r['valid_url'] = False
    if not check_techs(row[4],row[5],row[6]):
        print('Invalid branches tech')
        r['valid_techs'] = False
    if not check_branches(row[2],row[3]):
        print('Invalid branches branch')
        r['valid_branch'] = False
    print(f'Processing company ({row[1]} {site})...')
    site_text = get_text_from_site(site)
    if site_text is None:
        r['site_is_available'] = False
    r['acc_desc'] = process.extractOne(row[8], [site_text])[1]
    r['acc_name'] = process.extractOne(row[1], [site_text])[1]
    r['have_name_in_site'] = check_have_name_in_site(row[1], site_text) if not site_text is None else False
    result[row[1]] = r
    print(f'Acc_Desc: {r["acc_desc"]}, Acc_Name: {r["acc_name"]}')

print(result)
