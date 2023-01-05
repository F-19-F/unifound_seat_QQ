import requests
import urllib.parse as up
from .config import getHost, SeatId
from .const import *


class wxUser(requests.sessions.Session):
    mMsn: str

    def __init__(self, msn='') -> None:
        super().__init__()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53"}
        self.mMsn = msn

    def _baseScanget(self, url):
        res = self.get(url, allow_redirects=False)
        return self.__handlemsg(up.unquote(res.headers['Location']))

    def __handlemsg(self, url: str):
        param = up.parse_qs(up.urlparse(url).query)
        res = {
            'status': SCAN_FAIL,
            'msg': param.get('msg', [''])[0],
            'resvmsg': '',
            'title': param.get('title', [''])[0]
        }
        # 拥有座位使用权
        if param['type'][0] == '4':
            # 正常使用
            if param['status'][0] == '0':
                res['status'] = SCAN_INUSE
            # 等待签到
            elif param['status'][0] == '5':
                res['status'] = SCAN_RESERVED
        # 座位可用
        elif param['type'][0] == '3':
            res['status'] = SCAN_FREE
            res['msg'] = int(param['dwMaxUseMin'][0])
        # 未绑定微信
        elif param['type'][0] == '2':
            res['status'] = SCAN_NO_MSN
        # 操作成功
        elif param['type'][0] == '1':
            res['status'] = SCAN_SUCCESS
        # 错误
        elif param['type'][0] == '0':
            if 'ResvMsg' in param:
                res['status'] = SCAN_OCCUPIED
                res['resvmsg'] = param['ResvMsg'][0]
            elif param['msg'][0] == '设备不可用':
                res['status'] = SCAN_BANDED
            else:
                res['status'] = SCAN_FAIL
        else:
            res['status'] = SCAN_UNKNOWN
        return res

    def doScan(self, seatname: str):
        seat = SeatId[seatname]
        return self._baseScanget(f'http://{getHost()}/Pages/WxSeatSign.aspx?sta=1&lab={seat["labId"]}&dev={seat["devId"]}&msn={self.mMsn}')

    def doSign(self):
        return self._baseScanget(f'http://{getHost()}/Pages/WxSeatSign.aspx?Userin=true')

    def doScanover(self):
        return self._baseScanget(f'http://{getHost()}/Pages/WxSeatSign.aspx?DoUserOut=2')

    def doUse(self, time):
        return self._baseScanget(f'http://{getHost()}/Pages/WxSeatSign.aspx?DoUserIn=true&dwUseMin={time}')
