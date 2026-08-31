import cv2 as cv

im = cv.imread('images/khmer-text-line.png')

if im is None:
    raise ValueError('can not load image')


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

print(
        "start:",
        i,
        "end:",
        j,
        "shape:",
        chunk.shape
    )

cv.imshow("Original", im)
cv.imshow("Resized Img", resized_img)





cv.waitKey(0)
cv.destroyAllWindows()


# chunk_width = 100
# overlap=16

# step = chunk_width - overlap

# chunks = []

# for start_x in range(0,new_width, step):

#     end_x = start_x + chunk_width

#     chunk = resized_img[:, start_x:end_x]

#     chunks.append(chunk)