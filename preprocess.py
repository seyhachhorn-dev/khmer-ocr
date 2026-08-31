import cv2 as cv

im = cv.imread('images/khmer-article.jpg')

if im is None:
    raise ValueError('can not load image')


# original size:
print("Shape:", im.shape)


# get two agrument first
height, width = im.shape[:2]

print("Height:", height)
print("Width:", width)

target_height = 48

scale = target_height / height

new_width = int(width*scale)
print("new width:", new_width)


# resize the original image

resized_img = cv.resize(im,(target_height,new_width))




cv.imshow("Original", im)
cv.imshow("Resized Img", resized_img)

cv.waitKey(0)
cv.destroyAllWindows()

