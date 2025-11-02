import cv2 
import numpy as np

# Read image
img = cv2.imread("C:\\Users\\veathavalli\\Desktop\\Capture.PNG")

# Convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise and enhance edges
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Hough Circle Transform
circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=30,
                           param1=50, param2=30, minRadius=5, maxRadius=50)

# Draw detected circles and display coordinates
if circles is not None:
    circles = np.uint16(np.around(circles))
    for circle in circles[0, :]:
        center = (circle[0], circle[1])
        radius = circle[2]
        # Draw circle
        cv2.circle(img, center, radius, (0, 255, 0), 2)
        # Draw center
        cv2.circle(img, center, 2, (0, 0, 255), 3)
        # Print coordinates
        print("Center: {}, Radius: {}".format(center, radius))

# Display the image with detected circles
cv2.imshow("Detected Balls", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
