import numpy as np
import os
import cv2
from twilio.rest import Client


ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_NUMBER = os.environ['TWILIO_NUMBER']
TARGET_NUMBER = os.environ['TARGET_NUMBER']


MOTION_FRAME = 24
IMAGE_HEIGHT = 240
THRESHOLD = 80

# Get the most recent file saved
contents = os.listdir('.')

vid_paths = [path for path in contents if path.endswith('.mp4')]
vid_path = vid_paths[-1]
vidcap = cv2.VideoCapture(vid_path)


# Capture first frame
success, frame = vidcap.read()
if success:
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    np_frame1 = np.asarray(frame, dtype='uint8')

# Fast forward
for i in range(24):
    vidcap.read()

# Capture motion frame
success, frame = vidcap.read()
if success:
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    np_frame2 = np.asarray(frame, dtype='uint8')

# Compare top half of the images
result = np.allclose(
    np_frame1[:IMAGE_HEIGHT, :],
    np_frame2[:IMAGE_HEIGHT, :],
    atol=THRESHOLD
    )

if result == False:
    # Send a text to myself via twilio
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages.create(
            body='Something tall detected!',
            from_=TWILIO_NUMBER,
            to=TARGET_NUMBER
        )
