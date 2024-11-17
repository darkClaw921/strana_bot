import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from pprint import pprint
load_dotenv()

BASE_URL=os.getenv('API_STRANA_URL')

@dataclass
class Endpoint:
    getAllCities:str='/v1/cities/list' #список всехипотечных программ в городе 
    getMortagageList:str='/v1/mortgages/list' #список всехипотечных программ в городе 
    getBestLoan:str='/v1/loan-offers/best/list' #лучшие предложения 

def get_all_cityes():
    url=BASE_URL+Endpoint.getAllCities
    cities=requests.get(url)
    # pprint(cities.json())
    return cities.json()

def get_mortgage_list(slugCity:str):
    url=BASE_URL+Endpoint.getMortagageList
    url+=f'?city={slugCity}'
    mortgage=requests.get(url)
    # pprint(mortgage.json())
    return mortgage.json()

def prepare_cities()->dict[str,str]:
    cities=get_all_cityes()
    citys={}
    for city in cities:
        slug=city['slug']
        citys[city['name']]=slug
    # pprint(citys)
    return citys

def prepare_mortgage(slugCity:str)->str:
    mortgages=get_mortgage_list(slugCity)
    mortText=''
    for mortgage in mortgages:
        mortText+=f"Название: {mortgage['name']}\n"
        mortText+=f"Ставка: {mortgage['rate']}%\n"
        mortText+=f"Период: {mortgage['creditPeriod']}\n"
        mortText+=f"Цена: {mortgage['creditAmount']:,}\n"

        tags=''
        for tag in mortgage['tags']:
                tags+=f"{tag['text']},\n"

        mortText+=f"Особенности: {tags}\n\n"

    # print(mortText)
    return mortText



if __name__ == '__main__':
    # get_all_cityes()
    # get_mortgage_list('tmn')
    # prepare_mortgage('spb')
    prepare_cities()