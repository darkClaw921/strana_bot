from datetime import datetime
import json
from pprint import pprint

import aiohttp
from dotenv import load_dotenv
import os
from workGS import Sheet
from workRedis import add_message_to_history, get_history, clear_history    
import re
import postgreWork 
import apiStrana
from difflib import SequenceMatcher

sheet=Sheet('5f6f677a3cd8.json','test_promts','Лист1')
load_dotenv()

PORT_GENERATE_ANSWER=os.getenv('PORT_GENERATE_ANSWER')
IP_SERVER = os.getenv('IP_SERVER')
GENERATE_ANSWER_URL=os.getenv('GENERATE_ANSWER_URL')
SENDER_MESSAGE_URL=os.getenv('SENDER_MESSAGE_URL')

triggers=sheet.get_all_triggers()
CITIES_SLUG=apiStrana.prepare_cities()


USER_LIST={}
async def request_data(url, json):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,json=json) as response:
            return await response.text()

async def request_data_param(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url,params=params) as response:
            return await response.text()

def find_phone_numbers(text):
    pattern = r'(\+?\d{1,2}\s?[-(]?\d{3}[-)]?\s?\d{3}\s?[-]?\s?\d{2}\s?[-]?\s?\d{2})'
    phone_numbers = re.findall(pattern, text)
    result = []
    for num in phone_numbers:
        number = num.replace("-", "").replace(' ','').replace('(','').replace(')','')
        if len(number) == 11 and num[0] != '8':
            number = '+' + number
        elif len(number) == 10:
            number = '+7' + number
        result.append(number)
        
    return result   

def create_lead(name: str, phone: str, userID:str, nicknameUser) -> str:
    """создание лида в базе если известо имя и телефон"""
    # print(f'{bcolors.OKGREEN}Создание лида{bcolors.ENDC}')
    # nickname = 'darkClaw921'
    # if find_phone_numbers(phone) == []:
    #     return 'Пожалуйста укажите номер телефона в формате 8(999)999-99-99'
    
    nickname = f'{nicknameUser}'
    utmSource = 'telegram'  
    utmMedium = 'neuro_bot' 
    text=f"""Создан новый лид: 
{name}
{userID} 
{phone}
{nickname}
{utmSource}
{utmMedium} """
    print(text)
    textDontUse = 'пользователь уже создал лид больше не создавай его и не используй функцию create_lead'
    text='Ваша заявка принята, ожидайте пока с вами свяжется менеджер'
    return 0

def find_most_similar_city(input_string, cities_dict):
        highest_similarity = 0
        most_similar_city = None
        
        for city in cities_dict.keys():
            # Вычисляем схожесть
            similarity = SequenceMatcher(None, input_string.lower(), city.lower()).ratio()
            
            # Если текущая схожесть выше, обновляем значения
            if similarity > highest_similarity:
                highest_similarity = similarity
                most_similar_city = city
                
        return most_similar_city, highest_similarity


async def handler_in_command(chat_id:int,
                             text:str,
                             messanger: str,
                             username:str):
    global USER_LIST
    if text == '/start':
        params={'chat_id': chat_id, 'text': 'Привет, я помогу тебе выбрать квартиру, просто скажи что вы хотите', 'messanger': messanger}
        await request_data_param(f'http://{SENDER_MESSAGE_URL}/send_message', params)
        try:
            await postgreWork.add_new_user(chat_id, username)
        except:
            print('Пользователь уже есть')

        # user=postgreWork.get_user(chat_id)
        # user.word_start=None
        fields={
            'word_start': None
        }
        postgreWork.update_user(chat_id, fields=fields)
        return 0

    if text == '/clear':
        clear_history(chat_id)
        params={'chat_id': chat_id, 'text': 'История диалога очищена', 'messanger': messanger}
        await request_data_param(f'http://{SENDER_MESSAGE_URL}/send_message', params)
        return 0

async def handler_in_message(chat_id: int, text: str, messanger: str, username:str):
    global USER_LIST
    isPersonalDataUser=False
    modelIndex='main'   

    if find_phone_numbers(text) != []:
        isPersonalDataUser=True
        user=postgreWork.get_user(userID=chat_id)
        if user.name is None:
            params={'chat_id': chat_id, 'text': 'Еще мне нужно ваще имя', 'messanger': messanger}
        
            await request_data_param(f'http://{SENDER_MESSAGE_URL}/send_message', params)
            return
        
        leadID=create_lead(name=user.name, phone=user.phone, 
                           userID=user.id,
                           nicknameUser=user.nickname)
        # user.lead_id=leadID
        fields={
            'lead_id': leadID
        }
        postgreWork.update_user(userID=user.id, fields=fields)
        params={'chat_id': chat_id, 'text': 'Ваша заявка принята, ожидайте пока с вами свяжется менеджер', 'messanger': messanger}
        await request_data_param(f'http://{SENDER_MESSAGE_URL}/send_message', params)
        return

    if text in ['питер', 'спб', 'spb']:
        text='Санкт-Петербург'
    most_similar_city, highest_similarity = find_most_similar_city(input_string=text.title(),
                                                                   cities_dict=CITIES_SLUG)
    if highest_similarity >= 0.60:

        fields={
            'city': CITIES_SLUG[most_similar_city],
        }    
        postgreWork.update_user(userID=chat_id, fields=fields)
        USER_LIST.pop(chat_id)

    #класифицируем историю ползователя 
    # history=get_history(chat_id)
    # params = {'text':text,'promt': 'Ты класификатор истории пользователя, надо определить какой это тип истории, если это личные данные то отправляй 1, если нет то 0', 
    #           'history': history, 'model_index': 'giga', 
    #           'temp': 0.5, 'verbose': 1}
    # answer=await request_data(f'http://{GENERATE_ANSWER_URL}/generate-answer', params)
    # answer=json.loads(answer)
    # pprint(answer)
    
    # if answer['answer']=='1':
    #     isPersonalDataUser=True
    #     modelIndex='giga'
        
        

    
    if not isPersonalDataUser:
        
        add_message_to_history(chat_id,'user', text)
        history = get_history(chat_id)
        # text=''
    else:
        text='номер телефона 888888888'

    userID=chat_id
    if len(history) > 15:
        clear_history(chat_id)
        add_message_to_history(chat_id, 'user', text)
        history = get_history(chat_id) 


    print(text)
    
    
#     promt="""Ты бот-помощник, который помогает пользователю найти информацию. Итвоя главная задача заставить купить 
# квартиру. отвечай пользователю только из информации в документе если не нашел информацию, то пиши что переводишь  диалог на менеджера"""
    

    
    if text in triggers:
            promt=triggers[text]
            USER_LIST[userID]=promt

    if userID not in USER_LIST:
        if text in triggers:
            promt=triggers[text]
            USER_LIST[userID]=promt
        else:
            promt='https://docs.google.com/document/d/1_ih810l3AfLZrNS2h1TNzOaO15ytrS7DGT9pSFpA9M8/edit?usp=sharing'
            params = {'promt_url': promt}
            promt=await request_data(f'http://{GENERATE_ANSWER_URL}/load-promt', params)
            userInfo=f"""userID: {userID}
        nickname: {username}
        utm_source={messanger}
        utm_medium=neuro_bot"""
            
            slugCity=postgreWork.get_user(userID=userID).city
            try:
                mortagage=apiStrana.prepare_mortgage(slugCity=slugCity)
                
            except Exception as e:
                print(e)
                mortagage='в вашем городе нету'
            
            promt=promt.replace('[userInfo]', userInfo)
            promt=promt.replace('[mortgage]', mortagage)
            USER_LIST[userID]=promt

    promt=USER_LIST[userID]
    
        

    
    
    
    params = {'text':text,'promt': promt+'Если никакая функция не вызывается то обязательно принудительно используй функцию conduct_dialogue', 
              'history': history, 'model_index': modelIndex, 
              'temp': 0.5, 'verbose': 1}
    
    try:
    
        answer=await request_data(f'http://{GENERATE_ANSWER_URL}/generate-answer', params)
    
    except:
        history=get_history(userID)[-2:]


        answer=await request_data(f'http://{GENERATE_ANSWER_URL}/generate-answer', params)
        

    answer=json.loads(answer)

    pprint(answer)
    # answer=answer['answer']
    
    message_content=answer['content']
    try:
        answer=answer['answer'][0]['output']
        if answer=='':
            answer=answer['answer'][1]['output']

    except:
        params = {'text':text,'promt': promt + 'Если никакая функция не вызывается то обязательно используй функцию conduct_dialogue', 'history': history, 'model_index': modelIndex, 'temp': 0.5, 'verbose': 1}   
        answer=await request_data(f'http://{GENERATE_ANSWER_URL}/generate-answer', params)
        answer=answer['answer'][0]['output']

    params={'chat_id': chat_id, 'text': answer, 'messanger': messanger}
    await request_data_param(f'http://{SENDER_MESSAGE_URL}/send_message', params)

    add_message_to_history(chat_id, 'system', f"информация из истории {message_content} \n") 
    add_message_to_history(chat_id, 'system', answer) 
   