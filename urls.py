# import views
# import inspect

"""
Связывает пути и контроллеры автоматически. Путь формируется как lowercase название соответствующего класса. 
"""

routes = {}

# routes = {f'/': views.Index()}
#
# for name, obj in inspect.getmembers(views):
#     if inspect.isclass(obj):
#         if name == "Debug":
#             continue
#         elif name == "DebugAlt":
#             continue
#         elif name == "DebugNew":
#             continue
#         routes[f'/{name.lower()}/'] = obj()
