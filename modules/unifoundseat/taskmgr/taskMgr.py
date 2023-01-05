from shutil import which
from .baseTask import asyncBasetask
import json
import asyncio
import importlib
class asyncTaskManager:
    def __init__(self, loop,app=None) -> None:
        self.loop = loop
        self.tasks = {}
        self.torun = True
        self.load_data:dict =None
        self.app = app

    def addTask(self, task: asyncBasetask):
        self.tasks[task.key] = task
        return task.key

    def delTask(self, key: str):
        self.tasks.pop(key, None)

    def hasTask(self,key:str):
        return key in self.tasks

    def loadTasks(self,):
        try:
            with open("task.json",'r',encoding='utf-8') as f:
                self.load_data = json.loads(f.read())
        except:
            self.load_data = None
            
     

    def __saveTasks(self,):
        with open("task.json",'w+',encoding='utf-8') as f:
            task_keys = list(self.tasks.keys())
            tosave = {}
            for k in task_keys:
                tosave[k]={
                    "type":self.tasks[k].clsname,
                    "datas":self.tasks[k].datas
                }
            f.write(json.dumps(tosave,indent=4,ensure_ascii=False))

    async def mainloop(self,):
        looadedcls={}
        if self.load_data:
            keys = list(self.load_data.keys())
            for key in keys:
                if self.load_data[key]["type"] in looadedcls:
                    self.load_data[key]['datas']['app']=self.app
                    self.tasks[key]=looadedcls[self.load_data[key]["type"]](key,**self.load_data[key]['datas'])
                else:
                    for cls in asyncBasetask.__subclasses__():
                        if str(cls) == self.load_data[key]["type"]:
                            looadedcls[self.load_data[key]["type"]]=cls
                            self.load_data[key]['datas']['app']=self.app
                            self.tasks[key]=cls(key,**self.load_data[key]['datas'])
                    
        while self.torun:
            task_keys = list(self.tasks.keys())
            for key in task_keys:
                task = self.tasks[key]
                if not task.tostop and task.needrun():
                    asyncio.run_coroutine_threadsafe(
                        task.run(), asyncio.get_running_loop())
                # 回收内存
                if task.tostop:
                    self.delTask(task.key)
                    del task
            await asyncio.get_running_loop().run_in_executor(None,self.__saveTasks)
            await asyncio.sleep(1)

    def run(self):
        asyncio.run_coroutine_threadsafe(self.mainloop(), self.loop)

    def __del__(self):
        self.stop()

    def stop(self):
        self.torun = False
        