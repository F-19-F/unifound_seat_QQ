# 代理服务器
ProxyHost = ''
RealHost = '10.240.32.6:8099'
SeatFile = 'Seats.json'


import json
import os
filepath = os.path.join(os.path.dirname(__file__),SeatFile)
def getHost():
    global ProxyHost, RealHost
    if ProxyHost:
        return ProxyHost
    else:
        return RealHost


def loadSeatid(filename=filepath):
    f = open(filename, 'r', encoding='utf-8')
    data = f.read()
    f.close()
    result = json.loads(data)
    return result


SeatId = loadSeatid()
