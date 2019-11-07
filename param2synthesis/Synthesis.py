import json

def loadJSON(audio_json_path, visual_json_path):
    audio_json_data = json.load(open(audio_json_path, "r"))
    visaul_json_data = json.load(open(visual_json_path, "r"))
    return audio_json_data, visaul_json_data

audio_json_data, visaul_json_data = loadJSON(audio_json_path = 'AudioBeatsData8BeatsAverage.json', 
                                            visual_json_path = 'OptimizeData.json')

for audio_json_datum, visaul_json_datum in zip(audio_json_data, visaul_json_data):
    