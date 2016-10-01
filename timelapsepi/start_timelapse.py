"""
Timelapse camera modeule. More description goes here
"""
from picamera import PiCamera
from time import sleep
import time
import subprocess
import os
import json
import logging


def read_json(json_path = "configure.json"):
    """
    Helper function that loads a json from a file and closes the file safely
    :param json_path: string or unicode with relative filepath
    :return: dictionary containing all the json information
    """
    with open(json_path, "r") as json_file:
        return json.load(json_file)


def take_clip(camera, file_name, clip_length=5):
    """
    Take a short clip and save
    :param camera: PiCamera object from module picamera
    :param file_name: destination for file to be saved
    :return:
    """
    #camera.vflip = True
    camera.start_preview()
    sleep(clip_length)
    #this is a little weird, you would normally expect to hand it a file object, not a file path
    camera.capture(file_name)
    camera.stop_preview()



def update_dropbox(file, config):
    """
    Uploads all files in a working directory
    :param config: json config for this script. See sample-configure.json for an example
    :return:
    """
    logger = logging.getLogger(__name__)
    working_dir = config['file_system']['working_dir'] + "images/"
    remote_dir = config['file_system']['remote_dir']
    dropbox_uploader = config['file_system']['dropbox_upload']
    staged_file_name = working_dir + file
    remote_file_name = remote_dir + file
    logger.debug("Staged file name: %s", staged_file_name)
    try:
        #this allows us to detct if the subprocess didn't even return
        out = "Subprocess did not run"
        subprocess_string = '\n'.join([dropbox_uploader,
                                      "upload",
                                      staged_file_name,
                                      remote_file_name])
        out = subprocess.check_call([dropbox_uploader, "upload", staged_file_name, remote_file_name])
        if out is 0:
            rm_file = os.remove(staged_file_name)
            logger.debug("Zero exit code: %s", out)
        else:
            logger.warn("Nonzero exit code: %s", out)

    except Exception as e:
        # don't delete file
        logger.error("Failed to encode video: %s ", str(e))


def update_all_dropbox(config):
    """
    Uploads all files in a working directory
    :param config: json config for this script. See sample-configure.json for an example
    :return:
    """
    working_dir = config['file_system']['working_dir'] + "images/"
    for file in os.listdir(working_dir):
        if file.endswith(".jpg"):
            update_dropbox(file, config)



def start_timelapse(config):
    """
    Begins endlessly running timelapse process
    :param config: json config for this script. See sample-configure.json for an example
    :return: never returns a value
    """
    working_dir = config['file_system']['working_dir'] + "images/"
    camera = PiCamera()
    while True:
        if 6 < time.localtime().tm_hour < 16:
            time_string = time.strftime('%y%m%d%H%M')
            file_name = working_dir + time_string + '.jpg'
            take_clip(camera, file_name)
            update_all_dropbox(config)

        sleep(900)



if __name__ == '__main__':
    """
    Run with defaults if called as a script.
    TODO: pass command line argument allowing someone to specify different json
    """
    start_timelapse(read_json())
