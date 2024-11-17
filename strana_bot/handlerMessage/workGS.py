import gspread
from oauth2client.service_account import ServiceAccountCredentials
from loguru import logger
from pprint import pprint

class Sheet():

    @logger.catch
    def __init__(self, jsonPath: str, sheetName: str, workSheetName, servisName: str = None):

        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']  # что то для чего-то нужно Костыль
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            jsonPath, self.scope)  # Секретынй файл json для доступа к API
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(sheetName).worksheet(
            workSheetName)  # Имя таблицы
        # self.sheet = self.client.open(workSheetName)  # Имя таблицы

    def send_cell(self, position: str, value):
        #self.sheet.update_cell(position, value=value)
        self.sheet.update(position, value)

    def update_cell(self, r, c, value):
        self.sheet.update_cell(int(r), int(c), value)
        # sheet.update_cell(1, 1, "I just wrote to a spreadsheet using Python!")0

    def find_cell(self, value):
        cell = self.sheet.find(value)
        return cell

    def get_cell(self, row: str):
        # A1
        cell = self.sheet.acell(row).value
        return cell

    def get_value_in_column(self, column: int):
        # 3
        cell = self.sheet.col_values(column)
        return cell

    def insert_cell(self,data:list):
        """Записывает в последнуюю пустую строку"""
        nextRow = len(self.sheet.get_all_values()) + 1
        self.sheet.insert_row(data,nextRow, value_input_option='USER_ENTERED')
    
    def get_last_clear_row_for_column(self, column: str='ЛОКАЦИЯ'):
        """Находит последнюю пустую строку в колонке и возвращает ее номер и номер колонки"""
        colLocation=self.find_cell(column).col
        valuesLocation=self.get_value_in_column(colLocation)
        # pprint(valuesLocation)
        lastClearRowLocation=len(valuesLocation)+1

        #or
        # Находим индекс колонки "ЛОКАЦИЯ"
        # header = worksheet.row_values(1)  # Получаем первую строку (заголовки)
        # location_index = header.index("ЛОКАЦИЯ") + 1  # Индекс колонки (начинается с 1)

        return lastClearRowLocation, colLocation
        
    def get_all_triggers(self)->dict:
        """Возвращает все триггеры из таблицы"""
        allValues=self.sheet.get_all_values()
        #удаляем первую строку
        allValues=allValues[1:]
        #удаляем последнюю строку
        # allValues=allValues[:-1]
        triggers={}
        for value in allValues:
            word=value[0]
            promt=value[1]
            triggers[word]=promt
        return triggers
        


if __name__ == '__main__':
    # print('start')  
    s=Sheet('5f6f677a3cd8.json','test_promts','Лист1')
    # print('end')
    pprint(s.get_all_triggers())

   

    # # valuesLocation=s.get_value_in_column(colLocation)
    # lastClearRowLocation, colIndex=s.get_last_clear_row_for_column(col)
    # # pprint(valuesLocation)
    # print(lastClearRowLocation)
    # print(colIndex)

    # s.update_cell(lastClearRowLocation, colIndex, 'test')
    # s.update_cell(2, 1, 'Новый')
    pass