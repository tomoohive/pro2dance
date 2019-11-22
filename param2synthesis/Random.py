import numpy as np
import json

def loadJSON(audio_json_path, visual_json_path):
    audio_json_data = json.load(open(audio_json_path, "r"))
    visaul_json_data = json.load(open(visual_json_path, "r"))
    return audio_json_data, visaul_json_data

def randomVisualBeatsDanceData(audio_json_path, visual_json_path):
    audio_beats, visual_beats = loadJSON(audio_json_path, visual_json_path)
    visual_beats_index = len(visual_beats['beats_data'])
    visual_beat_list = []
    for audio_beat in audio_beats['beats_data']:
        visual_beat = visual_beats['beats_data'][np.random.randint(visual_beats_index)]
        visual_beat_list.append(visual_beat)
    result = {
        'beats_data': visual_beat_list
    }
    fw = open('RandomData.json', 'w')
    json.dump(result, fw, indent=2)

# def _optimize(audio_beat, visual_beats):
#     distances = np.array([_distance(p['vbeats'], audio_beat['abeats']) for p in visual_beats['beats_data']])
#     nearest_index = distances.argmin()
#     return visual_beats['beats_data'][nearest_index]

# def _distance(p0, p1):
#     return np.sqrt((p0 - p1) ** 2)