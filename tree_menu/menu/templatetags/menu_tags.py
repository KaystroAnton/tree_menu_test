from django import template
from django.urls import reverse, NoReverseMatch
from django.utils.safestring import mark_safe

from menu.models import MenuItem

register = template.Library()

# Получает дерево в виде списка
def get_tree_recursive(nodes, array):
    for node in nodes:
        array.append(node)
        if node.children.exists:
            get_tree_recursive(node.children.all(),array)
# Перестраивает дерева таким образом(root -> child -> child ... ->active_node) возвращает список, всех предков активного нода
def get_ancestors(active_node):
    new_tree = []
    if active_node.parent is not None:
        temporary_parent = active_node.parent
        while temporary_parent is not  None:
            new_tree.insert(0,temporary_parent)
            temporary_parent = temporary_parent.parent
    new_tree.append(active_node)
    return new_tree

# Рендер меню
def render_menu(menu_items, active_node, level = 0):
    item = menu_items[level]
    menu_html = '<ul>'
    menu_html += '<li>'
    if item is active_node:
        menu_html += f'<p> {item.name} </p>'
        menu_html += '<ul>'
        for child in item.children.all():
            menu_html += '<li>'
            menu_html += f'<a href="{child.get_item_url()}">{child.name}</a>'
        menu_html += '<ul>'
    else:
        menu_html += f'<a href="{item.get_item_url()}">{item.name}</a>'
        print(menu_items, active_node, level+1)
        menu_html += render_menu(menu_items, active_node, level+1)
    menu_html += '</li>'
    menu_html += '</ul>'
    return menu_html

# Тег для определения URL пункта меню
@register.simple_tag(name='get_url')
def get_item_url(item):
    if item.url:
        return item.url
    elif item.named_url:
        try:
            return reverse(item.named_url)
        except NoReverseMatch:
            return "#invalid-url"
    return

# Тег для определения полного URL страницы
@register.simple_tag(name = 'current_path',takes_context=True)
def get_current_path(context):
    return context.request.build_absolute_uri()

# Рекурсивное отображение дерева
@register.inclusion_tag('menu/render_recursive_full.html')
def render_recursive_full(nodes):
    return {'nodes': nodes}

@register.inclusion_tag('menu/render_recursive.html')
def render_recursive(nodes, active_node,level = 0):
    return {'nodes': nodes, 'active_node': active_node, 'level': level}

# Отображение ВСЕГО меню
@register.inclusion_tag('menu/show_full_menu.html',name = 'draw_full_menu')
def show_full_menu(menu_name=None,menu = None):
    if menu is None:
        menu = MenuItem.objects.filter(name=menu_name).select_related('parent')
        if len(menu) == 0:
            raise NameError('No menu with name- ',menu_name)
    return {'menu': menu}

# отображение меню
@register.simple_tag(name = 'draw_menu', takes_context=True)
def draw_menu(context,menu_name):
    current_path = context.request.build_absolute_uri()

    # Получили QuerySet одним запросом
    menu = MenuItem.objects.filter(name=menu_name).select_related('parent')
    if len(menu) == 0:
        raise NameError('No menu with name- ',menu_name)
    item_map=[]
    get_tree_recursive(menu,item_map)

    # Определение активного пункта и построение дерева
    ancestors = []
    active_node = None
    for item in item_map:
        if current_path == 'http://localhost:8000/': # Костыль, чтобы localhost корректно обрабатывался
            current_path =  'http://127.0.0.1:8000/'
        print("check urls ", current_path, "  ", item.get_item_url())
        if item.get_item_url() == current_path:
            ancestors=get_ancestors(item)
            active_node = item


    return mark_safe(render_menu(ancestors,active_node))


