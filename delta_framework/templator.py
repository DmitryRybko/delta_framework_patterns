from jinja2.environment import Environment
from jinja2 import FileSystemLoader


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры, передаваемые в шаблон
    :return:
    """

    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)

    # Рендерим шаблон с параметрами
    return template.render(**kwargs)
