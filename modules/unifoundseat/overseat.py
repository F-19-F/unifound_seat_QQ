from .utils import *
from .api import *
from .robot import getSessionbyid,robotUser
import asyncio
from datetime import datetime
channel = Channel.current()
# 取消OK
@channel.use(ListenerSchema(
    listening_events=[FriendMessage, StrangerMessage],
    inline_dispatchers=[Twilight([
        FullMatch('取消'),
        RegexMatch(".*?") @ "cmd"
    ])]))
async def scanseat(app: Ariadne, friend: Union[Friend,Stranger],cmd:RegexResult):
    loop = asyncio.get_running_loop()
    cmd = cmd.result.asDisplay()
    db_user = await loop.run_in_executor(None, database.GetUserByID, friend.id)
    if not db_user:
        await sendMessage(app,friend,'没有绑定!')
        return
    user = getSessionbyid(friend.id, db_user['num'], db_user['msn'])
    result = await user.getActivereservelist()
    if cmd == "所有预约":
        if result['status'] == WEB_SUCCESS:
            text='取消所有预约:'
            for i in result['msg']:
                if not i['id']:
                    text+=f"\n座位:{i['seatname']}\n时间:{i['start']}\n状态:不可操作"
                    continue
                if not i['started']:
                    r = await user.dowebReserveover(i)
                    if r['status'] == WEB_SUCCESS:
                        app.taskManager.delTask(f"{friend.id}-autosign-{i['start']}")
                        text+=f"\n座位:{i['seatname']}\n时间:{i['start']}\n状态:已取消预约和自动签到"
                    else:
                        text+=f"\n座位:{i['seatname']}\n时间:{i['start']}\n状态:取消失败:{r['msg']}"
                elif not i['signed']:
                    text+=f"\n座位:{i['seatname']}\n时间:{i['start']}\n状态:未签到,你可发送\"签到\"签到,或者在签到后发送\"取消当前座位\""
                else:
                    text+=f"\n座位:{i['seatname']}\n时间:{i['start']}\n状态:使用中未取消"
            await sendMessage(app,friend,text)
        else:
            await sendMessage(app,friend,"你没有任何预约")
    elif cmd == "当前座位":
        if result['status'] == WEB_SUCCESS:
            text='取消当前座位:'
            for i in result['msg']:
                if i['started'] and i['signed']:
                    r = await user.dowebReserveover(i)
                    if r['status'] == WEB_SUCCESS:
                        app.taskManager.delTask(f"{friend.id}-autorenew-{i['seatname']}")
                        text+=f"\n座位:{i['seatname']}\n时间:{i['start']}\n状态:已取消,自动续约已停止"
                    else:
                        text+=f"\n座位:{i['seatname']}\n时间:{i['start']}\n状态:取消失败:{r['msg']}"
            if text=='取消当前座位:':
                text+="没有正在使用的座位"
            await sendMessage(app,friend,text)
        else:
            await sendMessage(app,friend,"你没有任何预约")
    else:
        await sendMessage(app,friend,'请输入 "取消当前座位"或 "取消所有预约"')
        
        
    
    