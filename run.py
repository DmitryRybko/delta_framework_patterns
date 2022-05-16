from wsgiref.simple_server import make_server
from delta_framework.main import Framework
# from urls import routes
from views import routes
from settings import server_port

# WSGI application object
application = Framework(routes)

with make_server('', server_port, application) as httpd:
    print(f'Сервер запущен на порту {server_port}')
    httpd.serve_forever()
