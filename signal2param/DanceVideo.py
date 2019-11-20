import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import visbeat
import os
import subprocess
import json
import numpy as np
import pprint


class DanceVideo:
    def __init__(self, source_video):
        self.source_video = source_video
        self.sampling_rate = self.source_video.sampling_rate
        self.num_frames_total = self.source_video.num_frames_total
        self.file_path = self.source_video.getPath()
        self.png_dir = None
        self.splitFrameFromVideo(self.file_path)

    def splitFrameFromVideo(self, file_path):
        current_dir = os.getcwd()
        os.chdir(os.path.dirname(file_path))
        os.chdir('../../')
        if not os.path.isdir('Split'):
            os.mkdir('Split')
        os.chdir('./Split')
        split_dir = os.getcwd()
        self.png_dir = split_dir
        os.chdir(current_dir)
        if not os.path.exists(self.png_dir + "/image_1.png"):
            cmd = "ffmpeg -i '" + file_path + "' -vcodec png " + split_dir + "/image_%d.png"
            print cmd
            subprocess.call(cmd, shell=True)
        else:
            print 'png File is Exist.'   

    def getFrameNumber(self, f):
        if(f < 0):
            f = 0
        elif(f > (self.num_frames_total - 1)):
            f = self.num_frames_total - 1
        return int(f)

    def getNearestValue(self, time_list, num):
        idx = np.abs(np.asarray(time_list) - num).argmin()
        return idx
    
    def getTimeList(self, beats_data):
        time_list = []
        for beat_data in beats_data:
            time_list.append(beat_data.start)
        return time_list

    def addFrameNumberToVisualBeatsData(self, beats_data, audio_data):
        time_list = self.getTimeList(beats_data)
        for i in range(len(audio_data)):
            if(i == 0):
                start_frame = self.getFrameNumber(audio_data[i].start * self.sampling_rate)
                setattr(audio_data[i], 'start_frame', start_frame)
            elif(i == len(audio_data)-1):
                start_frame = self.getFrameNumber(audio_data[i].start * self.sampling_rate)
                setattr(audio_data[i], 'start_frame', start_frame)
                setattr(audio_data[i], 'end_frame', self.num_frames_total)
            else:
                start_frame = self.getFrameNumber(audio_data[i].start * self.sampling_rate)
                setattr(audio_data[i], 'start_frame', start_frame)
                setattr(audio_data[i-1], 'end_frame', start_frame - 1)
            weight = beats_data[self.getNearestValue(time_list, audio_data[i].start)].weight
            setattr(audio_data[i], 'weight', weight)
        return audio_data
        # setattr(beats_data[0], 'start_frame', 1)
        # for i in range(len(beats_data)):
        #     if(i == 0):
        #         end_frame = self.getFrameNumber(beats_data[i].start * self.sampling_rate)
        #         setattr(beats_data[i], 'end_frame', end_frame)
        #         setattr(beats_data[i+1], 'start_frame', end_frame + 1)
        #     elif(i == len(beats_data)-1):
        #         end_frame = self.getFrameNumber(beats_data[i].start * self.sampling_rate)
        #         setattr(beats_data[i], 'end_frame', end_frame)
        #     else:
        #         end_frame = self.getFrameNumber(beats_data[i].start * self.sampling_rate)
        #         setattr(beats_data[i], 'end_frame', end_frame)
        #         setattr(beats_data[i+1], 'start_frame', end_frame + 1)
        # return beats_data

    def extractVisualBeatsData(self):
        beats_data = self.source_video.getVisualBeats()
        audio_data = self.source_video.audio.getBeatEvents()
        return self.addFrameNumberToVisualBeatsData(beats_data, audio_data)

    def split_list(self, l, n):
        for idx in range(0, len(l), n):
            if len(l[idx: idx + n]) == n:
                yield l[idx: idx + n]
            else:
                pass
        
    def extractVisualBeatsData8BeatsAverage(self):
        splits_beats_data = self.split_list(self.extractVisualBeatsData(), 8)
        beats_average_data = []
        for i, split_beats_data in enumerate(splits_beats_data):
            weight_sum = reduce(lambda sum, beat_data: sum + abs(beat_data.weight), split_beats_data, 0)
            beats_average_datum = {
                'index': i,
                'frames': split_beats_data[-1].end_frame - split_beats_data[0].start_frame,
                'start_number': split_beats_data[0].start_frame,
                'file_path': self.png_dir + '/image_%d.png',
                'start_frame_file': self.png_dir + "/" + "image_" + str(split_beats_data[0].start_frame) + ".png",
                'end_frame_file': self.png_dir + "/" + "image_" + str(split_beats_data[-1].end_frame) + ".png",
                'vbeats': weight_sum/8}
            beats_average_data.append(beats_average_datum)
        return beats_average_data

    def min_max(self, x, axis = None):
        min = x.min(axis=axis, keepdims=True)
        max = x.max(axis=axis, keepdims=True)
        result = (x-min)/(max-min)
        return result

    def standardizationVisualBeats(self, beats_data):
        standardization_data = np.array([])
        for beat_data in beats_data:
            standardization_data = np.append(standardization_data, beat_data['vbeats'])
        standardization_data = self.min_max(standardization_data)
        for idx, standardization_datum in enumerate(standardization_data):
            beats_data[idx]['vbeats'] = standardization_datum
        return beats_data

    def dumpDictToJSON8BeatsAverage(self, file_path):
        beats_average_data = self.extractVisualBeatsData8BeatsAverage()
        beats_average_data_result = self.standardizationVisualBeats(beats_data = beats_average_data)
        result = {
            'beats_data': beats_average_data_result
        }
        fw = open(file_path, 'w')
        json.dump(result, fw, indent=2)

def getNearestValue(time_list, num):
    idx = np.abs(np.asarray(time_list) - num).argmin()
    return time_list[idx], idx

# SOURCE_VIDEO_URL = 'https://www.youtube.com/watch?v=ZfICRzbt-ZY'
# test_video = visbeat.PullVideo(source_location = SOURCE_VIDEO_URL)
# # a = test_video.getFeature('impact_envelope')
# # print(len(a))
# # print(test_video.sampling_rate)
# # for index, value in enumerate(a):
# #     plt.plot(index, value, marker='.')
# # plt.savefig('a.png')
# source_video = DanceVideo(test_video)
# results = source_video.extractVisualBeatsData()
# audio_beats = test_video.audio.getBeatEvents()
# time_list = []

# print test_video.getDuration()
# for result in results:
#     time_list.append(result.start)
#     print result.start
# for audio_beat in audio_beats:
#     print audio_beat.start, getNearestValue(time_list, audio_beat.start)

# print len(audio_beats), len(results)
