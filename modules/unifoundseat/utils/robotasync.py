from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Friend,Stranger
from graia.saya import Channel
from graia.ariadne.event.message import FriendMessage, StrangerMessage
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import Twilight
from graia.ariadne.message.parser.twilight import FullMatch, ArgumentMatch, RegexResult, RegexMatch, ArgResult
from typing import Union
async def sendMessage(app:Ariadne,friend:Union[Friend,Stranger],message:str):
    return await app.sendFriendMessage(friend,MessageChain.create(message))