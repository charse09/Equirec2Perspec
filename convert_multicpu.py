import os
import cv2 
import Equirec2Perspec as E2P
from PIL import Image
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Manager

class ImageProcessor:
    def __init__(self, image_counter, image_counter_lock):
        self.image_counter = image_counter
        self.image_counter_lock = image_counter_lock

    def process_frame(self, frame_num, FOV, theta_step, phi_step, height, width, num_horizontal, num_vertical):
        frame_filename = f"frame{frame_num}.png"
        equ = E2P.Equirectangular(frame_filename)    # Load equirectangular image

        # Generate and save perspective images moving horizontally right and vertically up
        for row in range(num_vertical):
            for col in range(num_horizontal):
                theta = col * theta_step
                phi = row * phi_step

                img = equ.GetPerspective(FOV, theta, phi, height, width) # Specify parameters(FOV, theta, phi, height, width)

                img = img[:,:,::-1]
                img1 = Image.fromarray(img.astype('uint8')).convert('RGB')

                with self.image_counter_lock:
                    image_filename = f"{self.image_counter.value:05d}.jpg"
                    img1.save(image_filename)
                    self.image_counter.value += 1

if __name__ == '__main__':
    # Fixed values
    FOV = 110
    width = 1440
    height = 1080

    num_horizontal = 8
    num_vertical = 2

    theta_step = 45  # Angle value of moving right horizontally
    phi_step = 30  # Angle value of moving up vertically

    num_frames = 3387  # Enter the number of images here
    max_workers = 8  # Adjust this based on the number of available CPU cores

    with Manager() as manager:
        image_counter = manager.Value('i', 0)
        image_counter_lock = manager.Lock()

        # Use ProcessPoolExecutor for parallel processing
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            image_processor = ImageProcessor(image_counter, image_counter_lock)

            futures = [
                executor.submit(
                    image_processor.process_frame,
                    frame_num, FOV, theta_step, phi_step, height, width, num_horizontal, num_vertical
                )
                for frame_num in range(num_frames)
            ]

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error processing frame: {e}")
