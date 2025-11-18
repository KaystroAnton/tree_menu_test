from django.conf import settings
from django.shortcuts import render
from menu.models import MenuItem

def show_menu(request):
    del_all(MenuItem)
    if not MenuItem.objects.all():
        creat_table(MenuItem)
    return render(request, "menu/menu.html")

def creat_table(model):
    menu = model.objects.create(name="menu",url = 'http://127.0.0.1:8000/00',url_name = 'localhost')
    menu2 = model.objects.create(name="menu2", url='menu2')
    menu3 = model.objects.create(name="menu3", url='menu3')
    main2 = model.objects.create(name="Главная2", parent=menu ,url='main2')
    main1 = model.objects.create(name="Главная",parent=menu ,url = 'http://127.0.0.1:8000/')
    model.objects.create(name="Магазин", parent=main1, url = 'Магазин')
    model.objects.create(name="О нас", parent=main1,url = 'О_нас')
    model.objects.create(name="menu5",url = 'menu5')
def del_all(model):
    for obj in model.objects.all():
        obj.delete()
