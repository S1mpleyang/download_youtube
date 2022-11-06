## Pre-requisities: run 'pip install youtube-dl' to install the youtube-dl package.
## Specify your location of output videos and input json file.
import json
import os
import sys
import xlrd

"""
下载youtube视频需要加速器
"""


def download(label, id):
    output_path = './videos'
    label = label.replace(" ", "_")
    youtube_id = id

    if os.path.exists(os.path.join(output_path, label, youtube_id + ".mp4")):
        return 0
    else:
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        url = f"https://www.youtube.com/embed/{youtube_id}"
        vid_loc = output_path + '/' + label
        if not os.path.exists(vid_loc):
            os.mkdir(vid_loc)
        os.system('youtube-dl -o ' + vid_loc + '/' + youtube_id + '.mp4' + ' -f best ' + url)


##################################

workbook = xlrd.open_workbook(r'D:\DATASET\myaction\data_addition.xlsx')
sheet1 = workbook.sheets()[0]
# 数据总行数
nrows = sheet1.nrows

for i in range(1, nrows):
    info = sheet1.row_values(i)
    label, id, _, _, _ = info
    if label == "" or id == "":
        continue
    download(label, id)

# To save disk space, you could download the best format available
# 	but not better that 480p or any other qualities optinally
# See https://askubuntu.com/questions/486297/how-to-select-video-quality-from-youtube-dl
