import numpy as np
import json

"""
もしこのfunctionを使うならば、jsonの中の配列を送っていただきたい(未来への自分へ)
"""
def loadJSON(audio_json_path, visual_json_path):
    audio_json_data = json.load(open(audio_json_path, "r"))
    visaul_json_data = json.load(open(visual_json_path, "r"))
    return audio_json_data, visaul_json_data

def calculatePoseSimiler(judgement_human_pos, target):
    d = 0
    for i in judgement_human_pos.keys() & target.keys():
        a = np.array(target[str(i)])
        b = np.array(judgement_human_pos[str(i)])
        d += np.linalg.norm(a-b)
    return d

def E_beat(X_audio, Y_video):
    variance_value = np.array([])
    for audio_beat, visual_beat in zip(X_audio, Y_video):
        variance_value = np.append(variance_value, audio_beat['abeats'] - visual_beat['vbeats'])
    mse = (np.square(variance_value)).mean()
    return mse

def E_pose(Y_video):
    variance_value = np.array([])
    for i in range(len(Y_video)):
        if(i == len(Y_video) - 1):
            continue
        else:
            result = calculatePoseSimiler(Y_video[i]['end_frame_pos'],Y_video[i+1]['start_frame_pos'])
            variance_value = np.append(variance_value, result)
    mse = (np.square(variance_value)).mean()
    return mse

def calculateEnergyFunction(X_audio, Y_video):
    a = E_beat(X_audio, Y_video)
    b = E_pose(Y_video)
    print(a,b)
    return a+20*b

# audio_beats, visual_beats = loadJSON('AudioBeatsData8BeatsAverage.json','OptimizedData.json')
# print(E_beat(audio_beats['beats_data'], visual_beats['beats_data']))
# print(E_pose(visual_beats['beats_data']))
# print(calculateEnergyFunction(audio_beats['beats_data'], visual_beats['beats_data']))