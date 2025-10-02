from nicegui import app, ui
from database import Department, Student, Group

# центрируем контент
nc = ui.query(".nicegui-content")
st = """background:lightblue;
        width:100%;
        height:100vh;
        align-items:center;
        justify-content:center"""

nc.style(st)

def GroupsByDepartment(dpr_id):
    """Группы по выбранному факультету"""
    grp = (Group
           .select(Group.id, Group.name)
           .where(Group.department == dpr_id)
    )
    #строим словарь с группами
    gd = {}
    for g in grp:
        gd[g.id] = g.name

    return gd, list(gd.keys())[0]  # ключ 1-й группы

def StudentsByGroup(grp_id):
    """Возвращает список студентов по выбранной группе.\n
    Вызывается при изменении группы в выпадающем списке,\n
    а также при запуске приложения"""

    std = Student.select(
        Student.id,
        Student.fam.alias("Фамилия"),
        Student.studname.alias("Имя"),
        Student.age.alias("Возраст"),
        Student.studgroup,
    ).where(Student.studgroup == grp_id)
    # строим список словарей с данными студентов
    studData = [x for x in std.dicts()]
    return studData

# Получаем список факультетов
dpr = Department.select(Department.id, Department.name)
# словарь для выпадающего списка факультетов
departs = {}
for d in dpr:
    departs[d.id] = d.name

# выводим выпадающиe списки с группами и факультетами
with ui.card().style("margin:auto"):
    with ui.row():
        with ui.column().style("gap:0"):
            ui.label("Факультет:")
            # выпадающий список с факультетами
            dp = ui.select(
                departs,
                value=list(departs.keys())[0],
                on_change=lambda e: (
                    print("фак-т"),
                    new_grpdata := GroupsByDepartment(e.value)[0],
                    st.set_options(new_grpdata),
                    st.set_value(list(new_grpdata.keys())[0]),
                ),
            ).style("height:40px")

        grpdep = GroupsByDepartment(dp.value)
        ui.label("Группы:")
        st = ui.select(
            options=grpdep[0],
            value=grpdep[1],
            on_change=lambda e: (
                print("grp"),
                new_stdata := StudentsByGroup(e.value),
                stdTable.rows.clear(),
                # получаем новые данные, и передаем их в таблицу
                stdTable.rows.extend(new_stdata),
                stdTable.update(),
            ),
        )

    # Выводим таблицу со студентами
    # содержание таблицы зависит от выбранной группы
    stdTable = ui.table(
        rows=StudentsByGroup(st.value),
        row_key="id",
        title="Студенты",
        pagination=3,
        selection="single",
    )

    # ta = ui.textarea("qwerty")
    # stdTable.bind_filter_from( ta,'value')


ui.run()
