import argparse

from .DancePose import *

def main():
    parser = argparse.ArgumentParser(description='get tf-pose-estimation param')
    parser.add_argument('--json', type=str, default='./VisualBeatsData8BeatsAverage.json')
    parser.add_argument('--output', type=str, default='./VisualBeatsAndDancePoseData8BeatsAverage.json')
    args = parser.parse_args()

    dance_pose = DancePose(json_path = args.json)
    dance_pose.dumpDictToJSONDancePoseData(file_path = args.output)

if __name__ == '__main__':
    main()