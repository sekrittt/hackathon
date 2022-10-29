# from websearch import WebSearch as web

# for page in web('ООО "АГРОПЛАЗМА"').pages:
#     print(page)
import os, requests, re
from bs4 import BeautifulSoup
import pandas as pd
os.system('clear')

excel_1 = pd.read_excel('1. Компании.xlsx')
excel_2 = pd.read_excel('2. Продукты_new.xlsx')
excel_3 = pd.read_excel('3. Отрасли.xlsx')
excel_4 = pd.read_excel('4. Технологии.xlsx')

help_branch = pd.read_excel('Справочник. Отрасли и подотрасли.xlsx')
help_tech = pd.read_excel('Справочник. Технологии.xlsx')

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

        if row[1] in branches:
            branches[row[1]].append(row[3])
            continue
        branches[row[1]] = [
                row[3]
            ]
    return branches
        
help_tech_formatted = format_help_tech(help_tech)
help_branch_formatted = format_help_branches(help_branch)

def get_text_from_site(url: str):
    site = requests.get(url)
    site.encoding = site.apparent_encoding
    html = BeautifulSoup(site.text, 'html.parser')

    text = re.sub(r'\s+', ' ', html.get_text())
    return text

for index, row in excel_1.iterrows():
    if index == 0:
        continue
    site = row[7]
    if 