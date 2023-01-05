from .utils import *
from .api import *
from .robot import getSessionbyid
import asyncio
channel = Channel.current()
# OK
@channel.use(ListenerSchema(
    listening_events=[FriendMessage, StrangerMessage],
    inline_dispatchers=[Twilight([
        FullMatch('签到'),
    ])]))
async def sign(app: Ariadne,friend:Union[Friend,Stranger]):
    loop = asyncio.get_running_loop()
    db_user = await loop.run_in_executor(None, database.GetUserByID, friend.id)
    if not db_user:
        await sendMessage(app,friend, "没绑定")
        return
    user= getSessionbyid(friend.id, db_user['num'], db_user['msn'])
    rsvs = await user.getActivereservelist()
    if rsvs['status'] == WEB_SUCCESS:
        text = "预约如下:"
        for i in rsvs['msg']:
            if i['signed']:
                sta="已签到"
            elif i['started']:
                sta="未签到"
            else:
                sta="未开始"
            text+=f"\n{i['seatname']}:\n开始:{i['start']}\n结束:{i['end']}\n状态:{sta}"
            if i['started'] and not i['signed']:
                await user.doScan(i['seatname'])
                res = await user.doSign()
                if res['status'] == SCAN_SUCCESS:
                    await sendMessage(app,friend,f"座位{i['seatname']}:签到成功!")
                    return
                else:
                    await sendMessage(app,friend,f'签到失败:{res["msg"]}')
        await sendMessage(app,friend,text)
    else:
        await sendMessage(app,friend,"你还没有预约任何座位")