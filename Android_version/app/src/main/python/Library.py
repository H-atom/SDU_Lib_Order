import datetime

import requests
from lxml import etree
import prettytable as pt
import time

user_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"
host = "seat.lib.sdu.edu.cn"
date = time.strftime('%Y-%#m-%#d', time.localtime())
next_day = (datetime.datetime.now() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")

def room_lists(i,back):
    day_name = i
    # 获取软件园馆所有房间的信息
    if day_name == 0:
        room_url = "http://seat.lib.sdu.edu.cn/api.php/v3areas/85"
        room_headers = {
            "Cookie": f"Hm_lvt_f38ce10fcdb590711258afeff4dba5a1=1663037747,1664457580; Hm_lpvt_f38ce10fcdb590711258afeff4dba5a1=1664457580; PHPSESSID=ST-402575-QhJKhaAO7oWdsTqATiaY-cas; redirect_url=%2Fweb%2Fseat2%2Farea%2F85%2Fday%2F{date}",
            "Host": host,
            "Referer": f"http://seat.lib.sdu.edu.cn/web/seat2/area/85/day/{date}",
            "User-Agent": user_Agent
        }
    else:
        room_url = f"http://seat.lib.sdu.edu.cn/api.php/v3areas/85/date/{next_day}"
        room_headers = {
            "Cookie": f"Hm_lvt_f38ce10fcdb590711258afeff4dba5a1=1663037747,1664457580; Hm_lpvt_f38ce10fcdb590711258afeff4dba5a1=1664457580; PHPSESSID=ST-402575-QhJKhaAO7oWdsTqATiaY-cas; redirect_url=%2Fweb%2Fseat2%2Farea%2F85%2Fday%2F{next_day}",
            "Host": host,
            "Referer": f"http://seat.lib.sdu.edu.cn/web/seat2/area/85/day/{next_day}",
            "User-Agent": user_Agent
        }
    room_table = pt.PrettyTable()
    room_table.field_names = ['编号', '名称', '可使用座位']
    room_response = requests.get(url=room_url, headers=room_headers)
    room_list = room_response.json()['data']['list']['childArea']

    for k in room_list:
        room_table.add_row([k['id'], k['name'], int(k['TotalCount']) - int(k['UnavailableSpace'])])

    if back == 0:
        return room_table
    else:
        return room_list

def space_lists(i,number, back):
    day_name = i
    # 获取软件园馆所有房间的信息
    if day_name == 0:
        room_url = "http://seat.lib.sdu.edu.cn/api.php/v3areas/85"
        room_headers = {
            "Cookie": f"Hm_lvt_f38ce10fcdb590711258afeff4dba5a1=1663037747,1664457580; Hm_lpvt_f38ce10fcdb590711258afeff4dba5a1=1664457580; PHPSESSID=ST-402575-QhJKhaAO7oWdsTqATiaY-cas; redirect_url=%2Fweb%2Fseat2%2Farea%2F85%2Fday%2F{date}",
            "Host": host,
            "Referer": f"http://seat.lib.sdu.edu.cn/web/seat2/area/85/day/{date}",
            "User-Agent": user_Agent
        }
    else:
        room_url = f"http://seat.lib.sdu.edu.cn/api.php/v3areas/85/date/{next_day}"
        room_headers = {
            "Cookie": f"Hm_lvt_f38ce10fcdb590711258afeff4dba5a1=1663037747,1664457580; Hm_lpvt_f38ce10fcdb590711258afeff4dba5a1=1664457580; PHPSESSID=ST-402575-QhJKhaAO7oWdsTqATiaY-cas; redirect_url=%2Fweb%2Fseat2%2Farea%2F85%2Fday%2F{next_day}",
            "Host": host,
            "Referer": f"http://seat.lib.sdu.edu.cn/web/seat2/area/85/day/{next_day}",
            "User-Agent": user_Agent
        }
    room_table = pt.PrettyTable()
    room_table.field_names = ['编号', '名称', '可使用座位']
    room_response = requests.get(url=room_url, headers=room_headers)
    room_list = room_response.json()['data']['list']['childArea']
    room_id = number
    segment = 0
    if room_id == "0":
        while True:
            i = False
            for room in room_list:
                if int(room['TotalCount']) - int(room['UnavailableSpace']) > 0:
                    room_id = room['id']
                    segment = room['area_times']['data']['list'][0]['id']
                    i = True
                    break
            if i:
                break
            else:
                time.sleep(60)
                room_list = room_list(i,1)
    else:
        for k in room_list:
            if k['id'] == int(room_id):
                room_id = k['id']
                segment = k['area_times']['data']['list'][0]['id']
                break
    # 获取所有座位的信息
    day = time.strftime('%Y-%m-%d %H:%M', time.localtime()).split(" ")
    space_headers = {
        "Cookie": f"Hm_lvt_f38ce10fcdb590711258afeff4dba5a1=1663037747,1664457580; PHPSESSID=ST-459777-EruD4eJtb46ciBYBt4nA-cas; redirect_url=%2Fweb%2Fseat2%2Farea%2F85%2Fday%2F{date}",
        "User_Agent": user_Agent,
        "Host": host,
        "Referer": f"http://seat.lib.sdu.edu.cn/web/seat3?area={room_id}&segment={segment}&day={date}&startTime={day[1]}&endTime=22:30"
    }
    if i == 0:
        times = day[1].split(":")
        space_url = f"http://seat.lib.sdu.edu.cn/api.php/spaces_old?area={room_id}&segment={segment}&day={day[0]}&startTime={times[0]}%3A{times[1]}&endTime=22%3A30"
    else:
        space_url = f"http://seat.lib.sdu.edu.cn/api.php/spaces_old?area={room_id}&segment={segment}&day={next_day}&startTime=08%3A00&endTime=22%3A30"

    space_response = requests.get(url=space_url, headers=space_headers)
    space_list = space_response.json()['data']['list']

    space_table = pt.PrettyTable()
    space_table.field_names = ['编号', '名称', '所属区域', '状态', '状态名']
    if space_list is not None:
        for space in space_list:
            if space['status'] == 1:
                space_table.add_row([space['id'], space['name'], space['area_name'], space['status'], space['status_name']])

    if back == 0:
        return space_table
    elif back == 1:
        return space_list
    else:
        return segment

def back():
    php_url = "http://seat.lib.sdu.edu.cn/cas/index.php?callback=http://seat.lib.sdu.edu.cn/home/web/seat/area/84"
    php_headers = {
        "Refer": "http://seat.lib.sdu.edu.cn/home/web/seat/area/84",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.34",
    }
    php_response = requests.get(url=php_url, headers=php_headers)
    result = etree.HTML(php_response.text)
    lt = result.xpath('//*[@id="lt"]/@value')
    return lt[0]

def book(i,number,id,username,password,is_random,str_enc,lt):
    space_list = space_lists(i,number,1)
    segment = space_lists(i,number,2)

    # 获取登陆后的access_token
    service_url = "https://pass.sdu.edu.cn/cas/login?service=http%3A%2F%2Fseat.lib.sdu.edu.cn%2Fcas%2Findex.php%3Fcallback%3Dhttp%3A%2F%2Fseat.lib.sdu.edu.cn%2Fhome%2Fweb%2Fseat%2Farea%2F84"
    service_headers = {
        "User_Agent": user_Agent,
        "Cookie": "Language=zh_CN;",
        "Host": "pass.sdu.edu.cn",
        "Referer": "http://seat.lib.sdu.edu.cn/"
    }
    session = requests.session()
    service_response = session.get(url=service_url, headers=service_headers)
    service_cookie = service_response.cookies
    JSESSIONID = service_cookie.get("JSESSIONID")
    cookie_adx = service_cookie.get("cookie-adx")
    strEnc = str_enc[1:-1]
    service_data = {
        "rsa": str(strEnc),
        "ul": str(len(username)),
        "pl": str(len(password)),
        "lt": str(lt),
        "execution": "e1s1",
        "_eventId": "submit"
    }

    service_response1 = session.post(url=service_url, data=service_data, allow_redirects=False)
    service_cookie1 = service_response1.cookies
    location = service_response1.headers.get("Location")

    index_response = session.get(url=location)
    access_token = index_response.cookies.get("access_token")
    user_name = index_response.cookies.get("user_name")
    userid = index_response.cookies.get("userid")
    expire = index_response.cookies.get("expire")

    space_id = 0
    if is_random == 0:
        space_id = id
    else:
        for k in space_list:
            if k['status'] == 1:
                space_id = k['id']
                break

    day = time.strftime('%Y-%m-%d %H:%M', time.localtime()).split(" ")
    start_time = time.strftime('%H:%M', time.localtime())
    book_url = f"http://seat.lib.sdu.edu.cn/api.php/spaces/{space_id}/book"
    book_headers = {
        "Host": host,
        "User-Agent": user_Agent,
        "Cookie": f"Hm_lvt_f38ce10fcdb590711258afeff4dba5a1=1663037747,1664457580; redirect_url=%2Fweb%2Fseat2%2Farea%2F85%2Fday%2F2022-10-1; PHPSESSID=ST-460188-9NLCDvogr0mRdl57PkNJ-cas; userid={userid}; user_name={user_name}; access_token={access_token}; expire={expire}",
        "Referer": f"http://seat.lib.sdu.edu.cn/web/seat3?area={number}&segment={segment}&day={day}&startTime={start_time}&endTime=22:30",
        "Origin": "http://seat.lib.sdu.edu.cn"
    }
    book_data = {
        "access_token": str(access_token),
        "userid": str(userid),
        "segment": str(segment),
        "type": "1",
        "operateChannel": "2"
    }

    book_response = session.post(url=book_url, data=book_data, headers=book_headers)
    book_data = book_response.json()
    print(book_data)
    if book_data['status'] == 1:
        return book_data['data']['list']['spaceInfo']['areaInfo']['nameMerge'] + book_data['msg']
    else:
        return book_data['msg']
