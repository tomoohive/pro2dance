import visbeat
import os
import subprocess
import json

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
            subprocess.call(cmd, shell=True)
        else:
            print 'Audio File is Exist.'

    def extractAudioBeatsData(self):
        plot_data = self.target_video.audio.plotBeats()
        beats_data = []
        for index, beat_data in enumerate(plot_data[1]._xy):
            if(index == 0):
                beat_datum = {
                    'start_time': 0,
                    'beat_time': beat_data[0],
                    'weight': beat_data[1]
                }
            else:
                beat_datum = {
                    'start_time': beats_data[index - 1]['beat_time'],
                    'beat_time': beat_data[0],
                    'weight': beat_data[1]
                }
            beats_data.append(beat_datum)
        return beats_data

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
                'end_time': split_beats_data[-1]['beat_time'],
                'abeats': weight_sum/8}
            beats_average_data.append(beats_average_datum)
        return beats_average_data

    def dumpDictToJSON8BeatsAverage(self, file_path):
        beats_average_data = self.extractAudioBeatsData8BeatsAverage()
        result = {
            'beats_data': beats_average_data,
            'audio_path': self.audio_path
        }
        fw = open(file_path, 'w')
        json.dump(result, fw, indent=2)


    def test(self):
        self.getMP3Audio(self.file_path)