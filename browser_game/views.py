from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError, JsonResponse, HttpResponseRedirect, FileResponse, StreamingHttpResponse
from django.contrib.auth import logout, login, authenticate
from forum_adkh_timur.settings import MAIN_PAGE_URL


import os
import sys
import cv2
import time
import pygame
from django.views.decorators import gzip
from osgeo.gdal import GetDriverByName
from osgeo.gdal import Driver, Dataset, Band
from osgeo.gdalconst import GDT_Byte
from osgeo.gdalconst import GCI_RedBand, GCI_GreenBand, GCI_BlueBand

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.environ["SDL_VIDEODRIVER"] = "dummy"

CHUNK_SIZE = 1024 ** 3

FRAMERATE = 24
TEMP_RAST = 'temp.tif'
DEST_RAST = 'image.jpeg'
DRIVER = 'GTiff'
JPEG_DRIVER = 'JPEG'
DATATYPE = GDT_Byte
BANDS = 3
RASTERX = 560
RASTERY = 720
COLORSET = (GCI_RedBand, GCI_GreenBand, GCI_BlueBand)


def game():
    pygame.init()
    pygame.font.init()

    size = width, height = 560, 720
    speed = [2, 2]
    black = 0, 0, 0
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(size)

    ball = pygame.image.load("/home/timur/PyCharm/Django/forum_adkh_timur/browser_game/intro_ball.gif")
    ballrect = ball.get_rect()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]
        fps = clock.get_fps()
        tims = pygame.font.Font.render(font, '%.0f' % fps, True, (255, 255, 0))

        screen.fill(black)
        screen.blits(((ball, ballrect), (tims, (0, 0))), doreturn=True)

        arr = pygame.surfarray.array3d(screen)
        _, jpeg = cv2.imencode('.jpeg', arr)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        pygame.display.flip()
        clock.tick(FRAMERATE)


def index(request):
    return render(request, 'browser_game_page.html')


def browser_game(request):

    response = StreamingHttpResponse((portion for portion in game()),
                                     content_type="multipart/x-mixed-replace;"
                                                  "boundary=frame")

    return response
