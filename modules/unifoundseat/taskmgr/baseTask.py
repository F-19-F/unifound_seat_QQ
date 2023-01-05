from ..robot.unifound import *
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from datetime import datetime
import time


class asyncBasetask:
    def __init__(self, key, datas) -> None:
        self.key: str = key
        self.datas: dict = datas
        self.clsname: str = str(type(self))
        self.tostop: bool = False

    def needrun(self,) -> bool:
        return False

    async def run(self,):
        pass

    def stop(self,):
        self.tostop = True


class autoSigntask(asyncBasetask):
    def __init__(self, key, seatname, id, username, msn, nextruntime=None, date: datetime = None, app: Ariadne = None) -> None:
        super().__init__(key, {})
        self.datas['id'] = id
        self.datas['seatname'] = seatname
        self.datas['username'] = username
        self.datas['msn'] = msn
        if nextruntime:
            self.datas['nextruntime'] = nextruntime
        elif date:
            self.datas['nextruntime'] = date.timestamp()
        else:
            self.datas['nextruntime'] = 0
        self.app = app
        self.runlock = False

    def needrun(self) -> bool:
        return time.time() > self.datas['nextruntime'] and not self.runlock

    async def run(self):
        if self.runlock:
            return
        self.runlock=True
        user = getSessionbyid(
            self.datas['id'], self.datas['username'], self.datas['msn'])
        result = await user.doScan(self.datas['seatname'])
        if result['status'] == SCAN_RESERVED:
            result = await user.doSign()
            if result['status'] == SCAN_SUCCESS:
                pass
                # await self.app.sendFriendMessage(self.datas['id'], MessageChain.create(f"{self.datas['seatname']}已经签到好了哦"))
            else:
                await self.app.sendFriendMessage(self.datas['id'], MessageChain.create(f"{self.datas['seatname']}签到失败:{result['msg']}"))
            self.stop()
        elif result['status'] == SCAN_BANDED:
            self.datas['nextruntime'] += 60
        else:
            await self.app.sendFriendMessage(self.datas['id'], MessageChain.create(f"签到失败{result['msg']}"))
            self.stop()
        self.runlock=False


class autoRenewtask(asyncBasetask):
    def __init__(self, key, seatname, id, username, msn, nextruntime=None, app: Ariadne = None) -> None:
        super().__init__(key, {})
        self.datas['id'] = id
        self.datas['seatname'] = seatname
        self.datas['username'] = username
        self.datas['msn'] = msn
        if nextruntime:
            self.datas['nextruntime'] = nextruntime
        else:
            self.datas['nextruntime'] = 0
        self.app = app
        self.runlock = False

    def needrun(self) -> bool:
        return time.time() > self.datas['nextruntime'] and not  self.runlock

    async def run(self):
        if self.runlock:
            return
        self.runlock=True
        user = getSessionbyid(
            self.datas['id'], self.datas['username'], self.datas['msn'])
        # 判断状态
        result = await user.doScan(self.datas['seatname'])
        # 在用了
        if result['status'] == SCAN_INUSE:
            # 先取消
            result = await user.doScanover()
            # 取消成功
            if result['status'] == SCAN_SUCCESS:
                result = await user.doScan(self.datas['seatname'])
                # 判断状态
                if result['status'] == SCAN_FREE:
                    rsvmin = result['msg']
                    result = await user.doUse(rsvmin)
                    # 使用是否成功
                    if result['status'] == SCAN_SUCCESS:
                        await self.app.sendFriendMessage(self.datas['id'], MessageChain.create(f"{self.datas['seatname']},已经续约了一次"))
                        self.datas['nextruntime'] += 3600
                    else:
                        await self.app.sendFriendMessage(self.datas['id'], MessageChain.create(f"{self.datas['seatname']},自动续约失败:{result['msg']}"))
                        self.stop()
                # 被占用或其他
                else:
                    await self.app.sendFriendMessage(self.datas['id'], MessageChain.create(f"{self.datas['seatname']},自动续约失败:{result['msg']}"))
                    self.stop()
            # 取消失败
            else:
                await self.app.sendFriendMessage(self.datas['id'], MessageChain.create(f"{self.datas['seatname']},自动续约失败:{result['msg']}"))
                self.stop()
        # 根本就没在用
        else:
            await self.app.sendFriendMessage(self.datas['id'], MessageChain.create(f"{self.datas['seatname']},自动续约失败:{result['msg']}"))
            self.stop()
        self.runlock = False
