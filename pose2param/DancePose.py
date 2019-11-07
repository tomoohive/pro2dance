import sys
import json
sys.path.append('/pro2dance/tf-pose-estimation')
import energy

class DancePose:
    def __init__(self, json_path):
        self.visual_beats = self.loadVisualBeatsJSON(json_path)

    def loadVisualBeatsJSON(self, json_path):
        f = open(json_path, "r")
        json_data = json.load(f)
        return json_data

    def deleteNonePoseData(self, beats_data):
        for beat_data in beats_data[:]:
            if beat_data['start_frame_pos'] is None or beat_data['end_frame_pos'] is None:
                beats_data.remove(beat_data)
        return {'beats_data': beats_data}

    def getDancePoseData(self):
        result_json = energy.calculateHumanPoseFrame(self.visual_beats)
        return self.deleteNonePoseData(result_json['beats_data'])
    
    def dumpDictToJSONDancePoseData(self, file_path):
        result = self.getDancePoseData()
        fw = open(file_path, 'w')
        json.dump(result, fw, indent=2)
