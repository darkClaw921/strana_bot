import requests
from dotenv import load_dotenv
import os
import hashlib
import time
import random
import string
import logging
load_dotenv()
graphQL=os.getenv('GRAPHQL')
SECRET_KEY=os.getenv('SECRET_KEY')
# print(f'{SECRET_KEY=}')

# URL вашего GraphQL API
url = graphQL
# print(f'{url=}')
from pprint import pprint
# Функция для выполнения GraphQL запроса
# Функция для генерации заголовков запроса
# Настройки
import json

def signat():
    secret_key = SECRET_KEY
    version_header = "2.49.0"
    timestamp = int(time.time())
    
    # Вычисляем salt
    combined = f"{secret_key}{version_header}"
    salt = hashlib.md5(combined.encode()).hexdigest()
    
    # Вычисляем подпись
    value_string = f"{salt}{url}/{timestamp}"
    signature = hashlib.md5(value_string.encode()).hexdigest()
    
    # Формируем заголовки
    headers = {
        "X-Version": version_header,
        "X-Qrator-Hash": signature,
        "X-Qrator-Timestamp": str(timestamp),
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cookie": f"qrator_jsid={salt}"
    }
    
    # print("Generated headers:")
    # pprint(headers)
    return headers


def execute_query(query:str, variables=None):
    headers= signat()
    # data=query.encode()
    # response = requests.post(url+'/', headers=headers,json={'query': query, 'variables': variables,} )
    # print(f'{query=}')
    # print(f'{variables=}')

    json_data = {
        'query':query,
        'variables': variables,
        'operationName': 'getLayoutsList',
    }

    # response = requests.post(url+'/', headers=headers, json={'query': query, 'variables': variables,}, data=data)
    response = requests.post(url+'/', 
                             headers=headers, 
                             json=json_data)
    # jsonData={'query': query}
    # pprint(json.dumps(jsonData))
    # response = requests.post(url+'/', headers=headers,  data=json.dumps(jsonData))

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Запрос для получения списка планировок с параметрами
# get_layouts_list_query = '''query getLayoutsList(
get_layouts_list_query = '''query getLayoutsList(
    $first: Int,
    $after: String,
    $fullFinalPriceMin: String,
    $fullFinalPriceMax: String,
    $areaMin: String,
    $areaMax: String,
    $floorMin: String,
    $floorMax: String,
    $completionDate: [String],
    $building: [ID],
    $project: [ID],
    $section: [ID],
    $rooms: [ID],
    $action: Boolean,
    $orderBy: String,
    $isFavorite: Boolean,
    $orderRandom: Boolean,
    $city: ID,
    $id: [ID],
    $article: String,
    $features: [ID],
    $specialOffers: [ID],
    $andSpecialOffers: [ID],
    $specialOffersPanel: [ID],
    $actions: String,
    $orderMostExpensive: Boolean,
    $minMortgageMin: String,
    $minMortgageMax: String,
    $windowViewProfitbase: [ID],
    $number: String,
    $offset: Int,
    
) {
    result: allLayouts(
        first: $first,
        after: $after,
        fullFinalPriceMin: $fullFinalPriceMin,
        fullFinalPriceMax: $fullFinalPriceMax,
        areaMin: $areaMin,
        areaMax: $areaMax,
        floorMin: $floorMin,
        floorMax: $floorMax,
        completionDate: $completionDate,
        building: $building,
        project: $project,
        section: $section,
        rooms: $rooms,
        action: $action,
        order: $orderBy,
        isFavorite: $isFavorite,
        orderRandom: $orderRandom,
        city: $city,
        id: $id,
        article: $article,
        features: $features,
        specialOffers: $specialOffers,
        andSpecialOffers: $andSpecialOffers,
        specialOffersPanel: $specialOffersPanel,
        actions: $actions,
        orderMostExpensive: $orderMostExpensive,
        minMortgageMin: $minMortgageMin,
        minMortgageMax: $minMortgageMax,
        windowViewProfitbase: $windowViewProfitbase,
        number: $number,
        offset: $offset,
        
    ) {
        totalCount
        edges {
            node {
                id
                pk
                status
                article
                name
                number
                type
                area
                rooms
                isEuroLayout
                flatsCountMoreThan
                flatCount
                minFlatPriceAfterFiltering
                fullFinalPrice
                originalPrice
                layoutDiscountSize
                maxDiscount
                flatSold
                planPngPreview
                planHover
                minFloorPlan
                plan
                minFloor
                maxFloor
                project {
                    id
                    address
                    detailProjectId
                    name
                    slug
                    templateType
                    isReplacePrice
                    replacedPrice
                    hidePriceFromBroker
                    isSoon
                    startSales
                    findOutPrice
                    city {
                        id
                        slug
                        name
                    }
                    transport {
                        name
                    }
                    transportTime
                }
                building {
                    id
                    name
                    nameDisplay
                    buildingState
                    builtYear
                    readyQuarter
                    currentLevel
                    windowViewPlanLotDisplay
                    windowViewPlanLotPreview
                }
                floor {
                    plan
                    planWidth
                    planHeight
                    number
                }
                windowView {
                    ppoi
                    windowviewangleSet {
                        angle
                    }
                }
                features {
                    name
                }
                specialOffers {
                    id
                    name
                    badgeLabel
                    color
                }
            }
        }
        pageInfo {
            startCursor
            endCursor
            hasNextPage
            hasPreviousPage
        }
    }
}'''

# Пример параметров для запроса
variables = {
    # "first": 10,
    # "after": None,
    # "fullFinalPriceMin": "1000000",
    # "fullFinalPriceMax": "5000000",
    "areaMin": "1",
    "areaMax": "350",
    # "name": "СС-ГП3.E3.17.7",
    # "floorMin": "1",
    # "floorMax": "10",
    # "completionDate": ["2023-01-01", "2023-12-31"],
    # "building": ["building_id_1", "building_id_2"],
    # "project": ["project_id_1"],
    # "section": ["section_id_1"],
    # "rooms": ["room_id_1"],
    # "action": True,
    # "orderBy": "fullFinalPrice",
    # "isFavorite": False,
    # "orderRandom": False,
    # "city": "city_id",
    # # "id": ["layout_id_1"],
    # "article": "some_article",
    # "features": ["feature_id_1"],
    # "specialOffers": ["special_offer_id_1"],
    # "andSpecialOffers": ["and_special_offer_id_1"],
    # "specialOffersPanel": ["special_offer_panel_id_1"],
    # "actions": "some_action",
    # "orderMostExpensive": False,
    # "minMortgageMin": "500000",
    # "minMortgageMax": "2000000",
    # "windowViewProfitbase": ["window_view_id_1"],
    # "number": "some_number",
    # "offset": 0,
}

# Выполнение запроса и вывод результатов
def get_layouts_list():
    
    layouts = execute_query(get_layouts_list_query, variables=variables)['data']['result']['edges']
    return layouts

def get_all_layouts_list():
    all_layouts = []
    has_next_page = True
    after_cursor = None

    while has_next_page:
        # Обновляем переменные для следующего запроса
        variables['after'] = after_cursor
        layouts = execute_query(get_layouts_list_query, variables=variables)['data']['result']
        
        all_layouts.extend(layouts['edges'])
        has_next_page = layouts['pageInfo']['hasNextPage']
        after_cursor = layouts['pageInfo']['endCursor']  # Получаем курсор для следующей страницы
        print(has_next_page)
        print(after_cursor)
        print(len(all_layouts))
        

    return all_layouts

def prepare_to_dict_from_layouts(layouts:dict):
    # layouts = get_layouts_list()
    pprint(layouts)
    
    layoutsOut = []
    for layout in layouts:
        tempLayouts = {}
        layout = layout['node']
        tempLayouts['area']=layout['area']
        tempLayouts['rooms']=layout['rooms']
        tempLayouts['fullFinalPrice']=layout['fullFinalPrice']
        tempLayouts['originalPrice']=layout['originalPrice']
        tempLayouts['layoutDiscountSize']=layout['layoutDiscountSize']
        tempLayouts['maxDiscount']=layout['maxDiscount']
        tempLayouts['planPngPreview']=layout['planPngPreview']
        
        #две ванные?
        tempLayouts['features']=[feat['name'] for feat in layout['features']]
        #специальные предложения 
        tempLayouts['specialOffers']=[spec['name'] for spec in layout['specialOffers']]

        tempLayouts['adress']=layout['project']['address']
        tempLayouts['city']=layout['project']['city']['name']
        tempLayouts['name']=layout['project']['name']
        # pprint(tempLayouts)
        layoutsOut.append(tempLayouts)
    return layoutsOut


def layouts_to_text(layouts1:list[dict]):
    text = ""
    for layouts in layouts1:
        text += f"Планировка {layouts['name']} в {layouts['city']}, {layouts['adress']}:\n"
        text += f"Площадь: {layouts['area']} кв.м\n"
        text += f"Количество комнат: {layouts['rooms']}\n"
        text += f"Цена: {layouts['fullFinalPrice']} руб.\n"
        text += f"Цена без скидки: {layouts['originalPrice']} руб.\n"
        text += f"Размер скидки: {layouts['layoutDiscountSize']} руб.\n"
        text += f"Максимальная скидка: {layouts['maxDiscount']} руб.\n"
        text += f"Ссылка на планировку: {layouts['planPngPreview']}\n"
        text += f"Особенности: {', '.join(layouts['features'])}\n"
        text += f"Специальные предложения: {', '.join(layouts['specialOffers'])}\n"
        text += "==========\n"
    
    return text 

def get_layouts_text():
    # layoutsList=get_layouts_list()
    layoutsList=get_all_layouts_list()
    layouts = prepare_to_dict_from_layouts(layouts=layoutsList)
    
    text = layouts_to_text(layouts)
    return text

if __name__ == "__main__":
    text = get_layouts_text()
    with open('layouts.txt', 'w') as f:
        f.write(text)
    print(text)
# try:
#     layouts = execute_query(get_layouts_list_query, variables=variables)
#     print("Layouts List:", layouts)
#     pprint(layouts)
# except Exception as e:
#     print(e)