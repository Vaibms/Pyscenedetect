from scenedetect import SceneManager
from scenedetect.detectors import ContentDetector
from scenedetect.video_splitter import split_video_ffmpeg
from scenedetect import open_video
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

import os

video_path = 'video_test.mp4'
output_dir = 'scenes_output'

# Step 1: Detect scenes
video = open_video(video_path)
scene_manager = SceneManager()
scene_manager.add_detector(ContentDetector(threshold=10.0))

scene_manager.detect_scenes(video)
scene_list = scene_manager.get_scene_list()

print(f"Detected {len(scene_list)} scenes!")

# Step 2: Create output directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Step 3: Export each scene using moviepy (ffmpeg)
for i, (start, end) in enumerate(scene_list):
    start_sec = start.get_seconds()
    end_sec = end.get_seconds()
    output_filename = os.path.join(output_dir, f'scene_{i+1:03d}.mp4')
    
    print(f"Exporting Scene {i+1}: {start_sec:.2f}s to {end_sec:.2f}s -> {output_filename}")
    ffmpeg_extract_subclip(video_path, start_sec, end_sec, output_filename)

print("Scene splitting complete.")
