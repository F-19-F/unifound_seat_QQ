from requests import Response
from api import *
from datetime import datetime
import asyncio
cache_users = {}


class robotUser(unifoundUser):
    def __init__(self, username, id: int, msn='', hacklogin=True, passwd='') -> None:
        super().__init__(username, msn, hacklogin, passwd)
        cache_users[id] = self

    async def getActivereservelist(self):
        return await asyncio.get_running_loop().run_in_executor(None,super().getActivereservelist)

    async def doScan(self, seatname: str):
        return await asyncio.get_running_loop().run_in_executor(None,super().doScan,seatname)

    async def doUse(self, time):
        return await asyncio.get_running_loop().run_in_executor(None,super().doUse,time)

    async def doSign(self):
        return await asyncio.get_running_loop().run_in_executor(None,super().doSign)

    async def doScanover(self):
        return await asyncio.get_running_loop().run_in_executor(None,super().doScanover)

    async def dowebLogin(self):
        return await asyncio.get_running_loop().run_in_executor(None,super().dowebLogin)

    async def dowebReseve(self, seatname: str, starttime: datetime, endtime: datetime):
        return await asyncio.get_running_loop().run_in_executor(None,super().dowebReseve,seatname, starttime, endtime)

    async def dowebReserveover(self, rsv: dict):
        return await asyncio.get_running_loop().run_in_executor(None,super().dowebReserveover,rsv)

    async def getMsn(self):
        if not self.mMsn:
            await self.dowebLogin()
        return self.mMsn
    # 过期自动登录
    def _baseWebget(self, url):
        try:
            res = super()._baseWebget(url)
            if "ERRMSG_RESV_CONFLICT" in res['msg']:
                res['msg'] = "预约时间冲突"
            if "session =null" in res['msg']:
                super().dowebLogin()
                return super()._baseWebget(url)
            else:
                return res
        except:
            return {
                'status': WEB_FAIL,
                'msg': '出现异常'
            }
    
    def _baseScanget(self, url):
        try:
            return super()._baseScanget(url)
        except:
            return {
            'status': SCAN_FAIL,
            'msg': "出现异常",
            'resvmsg': '',
            'title': ''
        }
        


def getSessionbyid(id: int, username='', msn=''):
    if id in cache_users:
        return cache_users[id]
    elif username:
        user = robotUser(username, id, msn)
        return user
    else:
        return None


def delCache(id: int):
    cache_users.pop(id, None)


if __name__ == '__main__':
    # print(Info)
    print(u.mMsn)
    # print(GetDirectUrl("7A402-4F-015"))
