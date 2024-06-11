from nicegui import ui

#!/usr/bin/env python3
import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype

from nicegui import ui

# df = pd.DataFrame(data={
#     'col1': [x for x in range(4)],
#     'col2': ['This', 'column', 'contains', 'strings.'],
#     'col3': [x / 4 for x in range(4)],
#     'col4': [True, False, True, False],
# })

url1="https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv"
df = pd.read_csv(url1,header=0,names=['Index', 'Height', 'Weight'], usecols = [0,1,2])

#https://www.cdc.gov/nccdphp/dnpao/growthcharts/training/bmiage/page5_2.html#:~:text=Formula%3A%20weight%20(lb)%20%2F,in)%5D2%20x%20703&text=Then%2C%20calculate%20BMI%20by%20dividing,a%20conversion%20factor%20of%20703.
#Formula: weight (lb) / [height (in)]2 x 703
df['BMI'] = round(df.Weight / df.Height**2*703,1)

print(df)

def update(*, df: pd.DataFrame, r: int, c: int, value):
    df.iat[r, c] = value #обновляем вес и рост в DF

    newbmi = round(df.iat[r,2] / df.iat[r,1]**2*703,1) #вычисляем BMI c обновленными значениями
    df.iat[r,3]=newbmi #сохраняем обновленный BMI в DF

    bmi_dict[r].content=str(newbmi) #находим в словаре HTML-объект BMI по строке, в к-й обновлялся вес или рост
                                    #и заменяем его контент
    df.to_excel('f.xlsx') #обновляем файл


ui.button('Загрузить файл Excel', on_click=lambda: ui.download('f.xlsx'))
sb=df.BMI
print(df.iloc[[0],[3]]['BMI'][0])



bmi_dict={} #словарь HTML-объектов BMI

# with ui.grid(rows=len(df.index)+1).classes('grid-flow-col mx-8 mt-8'):
#     for c, col in enumerate(df.columns):
#         ui.label(col).classes('font-bold')
#         for r, row in enumerate(df.loc[:, col]):
#             if is_bool_dtype(df[col].dtype):
#                 cls = ui.checkbox
#                 print(cls)
#             elif is_numeric_dtype(df[col].dtype):
#                 cls = ui.number
#                 print(cls)
#             else:
#                 cls = ui.input
#             cls(value=row, on_change=lambda event, r=r, c=c: update(df=df, r=r, c=c, value=event.value))


with ui.grid(rows=len(df.index)+1).classes('grid-flow-col mx-1 mt-1 items-center'):
    for c, col in enumerate(df.columns):
        ui.label(col).classes('font-bold')
        for r, row in enumerate(df.loc[:, col]):
            if c == 0 :
                ui.html(f'{df.iloc[r,c]}',tag='div') #индексы
            elif c == 3: #BMI
                bmi = ui.html(f'{df.iloc[r,c]}').classes('font-semibold text-blue-600 ') #HTML-объект BMI
                bmi_dict[r] = bmi #сохраняем в словаре с ключем текущей строки
            elif c in (1, 2): #рост и вес
                cls = ui.number
                cls(value=row,on_change=lambda event, r=r, c=c: update(df=df, r=r, c=c, value=event.value))

ui.run(uvicorn_logging_level='info')
