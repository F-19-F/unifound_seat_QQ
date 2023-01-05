from .utils import *
from .api import *
import asyncio
channel = Channel.current()
# OK
@channel.use(ListenerSchema(
    listening_events=[FriendMessage, StrangerMessage],
    inline_dispatchers=[Twilight([
        FullMatch('公告\n'),
        RegexMatch("[\s\S]*") @ "content"
    ])]))
async def public(app: Ariadne,friend:Union[Friend,Stranger],content:RegexResult):
    if friend.id == 111:#能发送公告的QQ号
        susscesc = 0
        errorc = 0
        content = content.result.asDisplay()
        loop = asyncio.get_running_loop()
        users = await loop.run_in_executor(None, database.GetAllUser)
        for u in users:
            f = Friend(id=u['_id'],nickname="",remark="")
            try:
                await sendMessage(app,f,content)
                await asyncio.sleep(1)
                susscesc+=1
            except:
                errorc+=1
                continue
        res = "公告成功 成功:{},失败:{}".format(susscesc,errorc)
        await sendMessage(app,friend,res)