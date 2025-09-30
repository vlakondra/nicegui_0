from nicegui import app, ui


# ui.add_css('''
#     .red {
#         background: red;
#            color:white;
#            margin:30px;
#            padding:10px;
#     }
# ''')

# nc = ui.query('.nicegui-content')

# st='''background:lightblue;
#     width:100%;
#     height:100vh;
#     align-items:center;
#     justify-content:center'''

# def main():
#     nc.style(st)
#     with ui.card():
#         with ui.row(align_items='stretch'):
#             for n in range(9):
#                 with ui.card():
#                     ui.label(f'текст-{n}').classes('red')



print("Starting server...")

def main():
    var ="my text"
    ui.label(var)
    ui.label(var+var)

main()
ui.run()