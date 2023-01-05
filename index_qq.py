from graia.ariadne.app import Ariadne
from graia.ariadne.model import MiraiSession
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour

from modules.unifoundseat.taskmgr import asyncTaskManager


app = Ariadne(MiraiSession(
    host="http://localhost:9980",
    verify_key="f19isyourfather",
    account=2918732501
))
saya = app.create(Saya)
saya.install_behaviours(
    app.create(BroadcastBehaviour),
)
app.taskManager = asyncTaskManager(app.loop,app)
app.taskManager.loadTasks()
app.taskManager.run()

with saya.module_context():
    saya.require("modules.unifoundseat.bind")
    saya.require("modules.unifoundseat.scanseat")
    saya.require("modules.unifoundseat.sign")
    saya.require("modules.unifoundseat.autosign")
    saya.require("modules.unifoundseat.overseat")
    saya.require("modules.unifoundseat.reserve")
    saya.require("modules.unifoundseat.onekey")
    saya.require("modules.unifoundseat.autorenew")
    saya.require("modules.unifoundseat.public")

app.launch_blocking()
