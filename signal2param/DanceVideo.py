import visbeat
import os
import subprocess
import json

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
            subprocess.call(cmd, shell=True)
        else:
            print 'png File is Exist.'   

    def getFrameNumber(self, f):
        if(f < 0):
            f = 0
        elif(f > (self.num_frames_total - 1)):
            f = self.num_frames_total - 1
        return int(f)

    def addFrameNumberToVisualBeatsData(self, beats_data):
        setattr(beats_data[0], 'start_frame', 1)
        for i in range(len(beats_data)):
            if(i == 0):
                end_frame = self.getFrameNumber(beats_data[i].start * self.sampling_rate)
                setattr(beats_data[i], 'end_frame', end_frame)
                setattr(beats_data[i+1], 'start_frame', end_frame + 1)
            elif(i == len(beats_data)-1):
                end_frame = self.getFrameNumber(beats_data[i].start * self.sampling_rate)
                setattr(beats_data[i], 'end_frame', end_frame)
            else:
                end_frame = self.getFrameNumber(beats_data[i].start * self.sampling_rate)
                setattr(beats_data[i], 'end_frame', end_frame)
                setattr(beats_data[i+1], 'start_frame', end_frame + 1)
        return beats_data

    def extractVisualBeatsData(self):
        beats_data = self.source_video.getVisualBeats()
        return self.addFrameNumberToVisualBeatsData(beats_data)

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
            weight_sum = reduce(lambda sum, beat_data: sum + beat_data.weight, split_beats_data, 0)
            beats_average_datum = {
                'index': i,
                'start_frame_file': "image_" + str(split_beats_data[0].start_frame) + ".png",
                'end_frame_file': "image_" + str(split_beats_data[-1].end_frame) + ".png",
                'vbeats': weight_sum/8}
            beats_average_data.append(beats_average_datum)
        return beats_average_data

    def dumpDictToJSON8BeatsAverage(self, file_path):
        beats_average_data = self.extractVisualBeatsData8BeatsAverage()
        result = {
            'beats_data': beats_average_data,
            'dir_path': self.png_dir + '/'
        }
        fw = open(file_path, 'w')
        json.dump(result, fw, indent=2)
        