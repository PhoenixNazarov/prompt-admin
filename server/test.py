from jinja2 import Template

# Определите шаблон template1
template1 = """{{ name|default("Unknown") }}"""

# Определите шаблон template2
template2 = Template("""Template1: {{ template(template1) }}""")

# Установите значение переменной name
name = "John"

fill = {
    'template1': template1,
    'name': 'John'
}

def template(source: str):
    return Template(source).render(**fill)

# Отрендерите template2 и выведите результат
result = template2.render(**fill, template=template)
print(result)
