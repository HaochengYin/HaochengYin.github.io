import cv2
from PIL import Image
import os
import argparse
from tqdm.auto import tqdm

def convert_mp4_to_webp(input_path, output_path, fps=10, quality=80):
    """
    Convert MP4 video to animated WebP image with a progress bar.
    
    :param input_path: Path to the input MP4 file
    :param output_path: Path to save the output WebP file
    :param fps: Frames per second for the output WebP (default: 10)
    :param quality: Quality of WebP image, 0-100 (default: 80)
    :return: Path of the saved WebP file
    """
    # Open the video file
    video = cv2.VideoCapture(input_path)
    
    # Get video properties
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video_fps = video.get(cv2.CAP_PROP_FPS)
    
    # Calculate frame interval
    if fps > video_fps:
        print(f"Warning: Requested fps ({fps}) is higher than video fps ({video_fps}). Using video fps.")
        fps = video_fps
    frame_interval = max(1, round(video_fps / fps))
    
    frames = []
    count = 0
    
    # Create a tqdm progress bar
    with tqdm(total=total_frames, desc="Converting frames", unit="frame") as pbar:
        while True:
            success, frame = video.read()
            if not success:
                break
            
            if count % frame_interval == 0:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(frame_rgb)
                frames.append(pil_img)
            
            count += 1
            pbar.update(1)
    
    video.release()
    
    if frames:
        print("Saving WebP file...")
        # Save as WebP
        frames[0].save(output_path, format='WebP', append_images=frames[1:], 
                       save_all=True, duration=int(1000/fps), loop=0, quality=quality)
        print(f"Successfully converted {input_path} to {output_path}")
        return output_path
    else:
        print("No frames were extracted from the video.")
        return None

def main():
    parser = argparse.ArgumentParser(description="Convert MP4 video to animated WebP image.")
    parser.add_argument("input_path", help="Path to the input MP4 file")
    parser.add_argument("-o", "--output_path", help="Path to save the output WebP file (default: same name as input with .webp extension)")
    parser.add_argument("-f", "--fps", type=int, default=10, help="Frames per second for the output WebP (default: 10)")
    parser.add_argument("-q", "--quality", type=int, default=80, help="Quality of WebP image, 0-100 (default: 80)")
    
    args = parser.parse_args()
    
    # If output path is not specified, use the same name as input but with .webp extension
    if not args.output_path:
        args.output_path = os.path.splitext(args.input_path)[0] + '.webp'
    
    convert_mp4_to_webp(args.input_path, args.output_path, args.fps, args.quality)

if __name__ == "__main__":
    main()

'''
usage: python video2webp.py path/to/your/video.mp4 -f 15 -q 90
'''



