from picamera import PiCamera
from time import sleep
import time
import subprocess
import os
import json
import smtplib
import logging
#
#  Creating the useful functions
#

def read_json(json_path = "sample-configure.json"):
    """
    Helper function that loads a json from a file and closes the file safely
    :param json_path: string or unicode with relative filepath
    :return: dictionary containing all the json information
    """
    with open(json_path, "r") as json_file:
        return json.load(json_file)

def take_clip(camera, file_name):
    camera.vflip = True
    camera.start_preview()
    sleep(5)
    camera.capture(file_name)
    camera.stop_preview()

print read_json()

def send_email(subject, body, config):
    logger = logging.getLogger(__name__)

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % \
              (config['email']['from'],
               ", ".join(config['email']['to']),
               subject,
               body)
    logger.info("Message body: %s", message)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        #note this is cheating, we're using the first receiptiant as the login user
        #this does have the nice property that you always receive a copy in your inbox
        server.login(config['email']['to'][0], config['email']['password'])
        server.sendmail(config['email']['from'], config['email']['to'], message)
        server.close()
        logger.info("Sent mail to: %s", config['email']['to'])
    except Exception as e:
        logger.error("Failed to send mail: %s ", str(e))
        #you could use this if you actually wanted to cause a halt
        #raise e


def make_video(working_dir):
    logger = logging.getLogger(__name__)
    for file in os.listdir(working_dir):
        if file.endswith(".jpg"):
            staged_file_name = working_dir + file
            logger.info("Making video from: %s", staged_file_name)
            command = "ffmpeg -r 60 -f image2 -s 1920x1080 -i " + staged_file_name + " -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4"
            logger.debug("Running command: %s", command)
            args = command.split(" ")
            logger.debug("Args: %s", args)
            try:
                out = subprocess.check_call(*args)
                if out is 0:
                    logger.debug("Zero exit code: %s", out)
                else:
                    logger.warn("Nonzero exit code: %s", out)
            except Exception as e:
                # don't delete file
                # email the master
                logger.error("Failed to encode video: %s ", str(e))

def update_dropbox(config):
    logger = logging.getLogger(__name__)
    working_dir = config['file_system']['working_dir'] + "images/"
    remote_dir = config['file_system']['remote_dir']
    dropbox_uploader = config['file_system']['dropbox_upload']
    for file in os.listdir(working_dir):
        if file.endswith(".jpg"):
            staged_file_name = working_dir + file
            remote_file_name = remote_dir + file
            print(staged_file_name)
            try:
                #this allows us to detct if the subprocess didn't even return
                out = "Subprocess did not run"
                subprocess_string = '\n'.join(dropbox_uploader,
                                              "upload",
                                              staged_file_name,
                                              remote_file_name)
                out = subprocess.check_call([dropbox_uploader, "upload", staged_file_name, remote_file_name])
                if out is 0:
                    logger.debug("Zero exit code: %s", out)
                else:
                    logger.warn("Nonzero exit code: %s", out)
                    else_email_body = '\n'.join('Subprocess called:', subprocess_string)
                    send_email("Pi - TimeLapsing - Process Code %s" % out, else_email_body)
            except Exception as e:
                # don't delete file
                # email the master
                except_email_body = 'Error was as follows: %s' % str(e)
                logger.error("Failed to encode video: %s ", str(e))
                send_email("Pi - TimeLapsing - Exception: ", except_email_body)

def start_timelapse(config):

    working_dir = config['file_system']['working_dir'] + "images/"
    camera = PiCamera()

    while True:
        now = time.localtime().tm_hour
        if now < 15 and now > 8:
            time_string = time.strftime('%y%m%d%H%M')
            file_name = working_dir + time_string + '.jpg'
            update_dropbox(config)
            take_clip(camera, file_name)


        sleep(900)
