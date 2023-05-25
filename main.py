import time
import cv2

cap = cv2.VideoCapture('sample.mp4')
left_counter = 0
right_counter = 0

FLAG = None

tmp_x = tmp_y = count = 0
while True:
    ret, img = cap.read()

    if not ret: break

    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grey = cv2.GaussianBlur(grey, (21, 21), 0)
    ret, thresh = cv2.threshold(grey, 100, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours):
        c = max(contours, key=cv2.contourArea)
        x_coor, y_coor, width, height = cv2.boundingRect(c)
        count += 1
        tmp_x += x_coor
        tmp_y += y_coor
        if x_coor + width // 2 > 320:
            right_counter += 0 if FLAG else 1
            color = (255, 0, 0)
            FLAG = True
        else:
            left_counter += 1 if FLAG else 0
            color = (0, 0, 255)
            FLAG = False

        cv2.circle(img, (x_coor + width // 2, y_coor + height // 2), width // 2, color, 2)
        cv2.line(img, (0, y_coor + height // 2), (640, y_coor + height // 2), color, 1)
        cv2.line(img, (x_coor + width // 2, 0), (x_coor + width // 2, 480), color, 1)
        cv2.putText(img, "x: " + str(x_coor) + " y: " + str(y_coor) + " w: " + str(width) + " h: " + str(height),
                    (0, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0))
        cv2.putText(img, "left: " + str(left_counter) + " right: " + str(right_counter), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0))
        cv2.putText(img, "Distance: " + str(((x_coor + width // 2 - 320) ** 2 + (y_coor + height // 2 - 240) ** 2) ** 0.5),
                    (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0))
        cv2.putText(img, "Area percentage: " + str(100 * height * width / 640 / 480) + " %", (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0))

        cv2.rectangle(img, (220, 140), (420, 340), (0, 0, 0), 2)

    cv2.imshow('Pic', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.05)

print("x:", tmp_x / count, "y:", tmp_y / count)

cap.release()
cv2.destroyAllWindows()
