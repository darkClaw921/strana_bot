from sqlalchemy import (create_engine, Column, 
                        Integer, Float, String,
                        DateTime, JSON, ARRAY, 
                        BigInteger, func, text, 
                        BOOLEAN, URL, ForeignKey, cast)
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship, declarative_base
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pprint import pprint


load_dotenv()
userName = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
db = os.environ.get('POSTGRES_DB')
url = os.environ.get('POSTGRES_URL')



# Создаем подключение к базе данных
engine = create_engine(f'postgresql://{userName}:{password}@{url}:5432/{db}')
# engine = create_engine('mysql://username:password@localhost/games')




 
# Определяем базу данных
Base = declarative_base()



class User(Base):
    __tablename__ = 'User'
    
    id = Column(BigInteger, primary_key=True)
    created_date = Column(DateTime)
    nickname = Column(String)
    name=Column(String)
    phone=Column(String)
    lead_id=Column(BigInteger)
    city=Column(String)

    all_token=Column(Float)
    all_token_price=Column(Float)
    payload=Column(String)
    promt=Column(String)
    word_start=Column(String)
   
        

class Message(Base):
    __tablename__ = 'Message'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_date = Column(DateTime)
    user_id = Column(BigInteger)    
    message_id = Column(BigInteger)
    payload = Column(String)
    type_chat = Column(String)
    text = Column(String)



Base.metadata.create_all(engine)
# Base.metadata.update_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
# session


def add_new_user(userID:int, nickname:str):
    with Session() as session:
        newUser=User(
            created_date=datetime.now(),
            id=userID,
            nickname=nickname,
            all_token=0,
            all_token_price=0,     
               
        )
        
        session.add(newUser)
        session.commit()



def add_new_message(messageID:int, chatID:int, userID:int, text:str, type_chat:str,payload:str):
    with Session() as session:
        newMessage=Message(
            message_id=messageID,
            created_date=datetime.now(),
            group_id=chatID,
            user_id=userID,
            text=text,
            type_chat=type_chat,
            payload=payload
        )
        session.add(newMessage)
        session.commit()



def update_payload(userID:int, payload:str):
    with Session() as session:
        session.query(User).filter(User.id==userID)\
            .update({User.payload:payload}) 
        session.commit()

def update_token_for_user(userID:int, token:float):
    with Session() as session:
        user=session.query(User).filter(User.id==userID).one()
        user.all_token+=token
        session.commit()

def update_token_price_for_user(userID:int, tokenPrice:float):
    with Session() as session:
        user=session.query(User).filter(User.id==userID).one()
        user.all_token_price+=tokenPrice
        session.commit()

#обновляем данные пользователя только те что передали 
def update_user_name_and_phone(userID:int, name:str, phone:str):
    with Session() as session:
        user=session.query(User).filter(User.id==userID).one()
        user.name=name
        user.phone=phone
        # user.lead_id=lead_id
        # user.city=city

        session.commit()


def update_user(userID:int, fields:dict):
    with Session() as session:
        session.query(User).filter(User.id==userID).update(fields)
        
        session.commit()


def get_user(userID:int)->User:
    with Session() as session:
        user=session.query(User).filter(User.id==userID).one()
        return user
 
def get_payload(userID:int)->str:
    with Session() as session:
        user=session.query(User).filter(User.id==userID).one()
        return user.payload



def get_all_user_ids()->list[int]:
    ids=[]
    with Session() as session:
        users=session.query(User.id).all()
        for user in users:
            ids.append(user.id)
        return ids


def get_last_messages_for_user(userID:int, groupID:int, count:int=10)->list[Message]:
    with Session() as session:
        # messages=session.query(Message).filter(Message.user_id==userID).order_by(Message.created_date.desc()).limit(count).all()
        messages=session.query(Message).filter(Message.user_id==userID, Message.group_id==groupID).order_by(Message.created_date.desc()).limit(count).all()
        return messages


def check_user(userID:int)->bool:
    with Session() as session:
        users=session.query(User).filter(User.id==userID).all()
        if len(users) > 0:
            return True
        else:
            return False



if __name__ == '__main__':
   
    pass