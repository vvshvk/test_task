import numpy as np
import matplotlib.colors as colors
import re
from PIL import Image

from django.http import JsonResponse
from django.shortcuts import render
from .forms import ImageForm

# формат HEX-кода цвета
hx = re.compile(r'[a-fA-F0-9]{6}$')


# функция проверки на соответствие HEX-формату
def ishxcolor(value):
    return bool(hx.match(value))


def main(request):
    form = ImageForm()
    return render(request, 'pixels/main.html', {'form': form})


def upload_img(request):
    #загрузка картинок пользователями
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # получаем текущую картинку для демонстрации в шаблоне
            img_obj = form.instance
            img = img_obj.image.path
            # получаем количество черных и белых пикселей
            black, white = count_px(img)
            result_hex = -1
            return render(request, 'pixels/image.html',
                          {'img_obj': img_obj.image.url, 'black': black, 'white': white, 'img': img,
                           'count_hex': result_hex})
    else:
        form = ImageForm()
    return render(request, 'pixels/.html', {'form': form})


def count_px(p):
    img = Image.open(p, 'r')
    # конвертируем картинку в массив RGB-формата пикселей
    im = np.array(img.convert('RGB'))
    white = [255, 255, 255]
    black = [0, 0, 0]
    # проверяем все пиксели в картинке на соответствие выбранным цветам и считаем их количество
    result_black = np.count_nonzero(np.all(im == black, axis=2))
    result_white = np.count_nonzero(np.all(im == white, axis=2))
    return (result_black, result_white)


def count_hex(request):
    hex_color = request.POST.get('hex')
    p = request.POST.get('path')
    url = request.POST.get('url')
    black = request.POST.get('black')
    white = request.POST.get('white')
    img = Image.open(p, 'r')
    # конвертируем картинку в массив RGB-формата пикселей
    img = np.array(img.convert('RGB'))
    if ishxcolor(hex_color):
        hex_color = '#' + hex_color
        # переводим из формата HEX в RGB
        current_color = colors.hex2color(hex_color)
        # переводим из RGB формата [0.0-1.0] в формат RGB [0-255]
        current_color = list([int(255 * x) for x in current_color])
        # проверяем все пиксели в картинке на соответствие выбранным цветам и считаем их количество
        res_hex = np.count_nonzero(np.all(img == current_color, axis=2))
        result_hex = 'color: ' + str(res_hex)
        return render(request, 'pixels/image.html',
                      {'black': black, 'white': white, 'img': p, 'img_obj': url, 'count_hex': result_hex})
    else:
        return render(request, 'pixels/image.html',
                      {'black': black, 'white': white, 'img': p, 'img_obj': url, 'count_hex': 'hex code is invalid'})
