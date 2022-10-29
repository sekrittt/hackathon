# from websearch import WebSearch as web

# for page in web('ООО "АГРОПЛАЗМА"').pages:
#     print(page)
import os, json
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
            if row[3] in branches[row[1]]['sub']:
                branches[row[1]]['sub'][row[3]]['sub'].append(row[5])
                continue
            branches[row[1]]['sub'][row[3]] = {
                'sub': [
                    row[5]
                ]
            }
            continue
        branches[row[1]] = {
            'sub': {
                row[3]: {
                    'sub': [
                        row[5]
                    ]
                }
            }
        }
    return branches
        

help_branch_formatted = format_help_tech(help_tech)

#print(help_branch_formatted)

