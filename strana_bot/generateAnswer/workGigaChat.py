# from langchain.llms import GigaChat
# from langchain.chat_models import ChatGigaChat
# from langchain.schema import HumanMessage, SystemMessage, AIMessage, FunctionMessage
# from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from typing import List, Dict, Any, Optional
# from langchain_community.chat_models import ChatGigaChat
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.agents import AgentExecutor, create_gigachat_functions_agent
from typing import Dict
from langchain.tools import tool
from langchain_community.chat_models import GigaChat

@tool
def get_all_phone_names() -> str:
    """Возвращает названия моделей всех телефонов через запятую"""
    # Подсвечивает вызов функции зеленым цветом
    print("\033[92m" + f"Bot requested get_all_phone_names()" + "\033[0m")
    return ', '.join([stuff["name"] for stuff in stuff_database])

@tool
def get_phone_data_by_name(name: str) -> Dict:
    """
    Возвращает цену, характеристики и описание телефона по точному названию модели.

    Args:
        name (str): Точное название модели телефона.

    Returns:
        Dict: Словарь с информацией о телефоне (цена, характеристики и описание).
    """
    # Подсвечивает вызов функции зеленым цветом
    print("\033[92m" + f"Bot requested get_phone_data_by_name({name})" + "\033[0m")
    for stuff in stuff_database:
        if stuff["name"] == name:
            return stuff
    return None

@tool
def create_order(name: str, phone: str) -> None:
    """
    Создает новый заказ на телефон.

    Args:
        name (str): Название телефона.
        phone (str): Телефонный номер пользователя.

    Returns:
        str: Статус заказа.
    """
    # Подсвечивает вызов функции зеленым цветом
    print("\033[92m" + f"Bot requested create_order({name}, {phone})" + "\033[0m")
    print(f"!!! NEW ORDER !!! {name} {phone}")

tools = [
    get_all_phone_names,
    get_phone_data_by_name,
    create_order
]




# giga = GigaChat(credentials="", model="GigaChat", verify_ssl_certs=False)




# agent = create_gigachat_functions_agent(giga, tools)

# AgentExecutor создает среду, в которой будет работать агент
# agent_executor = AgentExecutor(
#     agent=agent,
#     tools=tools,
#     verbose=False,
# )






# class GigaChatWorker:
#     def __init__(self, credentials: str, scope: str = "GIGACHAT_API_PERS", verbose: bool = False):
#         self.credentials = credentials
#         self.scope = scope
        
#         callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]) if verbose else None
        
#         self.chat_model = ChatGigaChat(
#             credentials=self.credentials,
#             scope=self.scope,
#             verify_ssl_certs=False,
#             callback_manager=callback_manager
#         )

#     def generate_answer(self, messages: List[Dict[str, str]], functions: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
#         """
#         Генерирует ответ с использованием ГигаЧата через LangChain.

#         :param messages: Список сообщений в формате [{"role": "user", "content": "Привет"}, ...]
#         :param functions: Список доступных функций (опционально)
#         :return: Сгенерированный ответ
#         """
#         langchain_messages = []
#         for message in messages:
#             if message["role"] == "user":
#                 langchain_messages.append(HumanMessage(content=message["content"]))
#             elif message["role"] == "assistant":
#                 langchain_messages.append(AIMessage(content=message["content"]))
#             elif message["role"] == "system":
#                 langchain_messages.append(SystemMessage(content=message["content"]))
#             elif message["role"] == "function":
#                 langchain_messages.append(FunctionMessage(content=message["content"], name=message.get("name", "")))

#         if functions:
#             self.chat_model.function_call = "auto"
#             self.chat_model.functions = functions

#         response = self.chat_model(langchain_messages)

#         return {
#             "role": "assistant",
#             "content": response.content,
#             "function_call": response.additional_kwargs.get("function_call")
#         }


def main():
    # Пример использования без функций
    gigachat = GigaChatWorker(credentials="ваш_токен", verbose=True)
    
    messages_without_functions = [
        {"role": "system", "content": "Вы - полезный ассистент."},
        {"role": "user", "content": "Привет! Расскажи мне о погоде в Москве."}
    ]
    
    response_without_functions = gigachat.generate_answer(messages_without_functions)
    print("Ответ без использования функций:")
    print(response_without_functions)
    print("\n" + "="*50 + "\n")

    # Пример использования с функциями
    messages_with_functions = [
        {"role": "system", "content": "Вы - ассистент по продаже телефонов."},
        {"role": "user", "content": "Какие телефоны у вас есть в наличии?"}
    ]
    
    functions = [
        {
            "name": "get_phones",
            "description": "Получить список доступных телефонов",
            "parameters": {
                "type": "object",
                "properties": {
                    "brand": {"type": "string", "description": "Бренд телефона"},
                    "price_range": {"type": "string", "description": "Ценовой диапазон"}
                },
                "required": ["brand"]
            }
        }
    ]
    
    response_with_functions = gigachat.generate_answer(messages_with_functions, functions)
    print("Ответ с использованием функций:")
    print(response_with_functions)

if __name__ == "__main__":
    # main()
    system = "Ты — бот-продавец телефонов. Твоя задача — продать телефон пользователю, получив от него заказ. Если тебе не хватает каких-то данных, запрашивай их у пользователя."
    chat_history = [SystemMessage(content=system)]
    while True:
        user_input = input("Покупатель: ")
        if user_input == "":
            break
        result = agent_executor.invoke(
            {
                "chat_history": chat_history,
                "input": user_input,
            }
        )
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=result["output"]))
        print(f"Bot: {result['output']}")
