from requests import Response
from .wxSeat import wxUser
from .const import *
from .config import getHost, SeatId
from datetime import datetime, timedelta
from .parser import parserRsv
import json
import re


class unifoundUser(wxUser):
    mUsername: str
    mPassword: str
    mHacklogin: bool

    def __init__(self, username, msn='', hacklogin=True, passwd='') -> None:
        super().__init__(msn)
        self.mUsername = username
        self.mHacklogin = hacklogin
        self.mPassword = passwd

    def dowebLogin(self):
        if self.mHacklogin:
            res = self.get(
                f'http://{getHost()}/ClientWeb/pro/ajax/login.aspx?act=login&id={self.mUsername}&pwd=uniFound808')
        else:
            res = self.get(
                f'http://{getHost()}/ClientWeb/pro/ajax/login.aspx?act=login&id={self.mUsername}&pwd={self.mPassword}')
        result = res.text
        result = re.sub("{.*?密码不可用.*?}", '', result)
        result = json.loads(result)
        # 更新msn
        if 'data' in result and result['data'] and 'msn' in result['data'] and result['data']['msn'] and result['data']['msn'] != self.mMsn:
            self.mMsn = result['data']['msn']
        if result['ret'] == 1:
            result['status']=WEB_SUCCESS
        else:
            result['status']=WEB_FAIL
        return result

    def dowebReseve(self, seatname: str, starttime: datetime, endtime: datetime):
        dev_id = SeatId[seatname]['devId']
        start = starttime.strftime("%Y-%m-%d+%H%%3A%M")
        end = endtime.strftime("%Y-%m-%d+%H%%3A%M")
        return self._baseWebget(f"http://{getHost()}/ClientWeb/pro/ajax/reserve.aspx??dialogid=&dev_id={dev_id}&lab_id=&kind_id=&room_id=&type=dev&prop=&test_id=&term=&number=&classkind=&test_name=&start={start}&end={end}&up_file=&memo=&act=set_resv")

    def getActivereservelist(self):
        res = self._baseWebget(
            f"http://{getHost()}/ClientWeb/pro/ajax/center.aspx?act=get_History_resv&strat=90&StatFlag=New")
        if res['status'] == WEB_FAIL:
            return {
                'status': WEB_FAIL,
                'msg': []
            }
        if "没有数据" not in res['msg']:
            return {
                'status': WEB_SUCCESS,
                'msg': parserRsv(res['msg'])
            }
        else:
            return {
                'status': WEB_FAIL,
                'msg': []
            }

    def dowebReserveover(self, rsv: dict):
        if not rsv['started']:
            url = f'http://{getHost()}/ClientWeb/pro/ajax/reserve.aspx?act=del_resv&id={rsv["id"]}'
        else:
            url = f'http://{getHost()}/ClientWeb/pro/ajax/reserve.aspx?act=resv_leave&type=2&resv_id={rsv["id"]}'
        res = self.get(url)
        return self._handlejsonmsg(res)

    def _baseWebget(self, url):
        res = self.get(url)
        return self._handlejsonmsg(res)

    def _handlejsonmsg(self, res: Response):
        rt = {
            'status': WEB_FAIL,
            'msg': ''
        }
        try:
            r = res.json()
            rt['msg'] = r['msg']
            if res.json()['ret'] == 1:
                rt['status'] = WEB_SUCCESS
            else:
                rt['status'] = WEB_FAIL
        except:
            rt['msg'] = "未知异常"
        return rt


if __name__ == '__main__':
    pass
    # rsvs = client.getActivereservelist()['msg']
    # for i in rsvs:
    #     print(client.dowebReserveover(i))
    # asyncio.run(main())
