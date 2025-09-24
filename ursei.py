from nicegui import app, ui

from database import Student

@ui.page("/")
def index():
    st1: Student = Student.get(Student.id == 12)

    with ui.row().classes('align-center w-screen h-screen items-center justify-center'):
        with ui.card().style('width: 300px;'):
            ui.label("Студент: " + st1.fam + "!")
            ui.button("Click me!", on_click=lambda d: print(st1.fam))


@ui.page(path="/students")
def students():
    sts = (Student.select(
                Student.id,
                Student.fam, 
                Student.studname,
                Student.age, 
                Student.sex, 
                Student.studgroup)
                .limit(5)
                )

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

    r = [x for x in sts.dicts()]
    with ui.row().classes('align-center w-screen h-screen items-center justify-center'):
        ui.table(columns=cols, rows=r, row_key="id", pagination=3,title="Студенты")



@ui.page("/student")
def student():
    st: Student = Student.get()
    ui.label(text=st.studname + "-"+st.studgroup.name )


print("Starting server...")
ui.run()
