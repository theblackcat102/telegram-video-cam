import os
import numpy as np
import cv2
import imutils
import argparse
import datetime
import multiprocessing as mp
from settings import (
        max_frame_buffer, user_id, 
        telegram_api_key, count_down_frame,
        video_width,
        trigger_area,
        include_contour
)
from telegram.bot import Bot
bot = None

if len(user_id) != 0 and len(telegram_api_key) != "":
    bot = Bot(token=telegram_api_key)
    print('init bot')


cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object

firstFrame = None
frame_buffers = []
frame_count_down = -1


def save_frame(frame_buffers):
    frame_size = frame_buffers[0].shape[:2]
    frame_size = (int(frame_size[1]), int(frame_size[0]))

    filename = datetime.datetime.now().strftime("%A_%d_%B_%Y_%I:%M:%S%p.mp4")
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'MP4V'), 10.0, frame_size)
    print('write to buffer %d' % len(frame_buffers))
    for frame in frame_buffers:
        out.write(frame)

    out.release()
    if bot is not None:
        print('write to telegram')
        bot.send_message(chat_id=user_id, text='New movement!')
        bot.send_video(chat_id=user_id, 
            video=open(filename, 'rb'), supports_streaming=True)
        print('finish sending')
        os.remove(filename)


pool = mp.Pool() 
try:
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            # frame = cv2.flip(frame, offset_angle)
            # print(frame.shape)
            # write the flipped frame
            frame = imutils.resize(frame, width=video_width)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            # if the first frame is None, initialize it
            if firstFrame is None:
                firstFrame = gray
                continue
            frameDelta = cv2.absdiff(firstFrame, gray)
            firstFrame = gray

            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < trigger_area:
                    continue
                if include_contour:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                print('detected! %d' % frame_count_down)
                if frame_count_down != count_down_frame:
                    frame_count_down = count_down_frame

            if frame_count_down > 0:

                cv2.putText(frame, datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
                frame_buffers.append(frame)
                frame_buffers = frame_buffers[-max_frame_buffer:]
                frame_count_down = frame_count_down - 1

            if frame_count_down == 0:

                # async save frame
                if len(frame_buffers) > 0:
                    print('save frame')
                    # new_frame_buff = [ f.copy() for f in frame_buffers ]
                    save_frame(frame_buffers)
                    # pool.apply_async(save_frame, (frame_buffers,))
                    frame_buffers = []
                frame_count_down = -1
            # show the frame and record if the user presses a key
            # cv2.imshow("Security Feed", frame)
            # cv2.imshow("Thresh", thresh)
            # cv2.imshow("Frame Delta", frameDelta)
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key is pressed, break from the lop
            if key == ord("q"):
                break

            #cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
except KeyboardInterrupt:
    if len(frame_buffers) > 0:
        frame_size = frame_buffers[0].shape[:2]
        frame_size = (int(frame_size[1]), int(frame_size[0]))

        filename = datetime.datetime.now().strftime("%A_%d_%B_%Y_%I:%M:%S%p.mp4")
        out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'MP4V'), 10.0, frame_size)
        print('write to buffer %d' % len(frame_buffers))
        for frame in frame_buffers:
            out.write(frame)
        out.release()
    cap.release()
    pool.join()
    pool.close()

# Release everything if job is finished
cap.release()
# cv2.destroyAllWindows()