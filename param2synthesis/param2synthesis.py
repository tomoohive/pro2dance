from .PreOptimizeData import preOptimizeVisualBeatsDanceData
from .MetropolisHastings import *

def main():
    preOptimizeVisualBeatsDanceData('AudioBeatsData8BeatsAverage.json','VisualBeatsAndDancePoseData8BeatsAverage.json')
    MH = MetropolisHastings('AudioBeatsData8BeatsAverage.json','OptimizedData.json','VisualBeatsAndDancePoseData8BeatsAverage.json')
    MH.calculateMH(10000)

if __name__ == '__main__':
    main()