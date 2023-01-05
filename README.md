## UniSeat
联创图书馆座位自动预约的saya模块,
包括一键自动预约，到点自动签到等。

QQ机器人专业团队源码

### 1.如何使用
* 1.安装pdm
```shell
# 安装pdm
curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python3 -
# 安装依赖
pdm install
```
* 2.配置index_qq.py

项目使用 mirai-api-http，请按照[mirai-api-http](https://github.com/project-mirai/mirai-api-http)的文档配置好后修改index_qq.py里的 host,verify_key,account

* 3.配置代理服务器(服务器在校园网内网可以不配置)

修改modules/unifoundseat/api/config.py里的ProxyHost(ip:端口)
服务器跑在内网可以留空,外网需要你弄一个内网穿透，建议使用nps

* 4.配置数据库

项目使用MongoDB作为后端数据库，你需要在服务器上安装一个MongoDB
```shell
# debian系
sudo apt-get update && sudo apt-get install mongodb
sudo systemctl start mongodb 
```
* 5.修改能发送公告的QQ号，可选

在modules/unifoundseat/public.py,修改我注释的QQ号为你的，你QQ给机器人发送
```shell
公告
公告的内容
```
即可给每个绑定了的人发送公告内容，慎用，容易封机器人的号

* 6. 运行

```shell
# 需要python3.9
eval "$(pdm --pep582)"
python3.9 index_qq.py
```

### 2.关于其他学校
请自行修改modules/unifoundseat/api/Seats.json和匹配座位号规则。

陌生人回复消息奔溃的问题，改这行
__pypackages__/3.9/lib/graia/ariadne/app.py 421 return Friend(id=friend_id,nickname="陌生人",remark='陌生人')