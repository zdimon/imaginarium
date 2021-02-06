from datetime import datetime
from celery import shared_task
import socketio
import time
from datetime import datetime
from imagin.settings import BASE_DIR
import json
json_path = f'{BASE_DIR}/static/data.json'      
mgr = socketio.RedisManager('redis://localhost:6379/0', write_only=True)

@shared_task
def send_data_task(delay=0):
    if delay>0:
        time.sleep(delay)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    with open(json_path,'r') as file:
        json_data = json.loads(file.read())
    mgr.emit('ping', data={'time': current_time,'state': json_data})
    print(current_time,'sending')