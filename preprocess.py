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
resized_img = cv.resize(im,(target_height,new_width))

chunk_width = 100
overlap=16

step = chunk_width - overlap

chunks = []

for start_x in range(0,width, step):
    end_x = start_x + chunk_width

    chunk = resized_img[:, start_x:end_x]

    chunks.append(chunk)

    print(
        f"Chunk {len(chunks)}: "
        f"x={start_x} to {end_x}"
    )




# cv.imshow("Original", im)
# cv.imshow("Resized Img", resized_img)

cv.waitKey(0)
cv.destroyAllWindows()

