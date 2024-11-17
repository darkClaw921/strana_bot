from langchain_community.llms import OpenAI
from langchain.docstore.document import Document
import requests
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from operator import itemgetter

# import ipywidgets as widgets

import re

from openai import OpenAI
import os

# import tiktoken
import sys
from loguru import logger
from pprint import pprint
from langchain_core.tools import tool
from langchain_openai import  ChatOpenAI
from langchain.output_parsers import JsonOutputToolsParser
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough
from langchain_core.messages import HumanMessage, AIMessage
# from langchain.chat_models.gigachat import GigaChat

# from langchain_community.chat_models import GigaChat

# from langchain.agents import AgentExecutor, create_gigachat_functions_agent

from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models import ChatYandexGPT
import tiktoken
from dotenv import load_dotenv
load_dotenv()

key = os.environ.get('OPENAI_API_KEY')

# YC_IAM_TOKEN = os.environ.get('YC_IAM_TOKEN')
client = OpenAI(api_key=key,)
keyGiga = os.getenv('GIGA_CHAT_API_KEY')
print(keyGiga)
# chat_model = ChatYandexGPT(folder_id='b1g83bovl5hjt7cl583v', model_uri='gpt://b1g83bovl5hjt7cl583v/yandexgpt')       
# giga = GigaChat(credentials=keyGiga, model="GigaChat", verify_ssl_certs=False)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# from promt import clasificatorPromt

USERS_THREADS = {}
# from langchain.memory import PostgresChatMessageHistory
# history = PostgresChatMessageHistory(
#     connection_string="postgresql://postgres:mypassword@localhost/chat_history",
#     session_id="foo",
# )
# history.aget_messages()
# history.add_user_message("hi!")

# history.add_ai_message("whats up?")
# @tool
# def count_emails(last_n_days: int) -> int:
#     """Multiply two integers together."""
#     return last_n_days * 2


# @tool
# def send_email(message: str, recipient: str) -> str:
#     "Add two integers."
#     return f"Successfully sent email to {recipient}."

# тригер слово 
# промт 
# файл
# функция "собирает лид"




@tool('conduct_dialogue',return_direct=False)
def conduct_dialogue(text:str) -> str:
  """Ведет диалог с пользователем пока не будет вызвона другая функция create_lead"""
  print(f'{bcolors.OKGREEN}Диалог с пользователем{bcolors.ENDC}')
  return text

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

import postgreWork

@tool('save_name_user')
def save_name_user(name:str, userID:str):
    """Сохраняет имя пользователя"""
    print(f'{bcolors.OKGREEN}Сохранение имени пользователя{bcolors.ENDC}') 
    
    fields={
       'name':name
    }
    
    postgreWork.update_user(userID=userID,fields=fields )
    return name

@tool('create_lead',return_direct=False)
def create_lead(name: str, phone: str, userID:str) -> str:
    """создание лида в базе если известо имя и телефон"""
    print(f'{bcolors.OKGREEN}Создание лида{bcolors.ENDC}')
    # nickname = 'darkClaw921'
    if find_phone_numbers(phone) == []:
        return 'Пожалуйста укажите номер телефона в формате 8(999)999-99-99'
    
    nickname = 'None'
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
    return text
    # return {'name': name, 'phone': phone, 'nickname': nickname, 'utmSource': utmSource, 'utmMedium': utmMedium, 'userID': userID}

@tool('find_room', return_direct=True)
def find_room(area:float, adress:str):
   """ищет квартиры если пользователь явно указал площадь и адресс"""
   
   print(f'{bcolors.OKGREEN}Поиск квартиры{bcolors.ENDC}')
   text=f"Площадь: {area} кв.м\n"
   text+=f'{adress}'
   return text

#https://services.strana.com/api/v1/loan-offers/best/list?initialPayment=77&loanPeriod=25&cost=55290000&city=msk&program=all
# [{"id":2,"name":"Семейная ипотека","description":"Получите кредит на новую квартиру по льготной госпрограмме для семей с детьми","minPaymentAmount":88102,"minInitialPayment":20,"maxCreditAmount":30000000,"rate":6.78,"rateReduced":null,"maxCreditPeriod":30,"byDev":false,"periodParams":null},{"id":1,"name":"Стандартная ипотека","description":"Стандартная ипотека предусматривает получение кредита на общих основаниях с целью покупки жилья","minPaymentAmount":156004,"minInitialPayment":15,"maxCreditAmount":1200000000,"rate":14.3,"rateReduced":7.6,"maxCreditPeriod":30,"byDev":false,"periodParams":[{"months":24,"rate":7.6,"monthlyPayment":9480402},{"months":276,"rate":14.3,"monthlyPayment":15296575}]}]
def prepare_response(response:dict)->str:
    text=''
    #разбираем ценны на триады
    for i in response:
        text+=f"{i['name']}\n"
        text+=f"Первоначальный взнос: {i['minInitialPayment']}%\n"
        text+=f"Сумма кредита: {i['maxCreditAmount']:,} руб.\n"
        text+=f"Ставка: {i['rate']}%\n"
        text+=f"Минимальный ежемесячный платеж: {i['minPaymentAmount']:,} руб.\n"
        text+=f"Срок кредита: {i['maxCreditPeriod']} лет\n\n"
       

    return text

@tool('calculate_mortgage', return_direct=True)
def calculate_mortgage(initialPayment:int, loanPeriod:int, cost:int, city:str='msk', program:str='all'):
  """расчет ипотеки"""
  url=f'https://services.strana.com/api/v1/loan-offers/best/list?initialPayment={initialPayment}&loanPeriod={loanPeriod}&cost={cost}&city={city}&program={program}'
  response=requests.get(url)
  headers = {
    'accept': 'application/json',
  }

  params = {
    'city': city,
    'cost': cost,
    'initialPayment': initialPayment,
    'loanPeriod': loanPeriod,
    'program': program,
  }

  response = requests.get('https://services.stranadev-new.com/api/v1/loan-offers/best/list', params=params, headers=headers)
  pprint(response.json())  

  return prepare_response(response.json())



tools = [conduct_dialogue, find_room,save_name_user ]
# tools = [create_lead, conduct_dialogue, find_room, calculate_mortgage]
# # modelTools = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0).bind_tools(tools)
modelTools = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)



def call_tool(tool_invocation: dict) -> Runnable:
    """Function for dynamically constructing the end of the chain based on the model-selected tool."""
    tool_map = {tool.name: tool for tool in tools}
    tool = tool_map[tool_invocation["type"]]
    return RunnablePassthrough.assign(output=itemgetter("args") | tool)

call_tool_list = RunnableLambda(call_tool).map()
chain = modelTools | JsonOutputToolsParser() | call_tool_list



# agent = create_gigachat_functions_agent(giga, tools)

# # AgentExecutor создает среду, в которой будет работать агент
# giga_agent_executor = AgentExecutor(
#     agent=agent,
#     tools=tools,
#     verbose=False,
# )




# a = chain.invoke("сколько электронных писем я получил за последние 5 дней?")
# print(a)
# a = chain.invoke("пользователь уже создал лид больше не создавай его и не используй функцию create_lead  меня зовут Вася, мой номер телефона 8-800-555-35-35 ")
# print(a)

# 1/0
# a = chain.invoke("отправь писмо на адрес datkclaw@yandex.ru")
# a = chain.invoke("Send sally@gmail.com an email saying 'What's up homie")
# a = chain.invoke("Есть что-нибудь на завтра в Москве по танцам?")
# history="""Клиент: привет, я хочу узнать о мероприятии на завтра 
# Ассистент: Здравствуйте, уточните пожалуйста, в каком городе вы хотите найти мероприятие?
# Клиент: Бали
# Ассистент: какая тема мероприятия вас интересует?
# Клиент: танцы"""
# history="""Клиент: привет, я хочу узнать о мероприятии на завтра по танцам в убуд"""
# a=chain.invoke(
#     [
#         HumanMessage(
#             content="привет, я хочу узнать о мероприятии на завтра"
#         ),
#         AIMessage(content="Здравствуйте, уточните пожалуйста, в каком городе вы хотите найти мероприятие?"),
#         HumanMessage(content="Бали"),
#         AIMessage(content="какая тема мероприятия вас интересует?"),
#         HumanMessage(content="танцы"),
#     ]
# # )
# a=chain.invoke(
#   history
# )
# print(a)

# 1/0
class GPT():
  modelVersion = ''
  def __init__(self,modelVersion:str = 'gpt-4o-mini'):
    self.modelVersion = modelVersion
    pass

  

 
  def load_search_indexes(self, text:str = '') -> str:
    # Extract the document ID from the URL
    print('попали в load_serch_index')
    a=None
    a=self.create_embedding(text)

    return a

  def load_prompt(self, 
                  url: str) -> str:
    # Extract the document ID from the URL
    match_ = re.search('/document/d/([a-zA-Z0-9-_]+)', url)
    if match_ is None:
        raise ValueError('Invalid Google Docs URL')
    doc_id = match_.group(1)

    # Download the document as plain text
    response = requests.get(f'https://docs.google.com/document/d/{doc_id}/export?format=txt')
    response.raise_for_status()
    text = response.text
    return f'{text}'

  def create_image(self, promt:str) -> str:
    
    response = client.images.generate(prompt=promt,
    n=1,
    size="256x256")

    return response.data[0].url
  

  def create_embedding(self, data=None):
      
    def num_tokens_from_string(string: str, encoding_name: str) -> int:
      """Returns the number of tokens in a text string."""
      encoding = tiktoken.get_encoding(encoding_name)
      num_tokens = len(encoding.encode(string))
      return num_tokens

    source_chunks = []
    #splitter = CharacterTextSplitter(separator="\n", chunk_size=1524, chunk_overlap=0)
    splitter = CharacterTextSplitter(separator="==========", chunk_size=300, chunk_overlap=200)
    # pprint(splitter[1])
    os.remove('text.txt')
    for chunk in splitter.split_text(data):
      print(chunk)
      with open('text.txt', 'a') as f:
        f.write('\n==========\n')
        f.write(chunk)
      source_chunks.append(Document(page_content=chunk, metadata={}))

    # Создание индексов документа
    search_index = None
    search_index = Chroma.from_documents(source_chunks, OpenAIEmbeddings(), )
    # search_index.similarity_search
    count_token = num_tokens_from_string(' '.join([x.page_content for x in source_chunks]), "cl100k_base")
    print('\n ===========================================: ')
    print('Количество токенов в документе :', count_token)
    print('ЦЕНА запроса:', 0.0004*(count_token/1000), ' $')
    return search_index

  
  def answer_assistant(self,text, temp = 1, userID:int=0):
    global USERS_THREADS
    assistant ='asst_ljJQn6stjMsgIcGj4PkMvxnD' 
    
    # Upload a file with an "assistants" purpose
    lista=client.files.list(purpose='assistants')
    pprint(lista)
    fileCSV=lista.data[0]
   
    try:
      thread=USERS_THREADS[userID]
    except:
      thread = client.beta.threads.create()
      USERS_THREADS[userID] = thread 
    
    
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text,
        file_ids=[fileCSV.id]
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant,
        instructions="",
        tools=[{"type": "retrieval"}],
        
    )

    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
        )
     
    pprint(run.status)

    while run.status != 'completed':
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        logger.debug(run.status)

    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )

    pprint(run.usage)    
    
    totalToken = run.usage['total_tokens']
    #https://openai.com/pricing
    tokenPrice = 0.002*(totalToken/1000)
    print(totalToken)
    # pprint(thread.__dict__)
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
        )

   
    
    logger.info(f'{messages.data[0].content[0].text.value=}')
    answerText = messages.data[0].content[0].text.value 
    return answerText, totalToken, tokenPrice
  
  def answer_gigachat(self, promt:str,question:str, history:list, temp = 1, modelVersion='GigaChat'):
    messages = [
      {"role": "system", "content": promt},
      *history,
      {"role": "user", "content": question},
      ]
    pprint(messages)
    chat_history=[] 
    for i in messages:
      if i['role'] == 'user':
        chat_history.append(HumanMessage(i['content']))
      if i['role'] == 'system':
        chat_history.append(SystemMessage(i['content']))
    pprint(chat_history[0])
    answer = giga.invoke(chat_history)
    return answer

  def answer_gigachat_tools(self, promt:str,question:str, history:list, temp = 1, modelVersion='GigaChat'):
    messages = [
      {"role": "system", "content": promt},
      *history,
      # {"role": "user", "content": question},
      ]
    chat_history=[]
    pprint(messages)
    for i in messages:
      if i['role'] == 'user':
        chat_history.append(HumanMessage(i['content']))
      if i['role'] == 'system':
        chat_history.append(SystemMessage(i['content']))
    pprint(chat_history[0])
    answer = giga_agent_executor.invoke({
          'chat_history': chat_history,
          'input': question
       }
       )
    return answer.output  

  def classification_gigachat(self, promt:str, question:str, history:list, temp = 1, modelVersion='GigaChat')->str:
    messages = [
      
      {"role": "system", "content": promt},
      *history,
      {"role": "user", "content": question},
      ]
    chat_history=[]
    for i in messages:
      if i['role'] == 'user':
        chat_history.append(HumanMessage(i['content']))
      if i['role'] == 'system':
        chat_history.append(SystemMessage(i['content']))

    pprint(chat_history)
    pprint(chat_history[0])
    answer = giga.invoke(chat_history)

    return answer.content

  def answer(self, system, topic:list, temp = 1, modelVersion='gpt-4o-mini'):
    """messages = [
      {"role": "system", "content": system},
      {"role": "user", "content": topic}
      ]
    """

    messages = [
      {"role": "system", "content": system },
      
      ]
    messages.extend(topic)
    
    completion = client.chat.completions.create(model=modelVersion,
    
        messages=messages,
        temperature=temp,)
        
    
    totalToken = completion.usage.total_tokens
    answerText =completion.choices[0].message.content

    allToken = f'{totalToken} токенов использовано всего (вопрос-ответ).'
    allTokenPrice = f'ЦЕНА запроса с ответом :{0.002*(totalToken/1000)} $'
   
    return f'{answerText}', totalToken, 0.03*(totalToken/1000)
  
  @logger.catch
  def num_tokens_from_messages(self, messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            #logger.error(f'{messages}')
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
        
  def insert_newlines(self, text: str, max_len: int = 170) -> str:
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + " " + word) > max_len:
            lines.append(current_line)
            current_line = ""
        current_line += " " + word
    lines.append(current_line)
    return "\n".join(lines)

  def answer_yandex(self,promt:str, history:list, temp = 1):
    messages = [
      {"role": "system", "content": promt },
      #{"role": "user", "content": topic}
      #{"role": "user", "content": context}
      ]
    messages.extend(history) 
    historyPrepare = []
    for i in messages:
      if i['role'] == 'user':
        historyPrepare.append(HumanMessage(i['content']))
      if i['role'] == 'system':
        historyPrepare.append(SystemMessage(i['content']))
        
    answer = chat_model(historyPrepare)
    
    pprint(answer.content)

    answerText = answer.content
   
    
    # return f'{answerText}', totalToken, priceTokenRUB
    return f'{answerText}', 0,0,
  

  def asnwer_tools(self, history:list, temp = 1):
    
    historyText=''
    for i in history:
      if i['role'] == 'user':
        historyText+= f"Клиент: {i['content']}\n"
      
      if i['role'] == 'system':
        historyText+= f"Ассистент: {i['content']}\n"
    print(f'{historyText=}')
    answer=chain.invoke(
      historyText
    )
    print('========================================================')
    pprint(answer)
    
    answer=answer
    return answer

  def answer_tools_index(self, system, topic, history:list, search_index, temp = 1, verbose = 0):
    #Выборка документов по схожести с вопросом
    docs = search_index.similarity_search(topic, k=4)
    # print(search_index. )
    if (verbose): print('\n ===========================================: ')
    message_content = re.sub(r'\n{2}', ' ', '\n '.join([f'\nДокумент №{i+1}\n=====================' + doc.page_content + '\n' for i, doc in enumerate(docs)]))
    if (verbose): print('message_content :\n ======================================== \n', message_content)
    
    systemMess = 'Данные, на основании которых нужно продолжить диалог:'
    messages = [
      {"role": "system", "content": system + f"{systemMess} {message_content}"},
      {"role": "user", "content": 'Диалог с клиентом, который нужно продолжить:'},
      ]
    messages.extend(history)     
    
    historyText=''
    for i in messages:
      if i['role'] == 'user':
        historyText+= f"Клиент: {i['content']}\n"
      
      if i['role'] == 'system':
        historyText+= f"Ассистент: {i['content']}\n"
    print(f'{historyText=}')
    answer=chain.invoke(
      historyText
    )
    return answer, message_content 
  
  def answer_index(self, system, topic, history:list, search_index, temp = 1, verbose = 0):
    
    #Выборка документов по схожести с вопросом 
    docs = search_index.similarity_search(topic, k=2)
    if (verbose): print('\n ===========================================: ')
    message_content = re.sub(r'\n{2}', ' ', '\n '.join([f'\nДокумент №{i+1}\n=====================' + doc.page_content + '\n' for i, doc in enumerate(docs)]))
    if (verbose): print('message_content :\n ======================================== \n', message_content)

    systemMess = 'Данные, на основании которых нужно продолжить диалог:'
    messages = [
      {"role": "system", "content": system + f"{systemMess} {message_content}"},
      {"role": "user", "content": 'Диалог с клиентом, который нужно продолжить:'},
      ]
    
    messages.extend(history)
    pprint(messages)
    # example token count from the function defined above
    if (verbose): print('\n ===========================================: ')
    if (verbose): print(f"{self.num_tokens_from_messages(messages, 'gpt-3.5-turbo-0301')} токенов использовано на вопрос")

    completion = client.chat.completions.create(model=self.modelVersion,
        messages=messages,
        temperature=temp)
    totalToken = completion.usage.total_tokens
    answerText =completion.choices[0].message.content
    if (verbose): print('\n ===========================================: ')
    if (verbose): print(f'{totalToken} токенов использовано всего (вопрос-ответ).')
    if (verbose): print('\n ===========================================: ')
    if (verbose): print('ЦЕНА запроса с ответом :', 0.002*(totalToken/1000), ' $')
    if (verbose): print('\n ===========================================: ')
    print('ОТВЕТ : \n', self.insert_newlines(answerText))

    answer = answerText
    
    return f'{answer}', totalToken, 0.002*(totalToken/1000), docs

#    return answer
  def vision_answer(self, promt:str, base64_image:str):
    response = client.chat.completions.create(
      model="gpt-4-vision-preview",
      messages=[
              {
                  "role": "user",
                  "content": [
                      {"type": "text", "text": promt},
                      {
                          "type": "image_url",
                          "image_url": {
                             'url': f"data:image/jpeg;base64,{base64_image}"
                          },
                      },
                  ],
              }
          ],
          # max_tokens=300,
    )

    print(response.choices[0])
    return response.choices[0].message.content
     
     
     
     
      
  def get_summary(self, history:list, 
                  promtMessage = 'Write a concise summary of the following and CONCISE SUMMARY IN RUSSIAN:',
                  temp = 0.3):    
    """messages = [
      {"role": "system", "content": system},
      {"role": "user", "content": topic}
      ]
    """
    
    messages = [
      {"role": "system", "content": promtMessage},
      ]
    messages.extend(history)
    logger.info(f'answer message get_summary {messages}')
    completion = client.chat.completions.create(model=self.modelVersion,
      messages=messages,
      temperature=temp)
    logger.info(f'{completion["usage"]["total_tokens"]=}')
    logger.info(f'{completion["usage"]=}')
    answer =completion.choices[0].message.content  
    logger.info(answer)
    roleAsnwer= {'role': 'user', 'content': answer}
    return roleAsnwer

  
if __name__ == "__main__":   
  gpt = GPT()
  system='ты продажник квартир'
  messages = [
      {"role": "user", "content": 'ты робот',}
      # {"role": "user", "content": topic}
      ]
  # a = gpt.answer(system=system, topic=messages)
  # a= gpt.answer_gigachat(promt=system, question='есть квартра 59 кв метров в липецке?', history=messages)
  # print(a)
  a = gpt.answer_gigachat_tools(promt=system, question='есть квартра 59 кв метров в липецке?', history=messages)
  print(a)
  b="""
Сибирский сад в Екатеринбург, ул. братиславская тракт, 24:
"""
  a = gpt.classification_gigachat(promt="ты класификатор вопросов есть ли персональные данные или нет", question=b, history=[{"role": "user", "content": '',}])
  print(a)

  
  # a=requests.get('https://services.strana.com/api/v1/loan-offers/best/list?initialPayment=77&loanPeriod=25&cost=55290000&city=msk&program=all')
  # print(a.text)
  # b=prepare_response(response.json())
  # print(b)