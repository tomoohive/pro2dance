import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import visbeat
import os
import subprocess
import json
import numpy as np
import pprint

class DanceVideos:
    """
    dance_videos = list[DanceVideo...]
    """
    def __init__(self, dance_videos):
        self.dance_videos = dance_videos

    def makeDatabaseExtract8BeatsAverage(self):
        database = []
        for dance_video in self.dance_videos:
            dance_video_result = dance_video.extractVisualBeatsData8BeatsAverage()
            database.extend(dance_video_result)
        return database

    def dumpDictToJSON8BeatsAverageDatabase(self, file_path):
        beats_average_database = self.makeDatabaseExtract8BeatsAverage()
        result = {
            'beats_data': beats_average_database
        }
        fw = open(file_path, 'w')
        json.dump(result, fw, indent=2)