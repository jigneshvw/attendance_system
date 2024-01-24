# * ---------- IMPORTS --------- *
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, Response
# from flask import redirect, url_for
import os
import psycopg2
import cv2
import numpy as np
import re
import imutils
import pandas as pd
import copy

import time
import queue, threading
import requests

# from imutils.video import VideoStream
# from videocamera_class import VideoCamera
import face_recognition

# import imagezmq
from iron_mq import *



# from imutils.video import FPS




# Get the relative path to this file (we will use it later). 
# The location/path of the images saved or generated (eg: assets/img/) should be in the same folder as that of current python (.py) file stored.
FILE_PATH = os.path.dirname(os.path.realpath(__file__))

# * ---------- Create App --------- *
app = Flask(__name__)
# CORS(app, support_credentials=True)



# * ---------- DATABASE CONFIG --------- *

# DATABASE_USER = os.environ['DATABASE_USER']
# DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
# DATABASE_HOST = os.environ['DATABASE_HOST']
# DATABASE_PORT = os.environ['DATABASE_PORT']
# DATABASE_NAME = os.environ['DATABASE_NAME']



@app.route('/')
def index():
	return render_template('index.html')



global image_copy, image_file, connection, cursor
global face_locations, face_encodings, face_names, process_this_frame 

def gen():
	known_face_encodings = []
	known_face_names = []
	known_faces_filenames = []

	for (dirpath, dirnames, filenames) in os.walk('/static/assets/img/users/'):
		known_faces_filenames.extend(filenames)
		break

	for filename in known_faces_filenames:
		face = face_recognition.load_image_file('/static/assets/img/users/{filename}'.format(filename=filename))
		known_face_names.append(re.sub("[0-9]",'', filename[:-4]))
		known_face_encodings.append(face_recognition.face_encodings(face)[0])

	print(known_face_names)


	# fps = FPS().start()

	def process_frame(image):

		face_locations = []
		face_encodings = []
		face_names = []
		process_this_frame = True

		if process_this_frame:
			# Find all the faces and face encodings in the current frame of video
			face_locations = face_recognition.face_locations(image)
			face_encodings = face_recognition.face_encodings(image, face_locations)

			print(face_locations)
			
			# Initialize an array for the name of the detected users
			face_names = []

			# * ---------- Initialyse JSON to EXPORT --------- *
			json_to_export = {}
			
			for face_encoding in face_encodings:
				# See if the face is a match for the known face(s)
				matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
				name = "Unknown"

				# # If a match was found in known_face_encodings, just use the first one.
				# if True in matches:
				#     first_match_index = matches.index(True)
				#     name = known_face_names[first_match_index]

				# Or instead, use the known face with the smallest distance to the new face
				face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
				best_match_index = np.argmin(face_distances)
				if matches[best_match_index]:
					name = known_face_names[best_match_index]

					# * ---------- SAVE data to be send to the API -------- *
					json_to_export['name'] = str(name).lower()
					json_to_export['hour'] = f'{time.localtime().tm_hour}:{time.localtime().tm_min}'
					json_to_export['date'] = f'{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}'
					json_to_export['picture_array'] = image.tolist()


					# * ---------- SEND data to API --------- *

					r = requests.post(url='http://0.0.0.0:5000/receive_data', json=json_to_export)
					print("Status: ", r.status_code)

				face_names.append(name)
			
		process_this_frame = not process_this_frame




	## def stream_browser(frame):
	## 	yield (b'--frame\r\n'
	## 		   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


	# imageHub = imagezmq.ImageHub()
	mq = IronMQ(host='host current machine name', port='enter port', project_id='id', token='token')

	while True:

		# lock = threading.Lock()

		# lock.acquire()
		# image, frame = camera.get_frame()

		# imageHub = imagezmq.ImageHub()

		# (rpiName, image) = imageHub.recv_image()
		# imageHub.send_reply(b'OK')

		queue = mq.queue("my_queue")
		image = queue.get()
		print(type(image))
		queue.delete(image["messages"][0]["id"])


		frame = copy.deepcopy(image)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

		faces = face_cascade.detectMultiScale(gray, 1.3, 4)
		for (x,y,w,h) in faces:
			frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

		ret, jpeg = cv2.imencode('.jpg', frame)
		# print(type(jpeg))

		frame = jpeg.tobytes()
		
		
		print(type(frame))




		# continuously save image in image_for_add_emp folder, so that it can be used anytime for add_employee.
		# path_file = os.path.join(f"/var/www/FlaskApp/FlaskApp/static/assets/img/image_for_add_emp/capture.jpg")
		path_file = "/static/assets/img/image_for_add_emp/capture.jpg"
		image_file = image.copy()
		cv2.imwrite(path_file, np.array(image_file))

		# lock.release()

		## process_frame(image)

		## stream_browser(frame)

		t1 = threading.Thread(target=process_frame, args=(image,)) 

		t1.daemon = True
		# starting thread 1 
		t1.start() 
	  
		# wait until thread 1 is completely executed 
		t1.join() 


		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



		# fps.update()
		# fps.stop()
		# print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
		# print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))




@app.route('/video_feed', methods=['GET'])
def video_feed():
	return Response(gen(),
					mimetype='multipart/x-mixed-replace; boundary=frame')




# * ---------- DATABASE CONFIG --------- *

DATABASE_USER = 'DB user name'
DATABASE_PASSWORD = 'enter password'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 'enter port'
DATABASE_NAME = 'enter DB namme'

def DATABASE_CONNECTION():
	return psycopg2.connect(user=DATABASE_USER,
							  password=DATABASE_PASSWORD,
							  host=DATABASE_HOST,
							  port=DATABASE_PORT,
							  database=DATABASE_NAME)



# * --------------------  OTHER ROUTES ------------------- *
# * ---------- Get data from the face recognition ---------- *
@app.route('/receive_data', methods=['POST'])
def get_receive_data():
	if request.method == 'POST':
		json_data = request.get_json()

			# Connect to the DB
		connection = DATABASE_CONNECTION()
		cursor = connection.cursor()


		# Check if the user is already in the DB
		try:
			# Query to check if the user has been seen by the camera today
			user_saw_today_sql_query =\
				f"SELECT * FROM users WHERE date = '{json_data['date']}' AND name = '{json_data['name']}'"

			cursor.execute(user_saw_today_sql_query)
			result = cursor.fetchall()
			connection.commit()


			# If user is already in the DB for today:
			if result:
			   print('user ALREADY IN. Updating departure details...')
			   # {FILE_PATH}/static/assets/img/
			   image_path = f"/static/assets/img/departures/{json_data['date']}/{json_data['name']}/departure.jpg"
			   image_path_for_db_dep= f"/static/assets/img/departures/{json_data['date']}/{json_data['name']}/departure.jpg"
				# Save image
			   os.makedirs(f"/static/assets/img/departures/{json_data['date']}/{json_data['name']}", exist_ok=True)
			   cv2.imwrite(image_path, np.array(json_data['picture_array']))
			   json_data['picture_path'] = image_path_for_db_dep

				# Update user in the DB
			   update_user_querry = f"UPDATE users SET departure_time = '{json_data['hour']}', departure_picture = '{json_data['picture_path']}' WHERE name = '{json_data['name']}' AND date = '{json_data['date']}'"
			   cursor.execute(update_user_querry)

			else:
				print("user IN for FIRST TIME today. Inserting details...")
				# Save image
				# {FILE_PATH}/static/assets/img/
				image_path = f"/static/assets/img/arrivals/{json_data['date']}/{json_data['name']}/arrival.jpg"
				image_path_for_db_arr=  f"/static/assets/img/arrivals/{json_data['date']}/{json_data['name']}/arrival.jpg"
				# Save image
				os.makedirs(f"/static/assets/img/arrivals/{json_data['date']}/{json_data['name']}", exist_ok=True)
				cv2.imwrite(image_path, np.array(json_data['picture_array']))
				json_data['picture_path'] = image_path_for_db_arr

				#set id for each user for a first attendance for a day
				cursor.execute('select id from users')
				new_result = cursor.fetchall()
				

				if len(new_result)==0:
					json_data['id']=id=int(0)
				else:
					ids=[int(pd.Series(ind)) for ind in new_result]
					max_id=pd.Series(ids).max()
					id=max_id+1
					json_data['id']=int(id)

				print(json_data['id'])

				# Create a new row for the user today:

				insert_user_querry = f"INSERT INTO users (id, name, date, arrival_time, arrival_picture) VALUES ({json_data['id']}, '{json_data['name']}', '{json_data['date']}', '{json_data['hour']}', '{json_data['picture_path']}');"
				cursor.execute(insert_user_querry)

		except (Exception, psycopg2.DatabaseError) as error:
			print("ERROR DB: ", error)
		finally:
			connection.commit()

			# closing database connection.
			if connection:
				cursor.close()
				connection.close()
				print("PostgreSQL connection is closed")

		# Return user's data to the front
		return jsonify(json_data)



# * ---------- Get all the data of a particular (one) employee ---------- *
@app.route('/get_employee/<string:name>', methods=['GET'])
def get_employee(name):
	answer_to_send = {}

	keys=["id", "empName", "date", "inTime",  "outTime", "inTimeImg", "outTimeImg"]
	employee_name=str(name).lower()

			# Connect to DB
	connection = DATABASE_CONNECTION()
	cursor = connection.cursor()
	# Check if the user is already in the DB00
	try:
		# Query the DB to get all the data of a user:
		user_information_sql_query = f"SELECT * FROM users WHERE name = '{employee_name}'"

		cursor.execute(user_information_sql_query)
		result = cursor.fetchall()
		connection.commit()


		# if the user exist in the db:
		if result:
			print('RESULT: ',result)
			# Structure the data and put the dates in string for the front. 
			# Use the queried path of arrival_picture (index 5 in dictionary) from 'answer_to_send' and get the image from same path to display on UI.
			for k,v in enumerate(result):
				answer_to_send[k] = {}
				for ko,vo in zip(keys, result[k]):
					answer_to_send[k][ko] = str(vo)
			print('answer_to_send: ', answer_to_send)
		else:
			answer_to_send = {'error': 'User not found...'}

	except (Exception, psycopg2.DatabaseError) as error:
		print("ERROR DB: ", error)
	finally:
		# closing database connection:
		if (connection):
			cursor.close()
			connection.close()

	# Return the user's data to the front
	return jsonify(answer_to_send)



# * --------- Get the 5 last users seen by the camera --------- *
@app.route('/get_5_last_entries', methods=['GET'])
def get_5_last_entries():
	answer_to_send = {}

	keys=[ "id", "empName", "date", "inTime",  "outTime", "inTimeImg", "outTimeImg"]

		# Connect to DB
	connection = DATABASE_CONNECTION()
	cursor = connection.cursor()

	# Check if the user is already in the DB
	try:

		# Query the DB to get all the data of a user:
		lasts_entries_sql_query = f"SELECT * FROM users ORDER BY id DESC LIMIT 5;"

		cursor.execute(lasts_entries_sql_query)
		result = cursor.fetchall()
		connection.commit()

		# if DB is not empty:
		if result:
			# Structure the data and put the dates in string for the front
			for k, v in enumerate(result):
				answer_to_send[k] = {}
				for ko, vo in zip(keys, result[k]):
					answer_to_send[k][ko] = str(vo)
		else:
			answer_to_send = {'error': 'error detect'}

	except (Exception, psycopg2.DatabaseError) as error:
		print("ERROR DB: ", error)
	finally:
		# closing database connection:
		if (connection):
			cursor.close()
			connection.close()

	# Return the user's data to the front
	return jsonify(answer_to_send)



# * ---------- Add new employee ---------- *
@app.route('/add_employee/<string:name>', methods=['GET'])
# @cross_origin(supports_credentials=True)
def add_employee(name):
	try:
		# Get the picture from the request
		# image_file = request.files['image']
		# print(request.form['nameOfEmployee'])
		employee_name=str(name).lower()
		# print(employee_name)
		# data = request.data

		#read image from image_for_add_emp folder where it is being continuously saved in running video stream and save the same read image in users folder with employee name when add_employee route is being hit.
		in_image = cv2.imread("/static/assets/img/image_for_add_emp/capture.jpg")
		file_path = os.path.join(f"/static/assets/img/users/{employee_name}.jpg")
		cv2.imwrite(file_path, np.array(in_image))
		# image_file = Image.open(BytesIO(base64.b64decode(data)))
		# image_file.save(file_path)
		answer = 'success'

		# encoded_data = data.split(',')[1]
		# nparr = np.fromstring(encoded_data.decode('base64'), np.uint8)
		# img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

		# Store it in the folder of the know faces:
		
		# file_path = os.path.join(f"assets/img/users/{employee_name}.jpg")
		# image_file.save(file_path)
		# answer = 'success'
	except:
		answer = 'error'
	return jsonify(answer)

 # redirect(url_for('video_feed'))

# * ---------- Get employee list (names)---------- *
@app.route('/get_employee_list', methods=['GET'])
def get_employee_list():
	employee_list = {}

	# Walk in the user folder to get the user list
	walk_count = 0
	for file_name in os.listdir(f"/static/assets/img/users/"):
		# Capture the employee's name with the file's name
		name = re.findall("(.*)\.jpg", file_name)
		if name:
			employee_list[walk_count] = name[0]
		walk_count += 1

	return jsonify(employee_list)



# * ---------- Delete employee ---------- *
@app.route('/delete_employee/<string:name>', methods=['GET'])
def delete_employee(name):
	try:
		employee_name=str(name).lower()
		# Remove the picture of the employee from the user's folder:
		print('name: ', name)
		file_path = os.path.join(f'/static/assets/img/users/{employee_name}.jpg')
		os.remove(file_path)
		answer = 'success'
	except:
		answer = 'error'

	return jsonify(answer)


	

# # * -------------------- RUN SERVER -------------------- *
if __name__ == '__main__':
	# * --- DEBUG MODE: --- *
	# app.run()
	app.run(host='0.0.0.0', port=5000, debug=True)
	#  * --- DOCKER PRODUCTION MODE: --- *
	# app.run(host='0.0.0.0', port=os.environ['PORT']) -> DOCKER
