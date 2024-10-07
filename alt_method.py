import cv2

image = cv2.imread('image.bmp', cv2.IMREAD_GRAYSCALE)


def print_arr():
    for row in img_array:
        for element in row:
            print(element, end=' ')  # Print each element in the row with a space
        print()  # Move to the next row


if image is not None:
    height, width = image.shape[:2]
    img_array = [[0] * width for _ in range(height)]

    current_label = 0

    for row in range(height):
        for col in range(width):
            pixel_value = image[row, col]
            if row == 0:
                north_pixel_value = 0
                north_label = 0
            else:
                north_pixel_value = image[row - 1, col]
                north_label = img_array[row-1][col]
            if col == 0:
                west_pixel_value = 0
                west_label = 0
            else:
                west_pixel_value = image[row, col - 1]
                west_label = img_array[row][col-1]

            if pixel_value == west_pixel_value:
                img_array[row][col] = current_label


    print_arr()

else:
    print("No image found")
