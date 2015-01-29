import time
import sys
sys.path.append(r'X:\CODE\Reuseable')
inhalation = (
    (0.00,00000.00000),
    (0.12,18828.45188),
    (0.24,33891.21339),
    (0.36,40167.36402),
    (0.48,41422.59414),
    (0.60,38912.13389),
    (0.72,36401.67364),
    (0.84,33891.21339),
    (0.96,31380.75314),
    (1.08,25104.60251),
    (1.20,00000.00000),
    (2,0)
)
squareWave = (
    (0,5000),
    (1,5000),
    (1,45000),
    (2,45000)
)
curve = squareWave

assert curve[0][0]==0
    
def interpolate(index1,index2,givenTime):
    time1 = curve[index1][0]
    time2 = curve[index2][0]
    flow1 = curve[index1][1]
    flow2 = curve[index2][1]
    deltaTime = time2-time1
    deltaFlow = flow2-flow1
    fraction = ((givenTime-time1)/deltaTime)
    return flow1 + fraction*deltaFlow
    
def targetAt(time):
    timePostModulo = time%curve[-1][0]-curve[0][0]
    i = 0
    while curve[i][0] < timePostModulo:
        i += 1
    return interpolate(i-1,i,timePostModulo)

def followCurve():
    flowMeter.callMeRegularly()
    flowMeter.setFlow(targetAt(time.time()))

if __name__ == '__main__':
    import autoSetup
    import alicat
    flowMeter = autoSetup.setupA(alicat.alicatFlowController,loggingOn = True)
    startTime = time.time()
    while time.time() < startTime+3*(curve[-1][0]-curve[0][0]):
        followCurve()
    log = flowMeter.getLog()
    for reading in log:
        print('{}\t{}\t{}'.format(reading.time - log[0].time,targetAt(reading.time),reading.massFlow,reading.temperature,reading.pressure))
    flowMeter.setFlow(0)