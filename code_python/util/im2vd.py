import os
import imageio.v2 as imageio
from natsort import natsorted  # For natural sorting like T.1, T.2, ..., T.10

# -------------------------------------------------------------------------------- #
#                                  CONFIGURATION                                   #
# -------------------------------------------------------------------------------- #
IMAGE_FOLDER_PATH = '/pscratch/sd/k/kittiya/mean_project/vpic2/code_python2/images'
OUTPUT_PATH = "/pscratch/sd/k/kittiya/mean_project/vpic2/code_python2/videos"

filename_prefixes = '_'
FPS = 10                # Frames per second for the output video
OPTION = 1

# -------------------------------------------------------------------------------- #
#                                 CORE FUNCTIONS                                   #
# -------------------------------------------------------------------------------- #
def create_video_from_images():
    """Create and save an mp4 video from a sorted list of image filenames,
    only including images with the same size as the first one."""
    name = filename_prefixes
    image_files = [
        f for f in os.listdir(IMAGE_FOLDER_PATH) if f.endswith('.png') and f.startswith(filename_prefixes)
    ]
    image_files = natsorted(image_files)
    print(image_files)

    # Read the first image to get reference size
    first_image_path = os.path.join(IMAGE_FOLDER_PATH, image_files[0])
    first_image = imageio.imread(first_image_path)
    reference_shape = first_image.shape
    print(f"[Info] Reference image shape: {reference_shape}")

    writer = imageio.get_writer(f"{OUTPUT_PATH}/{name}.mp4", fps=FPS)
    writer.close()
    print(f"[Done] Video saved to: {OUTPUT_PATH}/{name}.mp4")

create_video_from_images()
