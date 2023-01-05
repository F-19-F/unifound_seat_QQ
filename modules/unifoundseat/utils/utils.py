import re

def judgeSeat(SeatName):
    result = ''
    res = re.findall("(.*?) ([\d]+)", SeatName)
    if len(res) != 0:
        #print(res)
        res = res[0]
        try:
            #自动添加楼层
            f = res[0][0]+"F"
            result = "7A{}-{}-{}".format(res[0], f, res[1].zfill(3))
            return result
        except:
            # print("座位格式错误！")
            return False
    #格式2
    res = re.findall("(.*?)-(.*?)-([\d]+)", SeatName)
    if len(res) != 0:
        res = res[0]
        try:
            result = "{}-{}-{}".format(res[0], res[1], res[2].zfill(3))
            return result
        except:
            # print("座位格式错误！")
            return False