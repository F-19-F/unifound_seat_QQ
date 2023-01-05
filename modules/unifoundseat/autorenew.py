from datetime import datetime, timedelta
import time
from .robot import  getSessionbyid
from .utils import *
from .api import *
from .taskmgr.baseTask import autoSigntask,autoRenewtask
import asyncio
channel = Channel.current()
# OK


@channel.use(ListenerSchema(
    listening_events=[FriendMessage, StrangerMessage],
    inline_dispatchers=[Twilight([
        FullMatch('自动续约'),
    ])]))
async def scanseat(app: Ariadne, friend: Union[Friend,Stranger]):
    loop = asyncio.get_running_loop()
    db_user = await loop.run_in_executor(None, database.GetUserByID, friend.id)
    if not db_user:
        await sendMessage(app, friend, '没有绑定!')
        return
    user = getSessionbyid(friend.id, db_user['num'], db_user['msn'])
    result = await user.getActivereservelist()
    if result['status'] == WEB_FAIL:
        await sendMessage(app, friend, "你还没有任何预约！")
        return
    else:
        tosend = '自动续约:'
        for i in result['msg']:
            if i['signed']:
                if app.taskManager.hasTask(f"{friend.id}-autorenew-{i['seatname']}"):
                    tosend += f"座位:{i['seatname']},已经在续约列表中了"
                    continue
                app.taskManager.addTask(autoRenewtask(
                    f"{friend.id}-autorenew-{i['seatname']}", i['seatname'], friend.id, db_user['num'], db_user['msn'],nextruntime=time.time()+3600, app=app))
                tosend += f"座位:{i['seatname']},开启自动续约成功"
        if tosend == '自动续约:':
            tosend+="你还没有任何正在在使用中的座位!"
    await sendMessage(app, friend, tosend)
