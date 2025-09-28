from nicegui import app, ui

from database import Student

@ui.page("/")
def index():

    lbl = ui.label(text="Привет, Урсэи!")
    stt =Student.get()
    lbl.text = stt.fam

    ui.link('Студенты',target='students')
    ui.link('Студент',target='student')


@ui.page(path="/students")
def students():
    #подготовка данных
    
    #выполним запрос к бд
    sts = (Student.select(
                Student.id,
                Student.fam, 
                Student.studname,
                Student.age, 
                Student.sex, 
                Student.studgroup)
                .limit(5)
                )

    #определяем столбцы таблицы
    cols = [
        {"name": "id", "label": "ID", "field": "id", "sortable": False},
        {"name": "fam", "label": "Фамилия", "field": "fam", "sortable": True},
        {"name": "studname", "label": "Имя", "field": "studname", "sortable": True},
        {"name": "sex", "label": "Пол", "field": "sex", "sortable": True},
        {"name": "age", "label": "Возраст", "field": "age", "sortable": True},
        {
            "name": "studgroup",
            "label": "Группа",
            "field": "studgroup",
            "sortable": True,
        },
    ]

    studData = [x for x in sts.dicts()]
    #Подставляем имя группы вместо id
    for x in studData:
        x['studgroup'] = Student.get(x['id']).studgroup.name  

    #Данные готовы
    
    #Создаем интерфейс пользователя
    with ui.column().style('margin:auto').classes('align-center  h-screen items-center justify-center'):
        def updateDialog():
            if not stdTable.selected:
                 sendMessage("Выберите студента")
                 return
            with ui.dialog() as dialog1, ui.card():
                with ui.column().classes("h-120 w-80 justify-start"):
                    faminp=ui.input(label='Фамилия',
                            value=stdTable.selected[0]['fam'],
                            validation={'Слишком длинная фамилия': lambda value: len(value) < 10}).style('width:100%')
                    nameinp=ui.input(label='Имя',
                            value=stdTable.selected[0]['studname'],
                            validation={'Слишком длинное имя': lambda value: len(value) < 10}).style('width:100%')
               
                    with ui.row().style("width:100%").classes('justify-center'):
                            ui.button('Отмена', icon='close', on_click=dialog1.close)
                            ui.button('Сохранить', icon='done',
                                      on_click=lambda :(
                                                        updateRow(fam=faminp.value,
                                                                   name=nameinp.value),
                                                        dialog1.close(),
                                                        stdTable.selected.clear(),
                                                        ))

            dialog1.open()      


        def delDialog():
            '''
            Диалог подтверждения удаления \n
            Вызывается при нажатии кнопки Удалить, если выбрана строка
            '''
            if not stdTable.selected:
                 sendMessage("Выберите студента")
                 return
            
            with ui.dialog() as dialog2, ui.card():
                with ui.column().classes("h-30 justify-between"):
                    ui.restructured_text(f"""
                                        Вы действительно хотите удалить студентa

                                        **{stdTable.selected[0]['fam']}** **{stdTable.selected[0]['studname']}**?
                                        """)
                    ui.label(" ",)

                    with ui.row().style("width:100%").classes('justify-between'):
                            ui.button('Отмена', icon='close', on_click=dialog2.close)
                            ui.button('Удалить', icon='done',
                                      on_click=lambda :(
                                                        removeRow(),
                                                        dialog2.close()
                                                        ))
                #Диалог открывается при вызове функции delDialog
                dialog2.open()

        def updateRow(fam,name):
             '''Обновление записи в базе'''

             st = Student.get(stdTable.selected[0]['id'])

             st.fam = fam
             st.studname = name
             st.save()
             
             #обновление строки в таблице
             #фильтруем по ID источник данных таблицы
             flt = list(filter(lambda x: x['id'] == st.id, studData))[0]
             #и обновляем поля в источнике
             flt['fam'] = fam
             flt['studname'] = name

             stdTable.update() #обновляем таблицу

        def removeRow():
            #удаление записи из базы
            delstd = Student.get(stdTable.selected[0]['id']).delete_instance()
            #удаление строки из таблицы
            stdTable.remove_rows(stdTable.selected)
            sendMessage("Студент удален!")

        #Выводим таблицу с данными  
        stdTable = ui.table(columns=cols, rows=studData, row_key="id",
                  pagination=3,title="Студенты",
                  selection='single')     
        
        #Под таблицей - кнопки вызова диалогов изменения и удаления
        with ui.row().style("width: 100%; justify-content: flex-end;"):
            ui.button(text="Изменить",on_click=updateDialog )
            ui.button(text="Удалить", on_click=delDialog)

    def sendMessage(text):
        """Вывод сообщений в нижней части экрана"""
        if text:
            ui.notify(  
                    text,
                    type="warning",
                    timeout=2000,
                )




@ui.page("/student")
def student():
    st: Student = Student.get()
    ui.label(text= f'{st.fam}  {st.studname}  Группа: {st.studgroup.name}' )


print("Starting server...")
ui.run()
