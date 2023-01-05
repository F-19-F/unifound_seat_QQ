from operator import ne
from unittest import result
from .utils import *
from .api import *
from .robot import getSessionbyid, robotUser
import asyncio
from datetime import datetime, timedelta
channel = Channel.current()
#OK


@channel.use(ListenerSchema(
    listening_events=[FriendMessage, StrangerMessage],
    inline_dispatchers=[Twilight([
        FullMatch("预约 "),
        RegexMatch(".*? ") @ "cmd",
        RegexMatch(".*?") @ "seatname",
    ])]))
async def scanseat(app: Ariadne, friend: Union[Friend,Stranger], cmd: RegexResult, seatname: RegexResult):
    loop = asyncio.get_running_loop()
    seatname = seatname.result.asDisplay()
    cmd = cmd.result.asDisplay().replace(" ","")
    if cmd not in ['今天','明天']:
        await sendMessage(app, friend, '"预约 今天 座位号"或"预约 明天 座位号"')
        return
    seatname = judgeSeat(seatname)
    if not seatname:
        await sendMessage(app, friend, '座位格式输错啦!')
        return
    if seatname not in SeatId:
        await sendMessage(app, friend, '没有这个座位呀!')
        return
    db_user = await loop.run_in_executor(None, database.GetUserByID, friend.id)
    if not db_user:
        await sendMessage(app, friend, '没有绑定!')
        return
    user = getSessionbyid(friend.id, db_user['num'], db_user['msn'])
    if cmd == "明天":
        tomorrow = datetime.now()+timedelta(days=1)
        datefrom = datetime(year=tomorrow.year,
                            month=tomorrow.month, day=tomorrow.day, hour=8)
    elif cmd == "今天":
        datefrom = datetime.now()
        if datefrom.hour < 8:
            datefrom = datetime(year=datefrom.year,
                            month=datefrom.month, day=datefrom.day, hour=8)
    hours = 5
    nextdate = datefrom
    looptime = 0
    while hours == 5:
        nextdate = datefrom+timedelta(hours=5*looptime)
        hours, res = await afterwardRsv(user, seatname, nextdate)
        looptime += 1
    # 第一次就不成功
    nextdate=datefrom+timedelta(hours=5*(looptime-1)+hours)
    if nextdate.hour > 22 or nextdate.day > datefrom.day:
        nextdate = datetime(year=nextdate.year,month=nextdate.month, day=nextdate.day, hour=22)
    if nextdate == datefrom and hours == 0:
        await sendMessage(app, friend, f"预约失败:{res['msg']}")
    # 选了至少1个小时
    else:
        await sendMessage(
            app, friend, f"预约成功:\n开始{datefrom.strftime('%Y-%m-%d %H:%M')}\n结束:{nextdate.strftime('%Y-%m-%d %H:%M')}")


async def afterwardRsv(user: robotUser, seatname: str, begin: datetime):
    hours = 5
    while hours>0:
        nextdate = begin+timedelta(hours=hours)
        # 超过晚上10点
        if nextdate.hour > 22 or nextdate.day>begin.day:
            nextdate = datetime(year=nextdate.year,month=nextdate.month, day=begin.day, hour=22,minute=0)
        res = await user.dowebReseve(seatname, begin, nextdate)
        if res['status'] == WEB_SUCCESS:
            return hours,res
        hours -= 1
    return hours, res
