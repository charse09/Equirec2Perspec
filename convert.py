import os
import cv2 
import Equirec2Perspec as E2P
from PIL import Image

if __name__ == '__main__':

    #Fixed values
    FOV = 110
    width = 1440
    height = 1080

    num_horizontal = 8
    num_vertical = 2

    #Counter for image numbering
    image_counter = 48

    theta_step = 45 #angle value of moving right horizontally
    phi_step = 30 #angle value of moving up vertically

    num_frames = 356 #Enter the number of images here

    #repeat until the number of input images
    for frame_num in range(num_frames):
        frame_filename = f"frame{frame_num}.png"
        equ = E2P.Equirectangular(frame_filename)    # Load equirectangular image

        #Generate and save perspective images moving horizontal right and up vertically
        for row in range(num_vertical):
            for col in range(num_horizontal):
                theta = col * theta_step
                phi = row * phi_step

                img = equ.GetPerspective(FOV, theta, phi, height, width) # Specify parameters(FOV, theta, phi, height, width)
                
                img = img[:,:,::-1]
                img1 = Image.fromarray(img.astype('uint8')).convert('RGB')

                image_filename = f"{image_counter:04d}.jpg"
                img1.save(image_filename)

                image_counter += 1
