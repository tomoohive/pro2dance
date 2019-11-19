from .EnergyFunction import calculateEnergyFunction
import numpy as np
import json
import copy
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

class MetropolisHastings:

    def __init__(self, audio_json_path, visual_json_path, video_json_path):
        self.audio_beats_data = self.loadJSON(json_path = audio_json_path)
        self.visual_beats_data = self.loadJSON(json_path = visual_json_path)
        self.video_data = self.loadJSON(json_path = video_json_path)

    def loadJSON(self, json_path):
        f = open(json_path, "r")
        json_data = json.load(f)
        return json_data

    def P(self, e_param):
        T = 0.25
        return np.exp(-e_param/T)

    def setVisualBeatsData(self, Y_video):
        result = {
            'beats_data': Y_video
        }
        self.visual_beats_data = result

    def dumpDictToJSONResult(self, file_path):
        fw = open(file_path, 'w')
        json.dump(self.visual_beats_data, fw, indent=2)

    def calculateMH(self, iteration):
        X_video = self.video_data['beats_data']
        X_audio = self.audio_beats_data['beats_data']
        Y_video = self.visual_beats_data['beats_data']
        beats_data_number = len(X_video)

        print('-------start-------')
        for iter in range(iteration):
            print('-------'+ str(iter) +' iteration-------')
            E0 = calculateEnergyFunction(X_audio, Y_video)
            P0 = self.P(e_param = E0)
            Y_video_dash = copy.deepcopy(Y_video)
            u = np.random.rand()
            i = np.random.randint(beats_data_number)
            v = np.random.randint(beats_data_number)
            j = np.random.randint(beats_data_number)
            print('Energy Function:' + str(E0))
            if u < 0.7:
                Y_video_dash[i] = X_video[v]
                print('1. exchange from X_video')
                print('Y_video_dash:' + str(i))
                print('X_video:' + str(j))
            else:
                Y_video_dash[i], Y_video_dash[j] = Y_video_dash[j], Y_video_dash[i]
                print('2. swap Y_video segments')
                print('Y_video_dash:' + str(i))
                print('Y_video_dash:' + str(j))
            E1 = calculateEnergyFunction(X_audio, Y_video_dash)
            P1 = self.P(e_param = E1)
            tmp = P1/P0
            if u <= min(tmp, 1):
                print('! Apply Y_video_dash Data !')
                Y_video = copy.deepcopy(Y_video_dash)
            
            print(u, tmp)
            plt.plot(iter, E0, marker='.')
    
        self.setVisualBeatsData(Y_video)
        self.dumpDictToJSONResult('MHresult.json')
        print('-------finish-------')
        plt.savefig('MHresult.png')
