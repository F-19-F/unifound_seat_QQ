from .utils import *
from .api import *
from .robot import robotUser
import asyncio
from datetime import datetime
channel = Channel.current()


# OK
@channel.use(ListenerSchema(
    listening_events=[FriendMessage, StrangerMessage],
    inline_dispatchers=[Twilight([
        FullMatch('绑定 '),
        RegexMatch(".*?") @ "num"
    ])]))
async def bind(app: Ariadne, friend: Union[Friend,Stranger], num: RegexResult):
    loop = asyncio.get_running_loop()
    num = num.result.asDisplay()
    user = robotUser(num, friend.id)
    msn = await user.getMsn()
    if(not msn):
        await sendMessage(app,friend, "学号输入有误或者你未绑定微信(绑定微信需用微信扫座位二维码并在登录时选择绑定此账号)")
        return
    now = datetime.now()
    User = await loop.run_in_executor(None, database.GetUserByID, friend.id)
    t = None
    if User and 'binddate' in User:
        t = datetime.strptime(User['binddate'], "%Y-%m-%d %H:%M:%S")
    if t and (now - t).days < 1:
        await sendMessage(app,friend,"为了防止滥用，一天只能绑定一次哦")
        return
    await loop.run_in_executor(None, database.UpdateUser, friend.id, {'msn': msn, 'binddate': now.strftime("%Y-%m-%d %H:%M:%S"), 'num': num})
    await sendMessage(app,friend,"绑定好了哦")