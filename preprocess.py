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
first_chunk = resized_img[:, 0:100]

second_chunk = resized_img[:, 84:184]

third_chunk = resized_img[:, 168:268]




cv.imshow("Original", im)
cv.imshow("Resized Img", resized_img)
cv.imshow("First Chunk", first_chunk)
cv.imshow("Second Chunk", second_chunk)
cv.imshow("third_chunk ", third_chunk)





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