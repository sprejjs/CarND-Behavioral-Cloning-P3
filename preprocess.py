import cv2
import csv
import matplotlib.image as mpimg
import numpy as np
from random import randint

steering_angle_adjustment = 0.25

def read_data(driving_log_path, return_images=True, pre_process=False, flip=False, dropSmallValuesWithRate=0):
    X_train = []
    y_train = []

    if not return_images:
        pre_process = False
        flip = False

    file = open(driving_log_path)

    reader = csv.reader(file)
    for row in reader:
        # Skip the title row
        if (row[3] != "steering"):
            center_image = row[0][row[0].index("IMG/"):]
            left_image = row[1][row[1].index("IMG/"):]
            right_image = row[2][row[2].index("IMG/"):]

            center_angle = float(row[3])
            left_angle = center_angle + steering_angle_adjustment
            right_angle = center_angle - steering_angle_adjustment

            randomInteger = randint(0, 100)

            if abs(center_angle) <= 0.2 and randomInteger <= dropSmallValuesWithRate:
                continue

            if return_images:
                center_image = mpimg.imread(center_image)
                left_image = mpimg.imread(left_image)
                right_image = mpimg.imread(right_image)

            if pre_process:
                center_image = easy_process(center_image)
                left_image = easy_process(left_image)
                right_image = easy_process(right_image)

            X_train.append(center_image)
            X_train.append(left_image)
            X_train.append(right_image)

            y_train.append(center_angle)
            y_train.append(left_angle)
            y_train.append(right_angle)

            if flip:
                X_train.append(np.fliplr(center_image))
                X_train.append(np.fliplr(left_image))
                X_train.append(np.fliplr(right_image))

                y_train.append(center_angle * -1)
                y_train.append(left_angle * -1)
                y_train.append(right_angle * -1)

    return [X_train, y_train]


def pre_process_image(image, use_gray=False, use_canny=False, use_blur=False, canny_low_threshold=0,
                      canny_high_threshold=0, gaussian_blur_kernel_size=0,
                      resize_image=False, crop_at_the_top=0, crop_at_the_bottom=0):
    # Cropping
    image = image[crop_at_the_top:image.shape[0] - crop_at_the_bottom, 0:image.shape[1]]

    if use_gray:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2HLS_FULL)
        image = image[:, :, 2]
        thresh = (0, 80)
        image[(image > thresh[0]) & (image <= thresh[1])] = 0

    if use_canny:
        image = cv2.Canny(image, canny_low_threshold, canny_high_threshold)

    if use_blur:
        image = cv2.GaussianBlur(image, (gaussian_blur_kernel_size, gaussian_blur_kernel_size), 0)

    if resize_image:
        image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

    return image


def easy_process(image):
    return pre_process_image(image, use_gray=False, use_canny=False, use_blur=False,  canny_low_threshold=550,
                             canny_high_threshold=150, gaussian_blur_kernel_size=1, resize_image=False,
                             crop_at_the_top=63, crop_at_the_bottom=28)
