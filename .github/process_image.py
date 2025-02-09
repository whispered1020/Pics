import os
import argparse
from PIL import Image

def process_image(input_path, output_dir):
    try:
        with Image.open(input_path) as img:
            filename = os.path.splitext(os.path.basename(input_path))[0]
            relative_path = os.path.relpath(input_path, start=os.getcwd())
            relative_dir = os.path.dirname(relative_path)

            if "field" in relative_path.lower():
                output_filename = f"{filename}.png"
                output_path = os.path.join(output_dir, relative_dir, output_filename)
                
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                if img.mode != "RGBA":
                    img = img.convert("RGBA")
                
                img = img.resize((512, 512))
                img.save(output_path, "PNG", optimize=True)
            else:
                output_filename = f"{filename}.jpg"
                output_path = os.path.join(output_dir, relative_dir, output_filename)
                
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                if img.mode == "RGBA":
                    img = img.convert("RGB")
                
                img = img.resize((322, 470))
                file_size_kb = os.path.getsize(input_path) / 1024
                if file_size_kb <= 60:
                    img.save(output_path, "JPEG", quality=90, optimize=True)
                else:
                    img.save(output_path, "JPEG", quality=80, optimize=True)

    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output_dir", help="Output directory")
    args = parser.parse_args()
    
    process_image(args.input, args.output_dir)