import cv2 as cv
import torch


im = cv.imread('images/khmer-text-line.png')

if im is None:
    raise ValueError('can not load image')

gray = cv.cvtColor(im,(0,255,128))

cv.imshow("gray",gray)


# original size:
print("Shape:", im.shape)


# get two agrument first
height, width = im.shape[:2]

print("Height:", height)
print("Width:", width)


# default hieght for khmer text
target_height = 48

scale = target_height / height

new_width = int(width*scale)

print("new width:", new_width)


# resize the original image
resized_img = cv.resize(im,(new_width,target_height))

# cut from 0 to 100 keep same height
# first_chunk = resized_img[:, 0:100]


chunk_width = 100
overlap = 16
# share region overlap to make second chunk know the first chunk info be 
# be able to predict
step_share_region = chunk_width - overlap

# start from 0 to 100 and keep plus 16 every step to keep share region
# i = start x axis & j = end x axis

for i in range(0,new_width,step_share_region):
    j = i + chunk_width
    chunk = resized_img[:,i:j]

    if chunk.shape[1] < chunk_width:
        padding = chunk_width - chunk.shape[1]

        chunk = cv.copyMakeBorder(
            chunk,
            0,
            0,
            0,
            padding,
            cv.BORDER_CONSTANT,
            value=(255,255,255)
        )

# print(
#         "start:",
#         i,
#         "end:",
#         j,
#         "shape:",
#         chunk.shape
#     )


tensor = torch.from_numpy(chunk)
print("Before:", tensor.shape)

# Change HWC → CHW
tensor = tensor.permute(2, 0, 1)
print("After permute:", tensor.shape)

tensor = tensor.float() / 255.0
print("Min:", tensor.min())
print("Max:", tensor.max())

tensor = tensor.unsqueeze(0)
print('unsqueeze',tensor.shape)

cv.imshow("Original", im)
cv.imshow("Resized Img", resized_img)





cv.waitKey(0)
cv.destroyAllWindows()

