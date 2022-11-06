import cv2
import sys
import os

"""
2.手动标注视频
"""

path = f"../videos/122"
name = "BV17L4y1H7gc"
video1 = os.path.join(path, name+".mp4")
cap = cv2.VideoCapture(video1)
fps = cap.get(cv2.CAP_PROP_FPS)
size = (
    int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
)
fourcc = cv2.VideoWriter_fourcc("M", "P", "4", "2")
outVideo = cv2.VideoWriter("saveVideo.mp4", fourcc, fps, size)  # change fps here



retaining = True
frame_count = 0
clip = []

while retaining:
    retaining, frame = cap.read()
    frame_count += 1
    if not retaining and frame is None:
        continue

    cv2.imshow('result', frame)
    outVideo.write(frame)
    if cv2.waitKey(10) & 0xff == ord('q'):
        sys.exit()
    elif cv2.waitKey(10) & 0xff == ord('s'):
        print(frame_count)

cap.release()
outVideo.release()
cv2.destroyAllWindows()

print("number of frame is {}".format(frame_count))