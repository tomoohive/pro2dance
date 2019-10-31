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

    def deleteNonePoseData(self, json_data):
        tmp_json_data = json_data
        for idx, json_datum in enumerate(json_data['beats_data']):
            if json_datum['start_frame_pos'] == None or json_datum['end_frame_pos'] == None:
                del tmp_json_data['beats_data'][idx]
        return tmp_json_data

    def getDancePoseData(self):
        result_json = energy.calculateHumanPoseFrame(self.visual_beats)
        return self.deleteNonePoseData(result_json)
    
    def dumpDictToJSONDancePoseData(self, file_path):
        result = self.getDancePoseData()
        fw = open(file_path, 'w')
        json.dump(result, fw, indent=2)
