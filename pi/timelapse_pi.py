from picamera import PiCamera
from time import sleep
import time
import subprocess
import os
import configure
import smtplib
#
#  Creating the useful functions
#

def cameraFunc():
	camera = PiCamera()
	camera.vflip = True
	camera.start_preview()
	sleep(5)
	camera.capture(file_name)
	camera.stop_preview()

def send_email(subject, body):
	user = configure.email["to"]
	pwd = configure.email["password"]
    	FROM = configure.email["from"]
    	recipient = configure.email["to"]
    	TO = recipient if type(recipient) is list else [recipient]
    	SERVER = configure.email["smtp_server"]
    	PORT = configure.email["smtp_port"]
    	SUBJECT = subject
    	TEXT = body

    	# Prepare actual message
    	message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
    	print(message)
    	try:
        	server = smtplib.SMTP("smtp.gmail.com", 587)
        	server.ehlo()
        	server.starttls()
        	server.login(user, pwd)
        	server.sendmail(FROM, TO, message)
        	server.close()
        	print 'successfully sent the mail'
    	except Exception as e:
        	print("failed to send mail " + str(e))


def make_video(working_dir):
	for file in os.listdir(working_dir):
		if file.endswith(".jpg"):
			staged_file_name = working_dir + file
			print(staged_file_name)
			command = "ffmpeg -r 60 -f image2 -s 1920x1080 -i " + staged_file_name + " -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4"
			print(command)
			args = command.split(" ")
			print(args)
			e = ''
			try:
			
				out = subprocess.check_call(*args)
				if out is 0:
					print(out)
				
				else:
					print(out + "is not zero")
			except e:
		    		# don't delete file
		    		# email the master
				print(e + "hit e")

#Define Useful Variables

working_dir = configure.file_system["working_dir"] + "images/"
remote_dir = configure.file_system["remote_dir"]
dropbox_uploader = configure.file_system["dropbox_upload"]
camera = PiCamera()

#Start the For Loop

while True:
	now = time.localtime().tm_hour
	if now < 15 and now > 8:
		e = ''
		time_string = time.strftime('%y%m%d%H%M')
		file_name = working_dir + time_string + '.jpg'
		
		camera.start_preview()
		sleep(5)
		camera.capture(file_name)
		camera.stop_preview()

		for file in os.listdir(working_dir):
			if file.endswith(".jpg"):
				staged_file_name = working_dir + file
				remote_file_name = remote_dir + file
				print(staged_file_name)
				try:
					out = subprocess.check_call([dropbox_uploader, "upload",  staged_file_name, remote_file_name])
					if out is 0:
						print(out)
						rm_file = os.remove(staged_file_name)
					else:
						else_email_body = 'Error was as follows: '+  e
						send_email("Pi - TimeLapsing - Out is 1", else_email_body)
						print(out + "is not zero")
				except e:
				    	# don't delete file
				    	# email the master
				    	except_email_body = 'Error was as follows: ' + e
				    	send_email("Pi - TimeLapsing - Except Block", except_email_body)
					print(except_email_body)

	sleep(900)
