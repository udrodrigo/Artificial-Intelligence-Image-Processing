import random
import cv2
import numpy as np


def split(img, row, col):

    height, width, _ = img.shape
    h = height//row
    w = width//col

    parts = []
    for i in range(row):
        for j in range(col):
            parts.append(img[i*h:(i+1)*h,j*w:(j+1)*w,:])
    return parts


def shuffle(parts):
    random.shuffle(parts)
    for part in parts:
        if np.random.randint(100) < 50:
            part[:] = cv2.flip(part, 0)
            pass 
    return parts


def join_vertical(rgb_parts, n, k):
    parts = []
    for part in rgb_parts:
        parts.append(cv2.cvtColor(part, cv2.COLOR_BGR2GRAY))

    strips = []
    used = []
    for i in range(len(rgb_parts)):
        if i not in used:
            for z in range(k-1):
                max_orientation = -1
                max_coef = -99
                max_j = -1
                for j in range(i+1, len(rgb_parts)):
                    if j not in used:
                        coeffs = []
                        coeffs.append(np.corrcoef(parts[i][0][:], parts[j][0][:])[0][1])
                        coeffs.append(np.corrcoef(parts[i][0][:], parts[j][-1][:])[0][1])
                        coeffs.append(np.corrcoef(parts[i][-1][:], parts[j][0][:])[0][1])
                        coeffs.append(np.corrcoef(parts[i][-1][:], parts[j][-1][:])[0][1])

                        for x in range(len(coeffs)):
                            if coeffs[x] > max_coef:
                                max_j = j
                                max_coef = coeffs[x]
                                max_orientation = x
                used.append(max_j)
                if max_orientation == 0:
                    parts[i] = np.concatenate((cv2.flip(parts[i], 0), parts[max_j]))
                    rgb_parts[i] = np.concatenate((cv2.flip(rgb_parts[i], 0), rgb_parts[max_j]))
                elif max_orientation == 1:
                    parts[i] = np.concatenate((parts[max_j], parts[i]))
                    rgb_parts[i] = np.concatenate((rgb_parts[max_j], rgb_parts[i]))
                elif max_orientation == 2:
                    parts[i] = np.concatenate((parts[i], parts[max_j]))
                    rgb_parts[i] = np.concatenate((rgb_parts[i], rgb_parts[max_j]))
                elif max_orientation == 3:
                    parts[i] = np.concatenate((parts[i], cv2.flip(parts[max_j], 0)))
                    rgb_parts[i] = np.concatenate((rgb_parts[i], cv2.flip(rgb_parts[max_j], 0)))
            used.append(i)
            strips.append(rgb_parts[i])
    return strips


def join_horizontal(rgb_parts, n):
    parts = []
    for part in rgb_parts:
        parts.append(cv2.cvtColor(part, cv2.COLOR_BGR2GRAY))

    strips = []
    used = []
    for i in range(n-1):
        max_orientation = -1
        max_coef = -99
        max_j = -1
        for j in range(1, len(rgb_parts)):
            if j not in used:
                coeffs = []
                coeffs.append(np.corrcoef(parts[0][:,-1], parts[j][:, 0])[0][1])
                coeffs.append(np.corrcoef(parts[0][:, 0], parts[j][:, -1])[0][1])
                coeffs.append(np.corrcoef(parts[0][:, -1], parts[j][::-1, 0])[0][1])
                coeffs.append(np.corrcoef(parts[0][::-1, 0], parts[j][:, -1])[0][1])
                for x in range(len(coeffs)):
                    if coeffs[x] > max_coef:
                        max_j = j
                        max_coef = coeffs[x]
                        max_orientation = x
        used.append(max_j)
        if max_orientation == 0:
            parts[0] = np.concatenate((parts[0], parts[max_j]), axis=1)
            rgb_parts[0] = np.concatenate((rgb_parts[0], rgb_parts[max_j]), axis=1)
        elif max_orientation == 1:
            parts[0] = np.concatenate((parts[max_j], parts[0]), axis=1)
            rgb_parts[0] = np.concatenate((rgb_parts[max_j], rgb_parts[0]), axis=1)
        elif max_orientation == 2:
            parts[0] = np.concatenate((parts[0], cv2.flip(parts[max_j], 0)), axis=1)
            rgb_parts[0] = np.concatenate((rgb_parts[0], cv2.flip(rgb_parts[max_j], 0)), axis=1)
        elif max_orientation == 3:
            parts[0] = np.concatenate((parts[max_j], cv2.flip(parts[0], 0)), axis=1)
            rgb_parts[0] = np.concatenate((rgb_parts[max_j], cv2.flip(rgb_parts[0], 0)), axis=1)

    return rgb_parts[0]




# img = cv2.imread("image.png")
# row = 2
# col = 4

# parts = shuffle(split(img, row, col))
# strips = join_vertical(parts, row*col, row)
# res = join_horizontal(strips, col)

# cv2.imshow('image', res)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
