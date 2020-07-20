# import the necessary packages
import numpy as np
import cv2
# load the image from disk
image = cv2.imread("LC81410452019115-color-processed.jpeg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
# threshold the image, setting all foreground pixels to
# 255 and all background pixels to 0
thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

from matplotlib import pyplot as plt
img = plt.imshow(thresh)
plt.show()

# flip data in threshold array
thresh1 = thresh - 255
np.where(thresh1==-255, 0, thresh1) 


# find angle of inclination

coords = np.column_stack(np.where(thresh1 > 0))
angle = cv2.minAreaRect(coords)[-1]
# the `cv2.minAreaRect` function returns values in the
# range [-90, 0); as the rectangle rotates clockwise the
# returned angle trends to 0 -- in this special case we
# need to add 90 degrees to the angle
if angle < -45:
    angle = -(90 + angle)
# otherwise, just take the inverse of the angle to make
# it positive
else:
    angle = -angle

angle

# rotate the image to deskew it
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(image, M, (w, h),flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


img = plt.imshow(rotated)

plt.show()

cv2.imwrite('color_img.jpeg', rotated)


# crop image to remove black margin
gray = cv2.cvtColor(rotated,cv2.COLOR_BGR2GRAY)
_,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
# # Now find contours in it. There will be only one object, so find bounding rectangle for it.

contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))
cnt = contours[-2]
x,y,w,h = cv2.boundingRect(cnt)
# # Now crop the image, and save it into another file.

crop = rotated[y:y+h,x:x+w]
cv2.imwrite('cropped.jpeg',crop)
img = plt.imshow(crop)
plt.show()
