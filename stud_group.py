from nicegui import app, ui
from database import Student, Group

def StudentsByGroup(grp_id):
    '''Возвращает список студентов по выбранной группе.\n
    Вызывается при изменении группы в выпадающем списке,\n
    а также при запуске приложения'''

    std = (Student
       .select(Student.id,
               Student.fam.alias('Фамилия'),
               Student.studname.alias('Имя'),
               Student.age.alias('Возраст'),
               Student.studgroup)
       .where(Student.studgroup == grp_id)
       )
    #строим список словарей с данными студентов
    studData = [x for x in std.dicts()]
    return studData

#центрируем контент
nc = ui.query('.nicegui-content')
st = '''background:lightblue;
        width:100%;
        height:100vh;
        align-items:center;
        justify-content:center'''

nc.style(st)

#Получаем список групп
grp = Group.select(Group.id, Group.name)

#Поскольку данные для выпадающего списка - словарь
#приходится его строить
gd={}
for g in grp:
    gd[g.id]=g.name

#выводим выпадающий список с группами
#группа по умолчанию с индексом 5. M.б. любая
with ui.card().style("margin:auto"):
    ui.select(gd, 
            value=list(gd.keys())[5], 
            on_change = lambda e:(
                new_stdata := StudentsByGroup(e.value),
                stdTable.rows.clear(),
                #получаем новые данные, и передаем их в таблицу    
                stdTable.rows.extend(new_stdata),
                stdTable.update()
                ))

    #Выводим таблицу со студентами
    #содержание таблицы зависит от выбранной группы
    stdTable = ui.table( rows=StudentsByGroup(list(gd.keys())[5]),
                    row_key="id",
                    title="Студенты",
                    pagination=3,
                    selection='single')  


ui.run()