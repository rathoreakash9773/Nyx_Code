# -*- coding: utf-8 -*-
"""WaterMarkRemovalWorking.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pmxtraMb5VIkaQJQpzIdzrTDlMAWYHYr
"""

import os
import subprocess
import shlex
import random
import shutil

def extract_frames(input_video, output_directory, max_frames=50):
    os.makedirs(output_directory, exist_ok=True)

    # Get key frame timings
    ffprobe_cmd = f'ffprobe -hide_banner -loglevel warning -select_streams v -skip_frame nokey -show_frames -show_entries frame=pkt_dts_time "{input_video}" | grep "pkt_dts_time="'
    keyframes_time = subprocess.check_output(ffprobe_cmd, shell=True, text=True).split('\n')
    keyframes_time = [line.split('=')[1] for line in keyframes_time if line]

    # Shuffle and select a subset of key frames
    selected_keyframes = random.sample(keyframes_time, min(len(keyframes_time), max_frames))

    # Extract frames
    for i, frame_time in enumerate(selected_keyframes):
        if not frame_time.replace('.', '').isdigit():
            print(f"Skipping unrecognized timing: {frame_time}")
            continue

        output_frame_path = os.path.join(output_directory, f'output_{i}.png')
        ffmpeg_cmd = f'ffmpeg -y -hide_banner -loglevel error -ss {frame_time} -i "{input_video}" -vframes 1 "{output_frame_path}"'
        subprocess.run(shlex.split(ffmpeg_cmd))

    return len(selected_keyframes)

def remove_watermark(input_video, output_video, mask_path):
    # Remove watermark using ffmpeg
    ffmpeg_cmd = f'ffmpeg -hide_banner -loglevel warning -y -stats -i "{input_video}" -acodec copy -vf "removelogo={mask_path}" "{output_video}"'
    subprocess.run(shlex.split(ffmpeg_cmd))

def main(input_folder, output_folder, mask_path=None, max_frames=50):
    os.makedirs(output_folder, exist_ok=True)

    for video_file in os.listdir(input_folder):
        if video_file.endswith(('.mp4', '.avi', '.mkv')):  # Add more video formats if needed
            input_video_path = os.path.join(input_folder, video_file)
            output_video_path = os.path.join(output_folder, f'{os.path.splitext(video_file)[0]}_cleaned.mp4')

            # Extract frames
            extracted_frames = extract_frames(input_video_path, os.path.join(os.getcwd(), 'frames'), max_frames)

            # Check if at least 2 frames were extracted
            if extracted_frames < 2:
                print(f"{extracted_frames} frames extracted from {video_file}, need at least 2, skipping.")
                continue

            if mask_path is None:
                print(f"Error: Please provide the path to the existing watermark mask for {video_file}. Skipping.")
                continue

            print(f"Removing watermark in {video_file}...")
            remove_watermark(input_video_path, output_video_path, mask_path)

            print(f"Cleaned video saved at: {output_video_path}")

    # Clean up temporary directory
    shutil.rmtree(os.path.join(os.getcwd(), 'frames'))

    print("Done")

if __name__ == "__main__":
    # Example usage
    main(
        input_folder="/content/sample_data/input videos",
        output_folder="/content/sample_data/output videos",
        mask_path="/content/videomask.png",  # Provide the path to your existing mask
        max_frames=50
    )