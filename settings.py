import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

# how many more frames to record after no movement
count_down_frame = int(os.getenv("COUNT_DOWN_FRAME", "100"))

include_contour = True

telegram_api_key = os.getenv("TELEGRAM_API_KEY", "")

user_id = os.getenv("USER_ID", "")

# maximum video number
max_frame_buffer = 5000 

font_size = float(os.getenv("FONT_SIZE", "0.5"))

# movement change patch size to trigger recording unit: pix^2
trigger_area = int(os.getenv("TRIGGER_AREA", "100"))

# resize frame to this width
video_width = int(os.getenv("VIDEO_WIDTH", "480")) 
