from nicegui import app, ui

from database import Student


@ui.page("/")
def index():
    st1: Student = Student.get()
    with ui.card(align_items="center"):
        ui.label("Hello, " + st1.fam + "!")
        ui.button("Click me!", on_click=lambda: print("Clicked!"))


@ui.page(path="/students")
def students():
    sts = Student.select(Student.id,Student.fam, Student.studname,Student.age, Student.sex, Student.studgroup).limit(5)
    d = sts.dicts()[0]
    print(d.keys())
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
    # for z in sts:
    #     print(z.studname, z.studgroup.name)
    ui.table(columns=cols,rows=r, row_key="id",pagination=3)


@ui.page("/student")
def student():
    st: Student = Student.get()
    ui.label(text=st.studname + "-"+st.studgroup.name )
    print(st.fam + "-" + st.studgroup.name)


print("Starting server...")


ui.run()
