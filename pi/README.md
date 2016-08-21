# Getting the Pi up and running

## Setting Up the Pi

First things first, get an sd disk and get a raspberry pi image on it (by following these instructions)[https://www.raspberrypi.org/documentation/installation/installing-images/mac.md

```
diskutil list
#find your sd cart in the list
diskutil unmountDisk /dev/<disk #>
#e.g. diskutil unmountDisk /dev/disk5
sudo dd bs=1m if=</path/to/raspbian.img> of=/dev/<disk #>
#e.g. sudo dd bs=1m if=~/Downloads/2016-05-27-raspbian-jessie.img of=/dev/rdisk5

```

Then install your camera by plugging it in to the board.

### First Boot
Boot up your raspberry pi.

I'm running this in desktop mode.  Yes it requires more cpu, but this allows me to more easily test the webcamera by plugging in to a display.

Add wifi credentials to the pi.
Set correct timezone.


### Test Camera
First enable the camera.
Test camera functionality by running a python script
```import picamera from PiCamera
from time import sleep
camera = PiCamera()
camera.start_preview()
sleep(5)
camera.stop_preview()
```
If you saw camera output on your display for 5 seconds, great, otherwise, you will need to debug the camera connection.

### Getting some needed software on your pi

At this point, ssh to the pi will suffice.  To find the ip address, from you're device
`arp -a | grep raspberry | awk '{print $2}'`

then 

`ssh pi@<ip address>`

#### Text editor

`sudo apt-get install vim`

#### DropBox Uploader

See [github](https://github.com/andreafabrizi/Dropbox-Uploader) for instructions.  Of course you could write that part to use scp or just save to disk.  I am using dropbox because they gave be 1 TB and I can quickly use the same location as a cdn for (the website)[../website/README.md]



