import argparse
import os
from PIL import Image

def convert_to_webp(input_path, output_dir=None, quality=80):
    """
    Convert PNG or JPEG image to WebP format.
    
    :param input_path: Path to the input image file
    :param output_dir: Directory to save the output WebP file (default: same as input)
    :param quality: Quality of WebP image, 0-100 (default 80)
    :return: Path of the saved WebP file
    """
    # Get the directory and filename of the input image
    input_dir, input_filename = os.path.split(input_path)
    
    # If no output directory is specified, use the input directory
    if output_dir is None:
        output_dir = input_dir
    
    # Create output filename with .webp extension
    output_filename = os.path.splitext(input_filename)[0] + '.webp'
    
    # Join the output directory and filename
    output_path = os.path.join(output_dir, output_filename)
    
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGB if the image is in RGBA mode (for PNGs with transparency)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # Save as WebP
            img.save(output_path, 'WEBP', quality=quality)
        
        print(f"Successfully converted {input_path} to {output_path}")
        return output_path
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert PNG or JPEG image to WebP format.")
    parser.add_argument("input_path", help="Path to the input image file")
    parser.add_argument("-o", "--output_dir", help="Directory to save the output WebP file (default: same as input)")
    parser.add_argument("-q", "--quality", type=int, default=80, help="Quality of WebP image, 0-100 (default: 80)")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the conversion function
    convert_to_webp(args.input_path, args.output_dir, args.quality)

if __name__ == "__main__":
    main()

'''
usage: python image2webp.py path/to/your/image.png -o path/to/output/directory -q 90
'''