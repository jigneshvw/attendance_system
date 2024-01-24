from iron_mq import *
import socket

import cv2
import copy
import numpy as np
import json

import imutils.video
import time



# ironmq = IronMQ(host='mq-aws-us-east-1-1.iron.io',
#                 project_id='500f7b....b0f302e9',
#                 token='Et1En7.....0LuW39Q',
#                 protocol='https', port=443,
#                 api_version=3,
#                 config_file=None)

class NumpyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.ndarray):
			return obj.tolist()
		return json.JSONEncoder.default(self, obj)



rpiName = socket.gethostname()


mq = IronMQ(host='0.0.0.0', port='enter port', project_id='enter proj id', token='enter token')

# Get a queue (if it doesn't exist, it will be created when you first post a message)
queue = mq.queue("my_queue")

video = imutils.video.VideoStream(src=0 , resolution=(320, 240)).start()
time.sleep(2.0)


while True:
	image = video.read()
	print('hostname: ', rpiName)
# Post a message
	data = json.dumps(image, cls=NumpyEncoder)
	print(type(data))
	queue.post(data)
	print('frame sent to server... \n')


# Delete a message (you must delete a message when you're done with it or it will go back on the queue after a timeout)
	# queue.delete(msg["messages"][0]["id"])