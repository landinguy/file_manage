import json
import os
import traceback as tb
from datetime import datetime

from Crypto.Cipher import AES
from django.http import HttpResponse, FileResponse
from django.utils.encoding import escape_uri_path

import logger
from dev import uploadPath
from .db import session, add
from .encrypt import en, de, en2, de2
from .entity import User, File, FidUid
from .util import Result, dump, get_uuid

log = logger.get()
model = AES.MODE_ECB
sk = ord('b')


def login(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    log.info("用户登录,username#%s,password#%s" % (username, password))
    user = session.query(User).filter_by(username=username, password=password).first()
    if user:
        return HttpResponse(dump(Result(data={'username': user.username, 'uid': user.id, 'role': user.role})))
    return HttpResponse(dump(Result(code=-1, msg='账号或者密码错误')))


def logout(request):
    return HttpResponse(dump(Result()))


def register(request):
    params = json.loads(request.body)
    log.info('用户注册,params#%s' % params)
    username = params['username']
    password = params['password']
    user = session.query(User).filter_by(username=username).first()
    if user:
        return HttpResponse(dump(Result(code=-1, msg='账号已存在！')))
    add(User(username=username, password=password, role='NORMAL'))
    return HttpResponse(dump(Result()))


def files(request):
    params = json.loads(request.body)
    log.info('查询文件,params#%s' % params)
    result = Result()
    try:
        query = session.query(FidUid)
        uid = params['uid']
        user = session.query(User).filter_by(id=uid).first()
        if user.role != 'ADMIN':
            query = query.filter_by(uid=uid)

        fid_list = {x.fid for x in query.all()}
        log.info('fid_list#%s' % fid_list)

        file_query = session.query(File).filter(File.id.in_(fid_list))
        total = file_query.count()
        page_size = params['pageSize']
        page_no = params['pageNo']
        data = file_query.order_by(File.id.desc()).offset((page_no - 1) * page_size).limit(page_size).all()
        list = [{'id': x.id, 'name': x.name, 'size': x.size, 'create_ts': x.create_ts, 'encryption_type': x.encryption_type} for x in data]
        result.data = {'list': list, 'total': total}
    except Exception:
        tb.print_exc()
        result.code = -1
        result.msg = '文件查询失败'
    return HttpResponse(dump(result))


def share(request):
    params = json.loads(request.body)
    log.info('共享文件,params#%s' % params)
    result = Result()
    try:
        add(FidUid(fid=params['fid'], uid=params['uid']))
    except Exception:
        tb.print_exc()
        result.code = -1
        result.msg = '文件共享失败'
    return HttpResponse(dump(result))


def upload(request):
    file = request.FILES.get("file")
    if not file:
        return HttpResponse(dump(Result(code=-1, msg='上传文件不能为空！')))

    try:
        filename = file.name
        size = file.size
        byte = file.read()
        private_key = None
        content = None

        encryption_type = int(request.POST.get('encryption_type'))
        uid = request.POST.get('uid')
        log.info('上传文件,filename#%s,encryption_type#%s,uid#%s' % (filename, encryption_type, uid))

        # log.info('before encode---#%s' % byte)
        # st = datetime.now().timestamp()
        # 加密方式一
        if encryption_type == 1:
            content = en(byte)

        # 加密方式二
        else:
            content = en2(sk, byte)
        # et = datetime.now().timestamp()
        # log.info('after encode---#%s' % content)
        # log.info('time---#%s' % (et - st))
        uuid = get_uuid() + '.fm'
        path = uploadPath + uuid
        with open(path, 'wb') as it:
            it.write(content)

        # et2 = datetime.now().timestamp()
        # log.info('time2---#%s' % (et2 - et))
        create_ts = str(datetime.today().replace(microsecond=0))
        f = File(name=filename, uid=uid, size=size, create_ts=create_ts, content=path, encryption_type=encryption_type, private_key=private_key)
        add(f)
        add(FidUid(fid=f.id, uid=uid))
    except Exception:
        tb.print_exc()
        return HttpResponse(dump(Result(code=-1, msg='上传文件失败！')))
    return HttpResponse(dump(Result()))


def download(request):
    id = request.GET.get('id')
    log.info('下载文件,id#%s' % id)
    try:
        select = session.query(File).filter_by(id=id).first()
        if not select:
            return HttpResponse(dump(Result(code=-1, msg='文件不存在！')))
        else:
            encryption_type = select.encryption_type
            filename = select.name
            content = None
            with open(select.content, 'rb') as it:
                content = it.read()
                # log.info('before decode---#%s' % content)
                if encryption_type == 1:
                    content = de(content)
                else:
                    content = de2(sk, content)

            # log.info('after decode---#%s' % content)
            temp_path = uploadPath + 'temp/'
            if not os.path.exists(temp_path):
                os.makedirs(temp_path)

            # 生成解密文件
            file_path = temp_path + filename
            with open(file_path, 'wb') as it:
                it.write(content)

            file = open(file_path, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename=%s' % escape_uri_path(filename)
            return response
    except IOError:
        tb.print_exc()
