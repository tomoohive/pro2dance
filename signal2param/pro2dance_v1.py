import os, time
import numpy as np
import sys
import subprocess
import matplotlib
matplotlib.use('Agg')
import visbeat

SPLIT_DANCEFER_ASSETS = 'SplitDanceferAssets'
PRODANCE_ASSETS = './ProdanceAssets'
SOURCE_URL = 'https://www.youtube.com/watch?v=mgGqkDjdD8U'
TARGET_URL = 'https://www.youtube.com/watch?v=prPjpwsGiws'

class SourceMedia:
    def __init__(self, path, name=None, **kwargs):
        self.path = path
        self._name = name
        self.__dict__.update(**kwargs)
    @property
    def name(self):
        if(self._name is not None):
            return self._name
        else:
            return os.path.splitext(os.path.basename(self.path))[0]

def generateOriginalDancefer():
    source_url = SOURCE_URL
    target_url = TARGET_URL
    output_path = './OriginalDancefer.mp4'
    result = visbeat.AutoDancefer(source=source_url, target = target_url,
                                output_path = output_path,
                                synch_video_beat = 0,
                                synch_audio_beat = 0)
    cmd = "ffmpeg -i OriginalDancefer.mp4 -ac 2 -ar 44100 -b:a 128K -f mp3 ExtractAudio.mp3"
    subprocess.call(cmd, shell=True)
    return result

def adjustmentBeat(original_video):
    duration = original_video.getDuration()
    duration = int(duration / 8) * 8
    return duration

def generateSplitDancefers(duration):
    for material in range(duration/8):
        if material == 0:
            generateSplitDancefer(0,0,8)
        else:
            generateSplitDancefer(material, material * 8, 8)

def getSplitDanceferList(dir_name):
    fltr_list = [filename for filename in os.listdir(dir_name) if not filename.startswith('.')]
    return fltr_list


def generateSplitDancefer(material, beat_offset, nbeats):
    source_url = SOURCE_URL
    target_url = TARGET_URL
    output_path = './' + SPLIT_DANCEFER_ASSETS + '/SplitDancefer' + str(material) + '.mp4'
    result = visbeat.AutoDancefer(source=source_url, target = target_url,
                                output_path = output_path,
                                synch_video_beat = 0,
                                synch_audio_beat = 0,
                                beat_offset = beat_offset,
                                nbeats = nbeats)

def extractVisualBeatsAverage(file_name):
    visbeat.SetAssetsDir(PRODANCE_ASSETS)
    prodance_folder = os.path.join('.', SPLIT_DANCEFER_ASSETS)
    path_to_split_video = os.path.join(prodance_folder, file_name)
    split_dance = SourceMedia(path = path_to_split_video)
    visbeat.PullVideo(name = split_dance.name, source_location = split_dance.path)
    element = visbeat.LoadVideo(name = split_dance.name)
    beatsData = element.getVisualBeats()
    del beatsData[0]
    strengthSum = 0
    for beatData in beatsData:
        strengthSum += beatData.weight
    return strengthSum/8

# return type dic
def extractVisualBeatsAverages(splitDanceferList):
    dicBeats = {}
    for splitDancefer in splitDanceferList:
        strength = extractVisualBeatsAverage(splitDancefer)
        dicBeats[splitDancefer] = strength
    dicBeats = sorted(dicBeats.items(), key=lambda x: x[1])
    return dicBeats

def ExtractAudioBeatsTest(beats_result_len):
    target_url = TARGET_URL
    target_video = visbeat.PullVideo(source_location = target_url)
    result = target_video.audio.plotBeats()
    beat_results = result[1]._xy[0:beats_result_len]
    beat_result_tolist = beat_results.tolist()
    beat_splits = np.array_split(beat_result_tolist, len(beat_results)/8)
    beat_list = []
    for beat_split in beat_splits:
        strengthSum = 0
        if len(beat_split) > 7:
            for beat in beat_split:
                strengthSum += beat[1]
            beat_list.append(strengthSum/8)
        else:
            pass
    AudioBeatsList = np.array(beat_list)
    AudioBeatsList = AudioBeatsList.argsort()
    return AudioBeatsList



def main():
    original_video = generateOriginalDancefer()
    beats_result = original_video.audio.plotBeats()
    beats_result_len = len(beats_result[1]._xy)
    audioBeatsList = ExtractAudioBeatsTest(beats_result_len)
    duration = len(audioBeatsList) * 8
    generateSplitDancefers(duration)
    splitDanceferList = getSplitDanceferList('./SplitDanceferAssets')
    splitDanceferBeatList = extractVisualBeatsAverages(splitDanceferList)
    print audioBeatsList
    join_mov = str("")
    for audioBeat in audioBeatsList:
        print splitDanceferBeatList[audioBeat][0]    
        join_mov += " -i ./SplitDanceferAssets/"+ splitDanceferBeatList[audioBeat][0]
    cmd1 = "ffmpeg" + join_mov + " -strict -2 -filter_complex " + "\"concat=n="+str(len(audioBeatsList))+":v=1:a=1\" output.mp4"
    cmd2 = "ffmpeg -i output.mp4 -i ExtractAudio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 result.mp4"
    subprocess.call(cmd1, shell=True)
    subprocess.call(cmd2, shell=True)

if __name__ == '__main__':
    main()