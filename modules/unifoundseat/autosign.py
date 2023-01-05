from datetime import datetime, timedelta
from .robot import  getSessionbyid
from .utils import *
from .api import *
from .taskmgr.baseTask import autoSigntask
import asyncio
channel = Channel.current()
# OK


@channel.use(ListenerSchema(
    listening_events=[FriendMessage, StrangerMessage],
    inline_dispatchers=[Twilight([
        FullMatch('自动签到'),
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
        await sendMessage(app, friend, "你还没有任何预约!")
        return
    else:
        tosend = '自动签到:'
        for i in result['msg']:
            if not i['signed']:
                date = datetime.strptime(f"{datetime.now().year}-{i['start']}", "%Y-%m-%d %H:%M")
                if app.taskManager.hasTask(f"{friend.id}-autosign-{i['start']}"):
                    tosend += f"\n预约:\n座位:{i['seatname']}\n开始时间:{i['start']}\n状态:已经设置过了"
                    continue
                app.taskManager.addTask(autoSigntask(
                    f"{friend.id}-autosign-{i['start']}", i['seatname'], friend.id, db_user['num'], db_user['msn'],date=date+timedelta(minutes=1), app=app))
                tosend += f"\n预约:\n座位:{i['seatname']}\n开始时间:{i['start']}\n状态:设置签到成功"
            else:
                tosend += f"\n预约:\n座位:{i['seatname']}\n开始时间:{i['start']}\n状态:已经生效了"
    await sendMessage(app, friend, tosend)
