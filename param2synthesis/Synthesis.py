import json
import subprocess

def loadJSON(audio_json_path, visual_json_path):
    audio_json_data = json.load(open(audio_json_path, "r"))
    visaul_json_data = json.load(open(visual_json_path, "r"))
    return audio_json_data, visaul_json_data

audio_json_data, visaul_json_data = loadJSON(audio_json_path = 'AudioBeatsData8BeatsAverage.json', 
                                            visual_json_path = 'MHresult.json')

join_mov = str("")

for index, (audio_json_datum, visaul_json_datum) in enumerate(zip(audio_json_data['beats_data'], visaul_json_data['beats_data'])):
    frames = visaul_json_datum['frames']
    sec = audio_json_datum['end_time'] - audio_json_datum['start_time']
    cmd1 = "ffmpeg -start_number " + str(visaul_json_datum['start_number']) + " -i " + visaul_json_datum['file_path'] + " -vframes "
    cmd1 += str(frames) + " -vcodec libx264 -pix_fmt yuv420p -r " + str(frames/sec) + " ./Pro2DanceOutput/output_" + str(index) + ".mp4"
    cmd2 = "ffmpeg -i ./Pro2DanceOutput/output_" + str(index) + ".mp4 -vf fps=30 -vcodec libx264 -pix_fmt yuv420p ./Pro2DanceOutput/segment_" + str(index) + ".mp4"
    cmd3 = "echo file \\'/pro2dance/Pro2DanceOutput/segment_" + str(index) + ".mp4\\' >> MovieList.txt" 
    subprocess.call(cmd1, shell=True)
    subprocess.call(cmd2, shell=True)
    subprocess.call(cmd3, shell=True)

cmd4 = "ffmpeg -f concat -safe 0 -i MovieList.txt -c copy ./Pro2DanceOutput/output.mp4"
subprocess.call(cmd4, shell=True)
cmd5 = "ffmpeg -i ./Pro2DanceOutput/output.mp4 -i " + audio_json_data['audio_path'] + " -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 result.mp4"
subprocess.call(cmd5, shell=True)