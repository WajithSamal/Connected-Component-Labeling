import cv2
import numpy as np
from PIL import Image, ImageOps
import random
import numpy

labels = []
label_conv = {}


def get_binary_image(img_array, threshold=150):
    for i in range(len(img_array)):
        for j in range(len(img_array[0])):
            if img_array[i][j] > threshold:
                img_array[i][j] = 1
            else:
                img_array[i][j] = 0
    return img_array


def get_colored_image(img):
    row, column = img.shape

    label_color = {0: (0, 0, 0)}
    coloured_image = np.zeros((row, column, 3), int)

    for i in range(row):
        for j in range(column):
            label = img[i, j]
            if label not in label_color:
                label_color[label] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            coloured_image[i, j, :] = label_color[label]

    return coloured_image


def decide_label(pixels):
    if all(i == 0 for i in pixels):
        if len(labels) == 0:
            labels.append(1)
            return max(labels)
        else:
            labels.append(max(labels) + 1)
            return max(labels)
    else:
        pixels = [i for i in pixels if i != 0]
        pixels.sort()

        minimum_value = pixels[0]
        maximum_value = pixels[len(pixels) - 1]

        if maximum_value == minimum_value:
            return minimum_value
        else:
            label_conv[maximum_value] = minimum_value
            return minimum_value


def two_pass(img):
    row, column = img.shape

    for i in range(row):
        for j in range(column):

            if img[i, j] == 1:

                if i == 0 and j == 0:
                    img[i, j] = decide_label([])

                elif i == 0 and j > 0:
                    img[i, j] = decide_label([img[i, j - 1]])

                else:
                    img[i, j] = decide_label([img[i - 1, j], img[i, j - 1]])

    for index in range(len(label_conv)):
        for i in range(row):
            for j in range(column):
                if img[i][j] in label_conv:
                    img[i][j] = label_conv[img[i][j]]

    return img


def main():
    image = Image.open("image.bmp")
    original = image

    image = image.convert('L')

    image = ImageOps.expand(image, border=1, fill='black')

    image = numpy.array(image)

    image = get_binary_image(image)

    passed_image = two_pass(image)
    coloured_image = get_colored_image(passed_image).astype(np.uint8)

    cv2.imshow("Output Image", coloured_image)

    cv2.imwrite("result.jpg", coloured_image)

    cv2.waitKey()


if __name__ == "__main__":
    main()
