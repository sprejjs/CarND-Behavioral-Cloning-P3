import matplotlib
matplotlib.use('TkAgg')

from tkinter import Tk, Label, Button, Scale, HORIZONTAL, Checkbutton, LEFT
from PIL import Image
from PIL.ImageTk import PhotoImage
from preprocess import pre_process_image, read_data
import matplotlib.image as mpimg

use_gray = False
use_canny = False
use_blur = False

crop_at_the_top = 0
crop_at_the_bottom = 0

canny_low_threshold = 0
canny_high_threshold = 0

gaussian_blur_kernel_size = 1

image_index = 0
X_train, y_train = read_data("driving_log.csv", return_images=False)


def print_configuration():
    print("Use grayscale: " + str(use_gray))
    print("Use canny: " + str(use_canny))
    print("use blur: " + str(use_blur))
    print("Crop at the top: " + str(crop_at_the_top))
    print("Crop at the bottom: " + str(crop_at_the_bottom))
    print("Canny low threshold: " + str(canny_low_threshold))
    print("Canny high threshold: " + str(canny_high_threshold))
    print("Gaussian blur kernel size: " + str(gaussian_blur_kernel_size))


def load_image(index):
    preprocessed_image = pre_process_image(mpimg.imread(X_train[index]),
                                           use_gray=use_gray,
                                           use_canny=use_canny,
                                           use_blur=use_blur,
                                           canny_low_threshold=canny_low_threshold,
                                           canny_high_threshold=canny_high_threshold,
                                           gaussian_blur_kernel_size=gaussian_blur_kernel_size,
                                           crop_at_the_top = crop_at_the_top,
                                           crop_at_the_bottom = crop_at_the_bottom)

    return Image.fromarray(preprocessed_image)


def change_image_index(val):
    global image_index
    image_index = int(val)
    reload_ui()


def change_crop_top(val):
    global crop_at_the_top
    crop_at_the_top = int(val)
    reload_ui()


def change_crop_bottom(val):
    global crop_at_the_bottom
    crop_at_the_bottom = int(val)
    reload_ui()


def change_canny_low_threshold(val):
    global canny_low_threshold
    canny_low_threshold = int(val)
    reload_ui()


def change_canny_high_threshold(val):
    global canny_high_threshold
    canny_high_threshold = int(val)
    reload_ui()


def change_gaussian_blur_kernel_size(val):
    global gaussian_blur_kernel_size

    n = int(val)

    if not n % 2:
        gaussian_blur_kernel_size = n + 1 if n > gaussian_blur_kernel_size else n - 1

    reload_ui()


def toggle_crop():
    global crop
    crop = not crop
    reload_ui()


def toggle_gray():
    global use_gray
    use_gray = not use_gray
    reload_ui()


def toggle_canny():
    global use_canny
    use_canny = not use_canny
    reload_ui()


def toggle_blur():
    global use_blur
    use_blur = not use_blur
    reload_ui()


def reload_ui():
    leftPhotoImage = PhotoImage(load_image(image_index + 1))
    centerPhotoIamge = PhotoImage(load_image(image_index))
    rightPhotoImage = PhotoImage(load_image(image_index + 2))

    window.leftImageView.configure(image=leftPhotoImage)
    window.leftImageView.image = leftPhotoImage

    window.centerImageView.configure(image=centerPhotoIamge)
    window.centerImageView.image = centerPhotoIamge

    window.rightImageView.configure(image=rightPhotoImage)
    window.rightImageView.image = rightPhotoImage

    window.cannyLowThreshold.set(canny_low_threshold)
    window.cannyHighThreshold.set(canny_high_threshold)
    window.gaussian_blur_kernel_size.set(gaussian_blur_kernel_size)

    window.leftCameraLabel.configure(text="Left Camera (" + str(y_train[image_index + 1]) + ")")
    window.centerCameraLabel.configure(text="Center Camera (" + str(y_train[image_index]) + ")")
    window.rightCameraLabel.configure(text="Right Camera (" + str(y_train[image_index + 2]) + ")")


def left_button_pressed(e):
    global image_index

    if (image_index > 0):
        image_index -= 3

    reload_ui()


def right_button_pressed(e):
    global image_index
    global image_paths

    if (image_index < len(X_train)):
        image_index += 3

    reload_ui()


window = Tk()

window.title("Pre-processing configuration")
window.configure(background='grey')

window.bind("<Left>", left_button_pressed)
window.bind("<Right>", right_button_pressed)

window.leftCameraLabel = Label(text="Left Camera (" + str(y_train[image_index + 1]) + ")")
window.leftCameraLabel.grid(row=0, column=0, sticky='we')

window.centerCameraLabel = Label(text="Center Camera (" + str(y_train[image_index]) + ")")
window.centerCameraLabel.grid(row=0, column=1, columnspan=2, sticky='we')

window.rightCameraLabel = Label(text="Right Camera (" + str(y_train[image_index + 2]) + ")")
window.rightCameraLabel.grid(row=0, column=3, sticky='we')

#Left Image
leftPhotoImage = PhotoImage(load_image(image_index + 2))
window.leftImageView = Label(window, image=leftPhotoImage)
window.leftImageView.grid(row=1, column=0)

#Center Image
centerPhotoIamge = PhotoImage(load_image(image_index + 1))
window.centerImageView = Label(window, image=centerPhotoIamge)
window.centerImageView.grid(row=1, column=1, columnspan=2)

#Right Image
rightPhotoImage = PhotoImage(load_image(image_index))
window.rightImageView = Label(window, image=rightPhotoImage)
window.rightImageView.grid(row=1, column=3)

Scale(window, from_=0, to=320, orient=HORIZONTAL, command=change_crop_top, label="Crop at the top").grid(row=2, column=0, columnspan=2, sticky='we')
Scale(window, from_=0, to=320, orient=HORIZONTAL, command=change_crop_bottom, label="Crop at the bottom").grid(row=2, column=2, columnspan=2, sticky='we')
Checkbutton(window, text="Use single color channel", command=toggle_gray, justify = LEFT).grid(row=4, columnspan=4, sticky='we')
Checkbutton(window, text="Use canny", command=toggle_canny, justify = LEFT).grid(row=5, columnspan=4, sticky='we')
window.cannyLowThreshold = Scale(window, from_=0, to=1500, orient=HORIZONTAL,
                                 command=change_canny_low_threshold, label="Low Canny Threshold")
window.cannyLowThreshold.grid(row=6, column=0, columnspan=2, sticky='we')

window.cannyHighThreshold = Scale(window, from_=0, to=1500, orient=HORIZONTAL,
                                  command=change_canny_high_threshold, label="High Canny Threshold")
window.cannyHighThreshold.grid(row=6, column=2, columnspan=2, sticky='we')

Checkbutton(window, text="Use blur", command=toggle_blur, justify=LEFT).grid(row=8, columnspan=4, sticky='we')
window.gaussian_blur_kernel_size = Scale(window, from_=1, to=49, orient=HORIZONTAL,
                                         command=change_gaussian_blur_kernel_size, label="Blur Kernel Size")
window.gaussian_blur_kernel_size.grid(row=9, columnspan=4, sticky='we')

Button(window, text="Print values", command=print_configuration).grid(row=10, columnspan=4, sticky='we')

Button(window, text="Close", command=quit).grid(row=11, columnspan=4, sticky='we')

window.mainloop()