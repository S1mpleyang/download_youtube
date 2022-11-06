import json
import os

"""
1.下载视频
'youtube-dl 'https://www.bilibili.com/video/BV1hS4y1U7uk' -o 输出路径 -f (135|best)'
"""

output_path = '../videos'
json_path = 'bilibili.json'
if not os.path.exists(output_path):
    os.mkdir(output_path)

data = json.load(open(json_path, 'r'))['database']
youtube_ids = list(data.keys())

for youtube_id in data:
    info = data[youtube_id]
    type = info['recipe_type']
    url = info['video_url']
    vid_loc = output_path + '/' + str(type)
    if not os.path.exists(vid_loc):
        os.mkdir(vid_loc)
    # os.system("youtube-dl --list-formats "+url)
    save_name = vid_loc + '/' + youtube_id + '.mp4'
    if os.path.exists(save_name):
        continue
    os.system('youtube-dl -o ' + save_name + ' -f best ' + url)