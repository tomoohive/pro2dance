import os, time
import numpy as np
import sys
import subprocess
import matplotlib
matplotlib.use('Agg')
import visbeat
from DanceVideo import *
from DanceMusic import *

# SOURCE_VIDEO_URL = 'https://www.youtube.com/watch?v=kS_DvUlrukk'
SOURCE_VIDEO_URL = 'https://www.youtube.com/watch?v=ZfICRzbt-ZY'
# SOURCE_VIDEO_URL = 'https://www.youtube.com/watch?v=zWvShbUpYHY'
# TARGET_VIDEO_URL = 'https://www.youtube.com/watch?v=prPjpwsGiws'
# TARGET_VIDEO_URL = 'https://www.youtube.com/watch?v=VdXZaGGWe3Y'
# TARGET_VIDEO_URL = 'https://www.youtube.com/watch?v=ZbZSe6N_BXs'
# TARGET_VIDEO_URL = 'https://www.youtube.com/watch?v=8wYzN_O9XlU'
TARGET_VIDEO_URL = 'https://www.youtube.com/watch?v=_NNYI8VbFyY'

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

def main():
    source_video = DanceVideo(visbeat.PullVideo(source_location = SOURCE_VIDEO_URL))
    source_video.dumpDictToJSON8BeatsAverage('VisualBeatsData8BeatsAverage.json')
    target_video = DanceMusic(visbeat.PullVideo(source_location = TARGET_VIDEO_URL))
    target_video.dumpDictToJSON8BeatsAverage('AudioBeatsData8BeatsAverage.json')

if __name__ == '__main__':
    main()