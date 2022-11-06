
import cv2
import os
import sys

"""
3.分割视频
change label_segment1-9.txt to a readable data  --> txt2read
将长视频按照标签分割为120帧的短视频  --> get_segment_video
"""


def generate_TSN_dataset():
    """
    生成TSN需要的train_list
    一个txt文件，每行为[文件路径(str)， 视频帧数(int)， 动作类别(int)]
    """
    with open("mouse_labels.txt", 'r') as f:
        label = f.readlines()

    print(label)


def txt2read(txt_path):
    with open(txt_path) as f:
        data = f.readlines()

    cfg_ifo = data[0:3]
    data_ifo = data[4:]

    for i in range(len(data_ifo)):
        data_ifo[i] = data_ifo[i].split(",")[0:3]

    data_ifo = sorted(data_ifo, key=lambda x: int(x[0]))
    # with open("out9.txt", 'w') as f:
    #     for i in data_ifo:
    #         f.writelines(i[0]+" "+i[1]+" "+i[2]+"\n")

    return data_ifo


def get_segment_video_byframe():
    """
    对长视频进行一级分割，分割后每个视频长度120帧

    :param video:
    :return:
    """
    segfile = "seg-1"
    camera = "camera-1"
    video = f"../../e618_data_20220112/{segfile}-mouse-day1-{camera}.avi"
    data_info = txt2read(f"../../e618_data_20220112/label_{segfile}.txt")

    ## 创建目录
    os.makedirs(os.path.join(".", "video", "fall_down"), exist_ok=True)


    # 参数设置
    reader = cv2.VideoCapture(video)
    width = 320
    height = 240
    fps = reader.get(cv2.CAP_PROP_FPS)
    label_dict = {
        "fall_down": 0,
    }
    # 开始
    for i in range(len(data_info)):
        print("i:", i)
        each_clip = data_info[i]
        start, Duration, TrackName = int(each_clip[0]), int(each_clip[1]), each_clip[2]
        # 开始时间 帧， 持续时间 帧
        step = 120

        seg_start = start
        seg_end = seg_start + step
        end = start + Duration

        while seg_end < end:
            count_frame = 0

            # 输出设置
            label_dict[TrackName] += 1
            out_info = f"{segfile}-mouse-day1-{camera}" + "-" + TrackName + "-" + str(label_dict[TrackName])
            output = os.path.join("..", "mouse", "video", TrackName, out_info + ".avi")
            writer = cv2.VideoWriter(
                output,
                cv2.VideoWriter_fourcc("M", "P", "4", "2"),
                fps,
                (width, height),
            )

            while count_frame < seg_end - seg_start:
                have_more_frame, frame = reader.read()
                if have_more_frame == False:
                    sys.exit()

                frame = cv2.resize(frame, (width, height))
                writer.write(frame)
                count_frame += 1

            writer.release()
            print(out_info + ", success!")

            seg_start = seg_end
            seg_end = min(seg_end + step, end)

    reader.release()


def get_segment_video_byms():
    """
    对长视频进行一级分割，分割后每个视频长度60帧
    
    :param video:
    :return:
    """
    segfile = "seg-4"
    camera = "camera-1"
    video = f"../../e618_data_20220112/{segfile}-mouse-day1-{camera}.avi"
    data_info = txt2read(f"../../e618_data_20220112/label_{segfile}.txt")

    ## 创建目录
    os.makedirs(os.path.join("..", "mouse", "video", "locomotion"), exist_ok=True)
    os.makedirs(os.path.join("..", "mouse", "video", "rearing"), exist_ok=True)
    os.makedirs(os.path.join("..", "mouse", "video", "turning"), exist_ok=True)
    os.makedirs(os.path.join("..", "mouse", "video", "pause"), exist_ok=True)
    os.makedirs(os.path.join("..", "mouse", "video", "grooming"), exist_ok=True)

    # 参数设置
    reader = cv2.VideoCapture(video)
    width = 320
    height = 240
    fps = reader.get(cv2.CAP_PROP_FPS)
    label_dict = {
        "locomotion": 0,
        "rearing": 0,
        "turning": 0,
        "pause": 0,
        "grooming": 0,
    }
    # 开始
    for i in range(len(data_info)):
        print("i:",i)
        each_clip = data_info[i]
        start, Duration, TrackName = int(each_clip[0]), int(each_clip[1]), each_clip[2]
        # 开始时间 ms， 持续时间 ms
        step = 60

        seg_start = (start * 3)//100
        end = ((start + Duration) * 3) //100
        seg_end = min(seg_start + step, end)

        while seg_start!= seg_end:
            count_frame = 0

            # 输出设置
            label_dict[TrackName] += 1
            out_info = f"{segfile}-mouse-day1-{camera}" + "-" + TrackName + "-" + str(label_dict[TrackName])
            output = os.path.join("..", "mouse", "video", TrackName, out_info + ".avi")
            writer = cv2.VideoWriter(
                output,
                cv2.VideoWriter_fourcc("M", "P", "4", "2"),
                fps,
                (width, height),
            )

            while count_frame < seg_end - seg_start:
                have_more_frame, frame = reader.read()
                if have_more_frame == False:
                    sys.exit()

                frame = cv2.resize(frame, (width, height))
                writer.write(frame)
                count_frame += 1

            writer.release()
            print(out_info + ", success!")

            seg_start = seg_end
            seg_end = min(seg_end + step, end)

    reader.release()


def show_video():
    path = "../../e618_data_20220112/seg-1-mouse-day1-camera-1.avi"
    cap = cv2.VideoCapture(path)

    retaining = True
    while retaining:
        retaining, frame = cap.read()
        cv2.imshow('result', frame)
        if cv2.waitKey(50) & 0xff == ord('q'):
            sys.exit()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # show_video()
    get_segment_video_byframe()
    # generate_TSN_dataset()
    # txt2read(f"../../e618_data_20220112/label_seg-9.txt")
