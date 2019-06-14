import cv2

# 入力画像のロード
img = cv2.imread('ChrSiro_Angry.jpg')

cv2.namedWindow('input')
cv2.imshow("input", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
