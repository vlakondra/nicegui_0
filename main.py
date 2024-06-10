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

df['BMI'] = round(df.Weight / df.Height**2*703,1)

print(df)
# df.to_excel('f.xlsx')

def update(*, df: pd.DataFrame, r: int, c: int, value):
    df.iat[r, c] = value
    df.iat[r,3]=round(df.iat[r,1] / df.iat[r,2]**2*703,1)
    df.to_excel('f.xlsx')
    print("DF",df)
    ui.notify(f'Set ({r}, {c}) to {value}')


ui.button('Загрузить файл Excel', on_click=lambda: ui.download('f.xlsx'))

ui.html('This is <u>emphasized</u>.', tag='em')

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


with ui.grid(rows=len(df.index)+1).classes('grid-flow-col mx-8 mt-8'):
    for c, col in enumerate(df.columns):
        ui.label(col).classes('font-bold')
        for r, row in enumerate(df.loc[:, col]):
            if c==0 :
                ui.html(f'{df.iloc[r,c]}',tag='div')
                # print('?',df.iloc[r,c])
            elif c==3:
                ui.html(f'{df.iloc[r,c]}',tag='div')
            elif c > 0 and c < 3:
                cls = ui.number
                cls(value=row,on_change=lambda event, r=r, c=c: update(df=df, r=r, c=c, value=event.value))
            # else:
            #     print(555)
            #     cls = ui.input

            #cls(value=row)




ui.run(uvicorn_logging_level='info')
