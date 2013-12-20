# -*- coding:utf-8 -*-

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from binbox.utils.filehelper import FileHelper
from binbox.utils.lingr import LingrBot
from settings import SETTINGS

import os
import dircache
import codecs
import json
import urllib

STATIC_FILE_THUMB = "/static/thumb/"
STATIC_FILE_PDF = "/static/pdf/"

@view_config(route_name='home', renderer='index.mak')
def index(request):
    here = os.path.dirname(__file__)
    
    _raw_filelist = dircache.listdir(here + STATIC_FILE_PDF)
    filelist = _gen_filelist(_raw_filelist)

    return {"books": filelist,
            "mode": "thumb"}

@view_config(route_name='list', renderer='index.mak')
def list(request):
    here = os.path.dirname(__file__)

    _raw_filelist = dircache.listdir(here + STATIC_FILE_PDF)
    filelist = _gen_filelist(_raw_filelist)

    return {"books": filelist,
            "mode": "list"}

@view_config(route_name='api_list')
def api_list(request):
    here = os.path.dirname(__file__)
    _raw_filelist = dircache.listdir(here + STATIC_FILE_PDF)
    return Response(
        json.dumps(_raw_filelist))


@view_config(route_name='api_file')
def api_file(request):
    target_file = request.GET.get('target')
    here = os.path.dirname(__file__)
    thumbfile = FileHelper(target_file)
    return Response(
        json.dumps(thumbfile.get_thumb()))

@view_config(route_name='post', renderer='index.mak')
def post(request):
    here = os.path.dirname(__file__)

    filename = request.POST['pdf'].filename
    input_file = request.POST['pdf'].file
    
    file_path = here + STATIC_FILE_PDF + filename
    output_file = open(file_path, 'wb')

    input_file.seek(0)

    while 1:
        data = input_file.read(2<<16)
        if not data:
            break
        output_file.write(data)
    output_file.close()
    
    bot = LingrBot(
        SETTINGS.ROOM, SETTINGS.NAME, SETTINGS.SECRET)
    bot.do_post("新規 :: " + filename.encode('utf-8'))

    _raw_filelist = dircache.listdir(here + STATIC_FILE_PDF)
    
    target_filelist = []
    for target_file in _raw_filelist:
        if re.compile('\.pdf').match(target_file):
            target_file.appened(target_file)
    _raw_filelist = target_filelist

    filelist = _gen_filelist(_raw_filelist)
    url = request.route_url('home')
    return HTTPFound(location=url)

def _gen_filelist(filelist):
    return_array = []
    for item in filelist:
        return_array.append(
            FileHelper(item,True))
    return return_array
