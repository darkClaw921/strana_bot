from fastapi import FastAPI, HTTPException,Form,Depends
import requests
from pprint import pprint
import os
from dotenv import load_dotenv
# from fastapi.security import OAuth2PasswordBearer
load_dotenv()

from typing import Annotated
from fastapi.staticfiles import StaticFiles
from typing import List, Dict
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel,Field
from datetime import datetime
from pprint import pformat, pprint
from chat import GPT
from helper import prepare_table_for_text
from graphqlStrana import get_layouts_text
# from fastapi import FastAPI, 
# TOKEN_BOT = os.getenv('TOKEN_BOT_EVENT')
gpt=GPT()
app = FastAPI(debug=False)
load_dotenv()
PORT = os.getenv('PORT_GENERATE_ANSWER')
HOST = os.getenv('HOST')
IP_SERVER = os.getenv('IP_SERVER')

app = FastAPI(
    title="STRANA System API",
    description="Generate answer API\nЛоги можно посмотреть по пути /logs\nОчистить логи можно по пути /clear_logs\n",
    version="1.0"
)
app.mount("/static", StaticFiles(directory="static/"), name="static")
templates = Jinja2Templates(directory="templates")
logs = []

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}

MODELS_INDEX={
    # 'model_1': 'gpt2',
}

def update_or_create_model_index():
    global MODELS_INDEX
    # text=prepare_table_for_text()
    text='данные о компании'
    #TODO: не работает
    # text1=get_layouts_text()
    text1='Планировка Страна.Береговая в Новосибирск, ул. 2-я Сухарная, 109/2:\n'

#     text1="""Планировка Страна.Береговая в Новосибирск, '
# 'ул. 2-я Сухарная, 109/2:\n'
# 'Площадь: 65.11 кв.м\n'
# 'Количество комнат: 3\n'
# 'Цена: 11620000.0 руб.\n'
# 'Цена без скидки: 12630435.0 руб.\n'
# 'Размер скидки: 0 руб.\n'
# 'Максимальная скидка: 0 руб.\n'
# 'Ссылка на планировку: \n'
# 'Особенности: Постирочная\n'
# 'Специальные предложения:  \n'"""
    main=gpt.load_search_indexes(text)
    MODELS_INDEX['main']=main
    print('начали получать комнаты')

    rooms=gpt.load_search_indexes(text1)
    MODELS_INDEX['rooms']=rooms
    return MODELS_INDEX

update_or_create_model_index()
pprint(MODELS_INDEX)
class Generate(BaseModel):
    text: str
    model_index: str
    temp: float
    history: list
    promt: str
    verbose: int

class Load_promt(BaseModel):
    promt_url: str

@app.get("/load-promt") 
async def load_promt(data: Load_promt):
    promt=gpt.load_prompt(data.promt_url)
    return promt

@app.get("/generate-answer/")
async def generate_answer(data: Generate):
    
    promt=data.promt
    text=data.text
    modelIndex=data.model_index
    temp=data.temp
    history=data.history
    if promt.startswith('http'):
        promt=gpt.load_prompt(promt)

    pprint(data.__dict__)
    # answer, token, price, docs =gpt.answer_index(system=promt, topic=text, history=history, 
    #                                              search_index=MODELS_INDEX[model_index],
    #                                              temp=temp, verbose=0)
    modelIndex='rooms'
    if modelIndex=='giga':
        modelIndex='rooms'
        # answer=gpt.classification_gigachat(promt=promt, question=text, history=history)
        # message_content = ''
    
    else:
        answer,message_content = gpt.answer_tools_index(system=promt,topic=text, history=history, 
                                    # search_index=MODELS_INDEX[modelIndex], 
                                    search_index=MODELS_INDEX['rooms'], 
                                    temp=temp, verbose=0)
        try:
            pprint(answer)
            if answer[0]['type'] in ['find_room']:
                text=answer[0]['output']
                answer,message_content = gpt.answer_tools_index(system=promt,topic="не запуская функцию find_room найли информачию о"+text, history=history, 
                                            search_index=MODELS_INDEX['rooms'], 
                                            temp=temp, verbose=0)
            if answer[0]['type'] in ['save_name_user']:
                text=answer[0]['output']
                answer,message_content = gpt.answer_tools_index(system=promt+'Пользователь оставил имя, тебе не нужно здароваться просто продалжай диалог по промту',
                                            topic=text, history=history, 
                                            search_index=MODELS_INDEX['rooms'], 
                                            temp=temp, verbose=0)
        except Exception as e:
            print(e)
            

    # pprint(MODELS_INDEX)

    return {"answer": answer,'content':message_content}



#работа с логами

def log_counts_by_level(logs: list) -> dict:
    counts = {'DEBUG': 0, 'INFO': 0, 'WARNING': 0, 'ERROR': 0}
    for log in logs:
        counts[log['level']] += 1
    return counts

def log_counts_by_minute(logs: list) -> dict:
    counts_by_minute = {}
    for log in logs:
        timestamp_minute = log['timestamp'][:16]  # Обрезаем до минут
        if timestamp_minute in counts_by_minute:
            counts_by_minute[timestamp_minute][log['level']] += 1
        else:
            counts_by_minute[timestamp_minute] = {'DEBUG': 0, 'INFO': 0, 'WARNING': 0, 'ERROR': 0}
            counts_by_minute[timestamp_minute][log['level']] += 1
    return counts_by_minute

@app.post("/logs")
async def add_log(log: Request):
    global logs

    # pprint(log.__dict__)
    json = await log.json()
    log_entry=json.get('log_entry')
    log_level = json.get('log_level')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    if len(logs) >= 100:
        logs.pop(0)
    logs.append({'timestamp': timestamp, 'level': log_level, 'message': log_entry})
    return {"message": "Лог записан!"}

@app.get("/logs", response_class=HTMLResponse)
async def view_logs(request: Request):
    global logs
    for log in logs:
        if isinstance(log['message'], dict) or isinstance(log['message'], list):
            log['message'] = pformat(log['message'])

    logs.reverse()
    counts_log = log_counts_by_level(logs)
    counts_log = log_counts_by_minute(logs)
    pprint(counts_log)
    return templates.TemplateResponse("index.html", {"request": request, "logs": logs, "log_counts": counts_log})

@app.post("/clear_logs")
async def clear_logs():
    global logs
    logs.clear()
    return {"message": "Логи очищены!"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(PORT))
