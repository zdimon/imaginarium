import socketio
import time
from datetime import datetime
from imagin.imagin.settings import BASE_DIR
import json
json_path = f'{BASE_DIR}/static/data.json'      
mgr = socketio.RedisManager('redis://localhost:6379/0', write_only=True)
from imagin.game.tasks import timer_task

while True: 
    time.sleep(2)  
    #timer_task.delay()  
    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # with open(json_path,'r') as file:
    #     json_data = json.loads(file.read())
    # mgr.emit('ping', data={'time': current_time,'state': json_data})
    # print(current_time,'sending')
