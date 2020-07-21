# import the necessary packages
import numpy as np
import cv2


def find_max_area_index(contours):
    contour_areas = list(map(cv2.contourArea, contours))
    return contour_areas.index(max(contour_areas))


def straighten_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    # threshold the image, setting all foreground pixels to 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # flip data in threshold array
    thresh1 = thresh - 255
    np.where(thresh1 == -255, 0, thresh1)

    # find angle of inclination

    coords = np.column_stack(np.where(thresh1 > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    return rotated


def remove_margin(rotated):
    # crop image to remove black margin
    gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    # # Now find contours in it. There will be only one object, so find bounding rectangle for it.

    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    max_contour_index = find_max_area_index(contours)
    cnt = contours[max_contour_index]
    x, y, w, h = cv2.boundingRect(cnt)
    # # Now crop the image, and save it into another file.

    crop = rotated[y : y + h, x : x + w]
    return crop


def process_sat_image(source_path, dest_path):
    # load the image from disk
    image = cv2.imread(source_path)
    straightened_image = straighten_image(image)
    cropped_image = remove_margin(straightened_image)

    # write jpeg to destination
    cv2.imwrite(dest_path, cropped_image)
