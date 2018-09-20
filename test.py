import time
import cv2

img = cv2.imread("OASIS/0/0_I1.jpg")
cv2.namedWindow("a", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("a",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
cv2.imshow("a", img)
cv2.waitKey(100)
print("Ok")
time.sleep(2)
img = cv2.imread("OASIS/0/0_I197.jpg")
cv2.imshow("a", img)
cv2.waitKey(100)
print("Ok")
time.sleep(2)
cv2.destroyAllWindows()
