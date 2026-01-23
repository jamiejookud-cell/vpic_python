import os
import imageio.v2 as imageio
from natsort import natsorted
from code_python.scripts.config.folder_paths import FOLDER_PATH, FIG_OUTPUT_PATH

OUTPUT_PATH = f"{FOLDER_PATH}/videos"

filename_prefix = 'rho_i'
file_output_name = filename_prefix + "_animation"
FPS = 30

def create_video_from_images(filename: str):
    # 1. Get and sort images
    image_files = [
        f for f in os.listdir(FIG_OUTPUT_PATH) if f.endswith('.png') and f.startswith(filename_prefix)
    ]
    image_files = natsorted(image_files)

    if not image_files:
        print("No images found!")
        return

    print(f"Processing {len(image_files)} images...")

    # 2. Set full save path
    save_path = os.path.join(OUTPUT_PATH, f"{filename}.mp4")

    # 3. Use a context manager to handle the writer
    # This automatically handles writer.close() even if an error occurs
    with imageio.get_writer(save_path, fps=FPS) as writer:
        for img_name in image_files:
            img_path = os.path.join(FIG_OUTPUT_PATH, img_name)
            image = imageio.imread(img_path)

            # Add image to video
            writer.append_data(image)
            print(f"Added {img_name}", end='\r')

    print(f"\n[Done] Video saved to: {save_path}")

create_video_from_images(file_output_name)