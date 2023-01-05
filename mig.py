import pymongo

class db():
    def __init__(self) -> None:
        self.myclient = pymongo.MongoClient()
        self.xrlib = self.myclient["XRLIB"]
        self.collcet = self.xrlib['users']
    
    def GetUserByID(self,id):
        res = self.collcet.find_one({'_id': id})
        if not res:
            return None
        return res

    def GetAllUser(self):
        res = self.collcet.find()
        if not res:
            return []
        return res
        
    def UpdateUser(self,id: int, data):
        # 有就更新
        if not self.collcet.find_one_and_update({'_id': id}, {'$set': data}):
            # 没有就插入
            t = {'_id': id}
            t.update(data)
            self.collcet.insert_one(t)
        return True

database = db()
users = database.GetAllUser()
import json
data = json.load(open("data.json",'r'))
print(data)
for u in users:
    print(u['num'])
    # for i in data:
    #     if i['msn'] == u['msn']:
    #         u['num'] = i['num']
    # database.UpdateUser(u['_id'], u)
# sys.modules[__name__] = db()
