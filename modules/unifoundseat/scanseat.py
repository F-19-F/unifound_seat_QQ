from .utils import *
from .api import *
from .robot import getSessionbyid,robotUser
import asyncio
from datetime import datetime
channel = Channel.current()

# OK
@channel.use(ListenerSchema(
    listening_events=[FriendMessage, StrangerMessage],
    inline_dispatchers=[Twilight([
        FullMatch('选座 '),
        RegexMatch(".*?") @ "seatname"
    ])]))
async def scanseat(app: Ariadne, friend: Union[Friend,Stranger], seatname: RegexResult):
    loop = asyncio.get_running_loop()
    seatname = seatname.result.asDisplay()
    seatname = judgeSeat(seatname)
    if not seatname:
        await sendMessage(app,friend,'座位格式输错啦!')
        return
    if seatname not in SeatId:
        await sendMessage(app,friend,'没有这个座位呀!')
        return
    db_user = await loop.run_in_executor(None, database.GetUserByID, friend.id)
    if not db_user:
        await sendMessage(app,friend,'没有绑定!')
        return
    user = getSessionbyid(friend.id, db_user['num'], db_user['msn'])
    result = await user.doScan(seatname)
    if result['status'] == SCAN_FREE:
        res = await user.doUse(result['msg'])
        if res['status'] == SCAN_SUCCESS:
            await sendMessage(app,friend,f"选座成功:我们已经帮你选了{result['msg']}分钟")
    elif result['status'] == SCAN_INUSE:
        await sendMessage(app,friend,f"{result['msg']}")
    elif result['status'] == SCAN_BANDED:
        await sendMessage(app,friend,"座位处于预约开始前夕,已被禁止操作")
    elif result['status'] == SCAN_OCCUPIED:
        await sendMessage(app, friend,f"选座失败:{result['msg']}\n{result['resvmsg']}")
    else:
        await sendMessage(app, friend,f"选座失败:{result['msg']}")