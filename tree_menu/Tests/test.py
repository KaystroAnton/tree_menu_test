from menu.models import Menu
main1 = Menu.objects.create(name="Главная")
shop = Menu.objects.create(name="Магазин")
Menu.objects.create(name="О нас", parent=main1)
Menu.objects.create(name="Каталог", parent=shop)