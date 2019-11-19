import visbeat
import os
import subprocess
import json
import numpy as np
import visbeat

class DanceMusic:
    def __init__(self, target_video):
        self.target_video = target_video
        self.file_path = self.target_video.getPath()
        self.audio_path = None
        self.getMP3Audio(self.file_path)

    def getMP3Audio(self, file_path):
        current_dir = os.getcwd()
        os.chdir(os.path.dirname(file_path))
        os.chdir('../../')
        if not os.path.isdir('Audio'):
            os.mkdir('Audio')
        os.chdir('./Audio')
        audio_dir = os.getcwd()
        self.audio_path = audio_dir + "/Audio.mp3"
        os.chdir(current_dir)
        if not os.path.exists(self.audio_path):
            cmd = "ffmpeg -i '" + file_path + "' -ac 2 -ar 44100 -b:a 128K -f mp3 " + self.audio_path
            print cmd
            subprocess.call(cmd, shell=True)
        else:
            print 'Audio File is Exist.'

    def extractAudioBeatsData(self):
        plot_data = self.target_video.audio.plotBeats()
        beats_data = []
        for index, beat_data in enumerate(plot_data[1]._xy):
            if(index == 0):
                beat_datum = {'start_time': beat_data[0]}
            elif(index == len(plot_data[1]._xy) - 1):
                beats_data[index-1]['weight'] = beat_data[1]
                beats_data[index - 1]['end_time'] = beat_data[0]
                pass
            else:
                beats_data[index - 1]['end_time'] = beat_data[0]
                beats_data[index - 1]['weight'] = beat_data[1]
                beat_datum = {'start_time': beat_data[0]}
            beats_data.append(beat_datum)
        # beats_data = []
        # for index, beat_data in enumerate(plot_data[1]._xy):
        #     beat_datum = {
        #         'start_time': beat_data[0],
        #         'weight': beat_data[1]
        #     }
        #     beats_data.append(beat_datum)
        # for index, beat_data in enumerate(plot_data[1]._xy):
        #     if(index < len(plot_data[1]._xy) - 1):
        #         beats_data[index]['end_time'] = beats_data[index + 1]['start_time']
        #     else:
        #         beats_data[index]['end_time'] = beat_data[1]
        # for index, beat_data in enumerate(plot_data[1]._xy):
        #     if(index == 0):
        #         beat_datum = {
        #             'start_time': 0,
        #             'beat_time': beat_data[0],
        #             'weight': beat_data[1]
        #         }
        #     else:
        #         beat_datum = {
        #             'start_time': beats_data[index - 1]['beat_time'],
        #             'beat_time': beat_data[0],
        #             'weight': beat_data[1]
        #         }
        #     beats_data.append(beat_datum)
        i = self.getStartBeatTime()
        return beats_data[1:]

    def split_list(self, l, n):
        for idx in range(0, len(l), n):
            if len(l[idx: idx + n]) == n:
                yield l[idx: idx + n]
            else:
                pass
    
    def extractAudioBeatsData8BeatsAverage(self):
        splits_beats_data = self.split_list(self.extractAudioBeatsData(), 8)
        beats_average_data = []
        for i, split_beats_data in enumerate(splits_beats_data):
            weight_sum = reduce(lambda sum, beat_data: sum + beat_data['weight'], split_beats_data, 0)
            beats_average_datum = {
                'index': i,
                'start_time': split_beats_data[0]['start_time'],
                'end_time': split_beats_data[-1]['end_time'],
                'abeats': weight_sum/8}
            beats_average_data.append(beats_average_datum)
        return beats_average_data

    def min_max(self, x, axis = None):
        min = x.min(axis=axis, keepdims=True)
        max = x.max(axis=axis, keepdims=True)
        result = (x-min)/(max-min)
        return result

    def standardizationAudioBeats(self, beats_data):
        standardization_data = np.array([])
        for beat_data in beats_data:
            standardization_data = np.append(standardization_data, beat_data['abeats'])
        standardization_data = self.min_max(standardization_data)
        for idx, standardization_datum in enumerate(standardization_data):
            beats_data[idx]['abeats'] = standardization_datum
        return beats_data

    def getStartBeatTime(self):
        beats_data = self.target_video.audio.getBeatEvents()
        index = len(beats_data) % 4
        return index

    def dumpDictToJSON8BeatsAverage(self, file_path):
        beats_average_data = self.extractAudioBeatsData8BeatsAverage()
        beats_average_data_result = self.standardizationAudioBeats(beats_data = beats_average_data)
        result = {
            'beats_data': beats_average_data_result,
            'audio_path': self.audio_path
        }
        fw = open(file_path, 'w')
        json.dump(result, fw, indent=2)


    def test(self):
        self.getMP3Audio(self.file_path)

# SOURCE_VIDEO_URL = 'https://www.youtube.com/watch?v=8wYzN_O9XlU'
# test_video = visbeat.PullVideo(source_location = SOURCE_VIDEO_URL)
# results = test_video.audio.getBeatEvents()
# for result in results:
#     print result
# print len(results)