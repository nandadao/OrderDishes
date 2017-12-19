from django.shortcuts import render
from checkstand.models import Menu, Kind
from django.http import HttpResponse

from PIL import Image
from django.conf import settings
import os


# Create your views here.
# 页面

def index(request):
    kinds = Kind.objects.all
    menus = Menu.objects.all()
    return render(request, 'checkstand/menumanage.html', locals())


def kind_index(request):
    kinds = Kind.objects.all()
    menus = Menu.objects.all()
    return render(request, 'checkstand/menukindmanage.html', locals())


# 增删改菜单action
def create_menu_action(request):
    name = request.POST.get('name', 'NAME')  # 如果为空则默认为NAME
    price = request.POST.get('price', 'PRICE')
    kind_name = request.POST.get('kind_name')
    kind = Kind.objects.get(name=kind_name)
    img = request.FILES.get('img')
    path = os.path.join(settings.MEDIA_ROOT, 'images', img.name)
    with open(path, 'wb') as pic:
        for p in img.chunks():
            pic.write(p)
    Menu.objects.create(name=name, price=price, kind=kind, img='images/%s' % img.name)
    kinds = Kind.objects.all
    menus = Menu.objects.all()
    return render(request, 'checkstand/menumanage.html', {'kinds': kinds, 'menus': menus})


def update_menu_action(request):
    id = request.POST.get('id')
    name = request.POST.get('name')
    price = request.POST.get('price')
    try:
        img = request.FILES.get('img')
        path = os.path.join(settings.MEDIA_ROOT, 'images', img.name)
        with open(path, 'wb') as pic:
            for p in img.chunks():
                pic.write(p)
        Menu.objects.filter(id=id).update(name=name, price=price, img='images/%s' % img.name)
    except AttributeError:
        Menu.objects.filter(id=id).update(name=name, price=price)
    kinds = Kind.objects.all()
    menus = Menu.objects.all()
    return render(request, 'checkstand/menumanage.html', {'kinds': kinds, 'menus': menus})


def delete_menu_action(request):
    id = request.POST.get('id')
    Menu.objects.filter(id=id).delete()
    kinds = Kind.objects.all()
    menus = Menu.objects.all()
    return render(request, 'checkstand/menumanage.html', {'kinds': kinds, 'menus': menus})


# 增删改菜类action
def add_kind_action(request):
    name = request.POST.get('kind_name')
    Kind.objects.create(name=name)
    kinds = Kind.objects.all()
    menus = Menu.objects.all()
    return render(request, 'checkstand/menukindmanage.html', {'kinds': kinds, 'menus': menus})


def delete_kind_action(request):
    name = request.POST.get('kind_name')
    Kind.objects.filter(name=name).delete()
    # kind=Kind.objects.get(name=name)
    # Menu.objects.filter(kind=kind).delete()
    # Kind.objects.filter(name=name).delete()
    kinds = Kind.objects.all()
    menus = Menu.objects.all()
    return render(request, 'checkstand/menukindmanage.html', {'kinds': kinds, 'menus': menus})


def update_kind_action(request):
    oldname = request.POST.get('oldkindname')
    newname = request.POST.get('newkindname')
    Kind.objects.filter(name=oldname).update(name=newname)
    kinds = Kind.objects.all
    menus = Menu.objects.all()
    return render(request, 'checkstand/menukindmanage.html', {'kinds': kinds, 'menus': menus})


def query_ajax(request):
    name = request.POST.get('username')
    Menu.objects.get(name=name)
    return HttpResponse('success')
