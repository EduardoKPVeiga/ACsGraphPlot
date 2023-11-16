import serial
import matplotlib.pyplot as plt
import statistics as statcs
import os

ser = serial.Serial(
   port='COM3',
   baudrate=38400,
   parity=serial.PARITY_ODD,
   stopbits=serial.STOPBITS_TWO,
   bytesize=serial.EIGHTBITS
)

timeBuffer = []
timePHBuffer = []
dataText = []

acBuffer1 = []
acBuffer2 = []
acBuffer3 = []

rmsBuffer1 = []
rmsBuffer2 = []
rmsBuffer3 = []

fqBuffer1 = []
fqBuffer2 = []
fqBuffer3 = []

phBuffer2 = []
phBuffer3 = []

contImg = 0
contPHs = 0
contFQs = 0
contRMSs = 0
contImgPHs = 0
contImgFQs = 0
contImgRMSs = 0

defaultPhaseAC01 = 0
defaultPhaseAC02 = 24000
defaultPhaseAC03 = 11914
defaultFrequency = 6010
defaultRMS = 12800
defaultRMS3 = 13100

workingDirPath = os.path.dirname(os.path.abspath(__file__))

def plotACGraph():
    global workingDirPath

    global acBuffer1
    global acBuffer2
    global acBuffer3

    global contImg

    fig, axis = plt.subplots(3)
    fig.suptitle('ACs')

    # function to show the plot
    fig.set_size_inches(7.0, 5.0)
    plt.subplots_adjust(left=0.3)

    text = []

    # plotting the points
    axis[0].plot(timeBuffer, acBuffer1)
    axis[1].plot(timeBuffer, acBuffer2)
    axis[2].plot(timeBuffer, acBuffer3)

    axis[0].axhline(y = 0, color = 'r', linestyle = 'dashed')
    axis[1].axhline(y = 0, color = 'r', linestyle = 'dashed')
    axis[2].axhline(y = 0, color = 'r', linestyle = 'dashed')

    dataText.reverse()
    for j in range(len(dataText)):
        plt.figtext(0.05,0.00 + (3*j/100), dataText[j], fontsize=8, va="top", ha="left")

    ACFileName = "ACs\AC_"+ str(contImg) +".png"
    plt.savefig(os.path.join(workingDirPath, ACFileName), bbox_inches = "tight")
    contImg += 1

    #plt.draw()
    #plt.pause(10.0)
    #plt.close()

    acBuffer1.clear()
    acBuffer2.clear()
    acBuffer3.clear()
    dataText.clear()

def plotFQErrorGraph():
    
    global workingDirPath
    global contFQs
    global contImgFQs

    avgFQ01 = statcs.median(fqBuffer1)
    avgFQ02 = statcs.median(fqBuffer2)
    avgFQ03 = statcs.median(fqBuffer3)
    stdevFQ01 = statcs.stdev(fqBuffer1)
    stdevFQ02 = statcs.stdev(fqBuffer2)
    stdevFQ03 = statcs.stdev(fqBuffer3)

    figFQ, axisFQ = plt.subplots(3)
    figFQ.suptitle('FQs')

    figFQ.set_size_inches(7.0, 5.0)
    plt.subplots_adjust(left=0.3)
    plt.ylim([5500, 7000])
                    
    # plotting the points
    if len(timePHBuffer) == len(fqBuffer1):
        axisFQ[0].plot(timePHBuffer, fqBuffer1)
    else:
        timePHBuffer2 = timePHBuffer
        while len(timePHBuffer2) > len(fqBuffer1):
            timePHBuffer2.pop(len(timePHBuffer2) - 1)
        
        while len(timePHBuffer2) < len(fqBuffer1):
            timePHBuffer2.append(timePHBuffer2[len(timePHBuffer2) - 1] + 1)

        axisFQ[0].plot(timePHBuffer2, fqBuffer1)

    if len(timePHBuffer) == len(fqBuffer2):
        axisFQ[1].plot(timePHBuffer, fqBuffer2)
    else:
        timePHBuffer2 = timePHBuffer
        while len(timePHBuffer2) > len(fqBuffer2):
            timePHBuffer2.pop(len(timePHBuffer2) - 1)
        
        while len(timePHBuffer2) < len(fqBuffer2):
            timePHBuffer2.append(timePHBuffer2[len(timePHBuffer2) - 1] + 1)

        axisFQ[1].plot(timePHBuffer2, fqBuffer2)

    if len(timePHBuffer) == len(fqBuffer3):
        axisFQ[2].plot(timePHBuffer, fqBuffer3)
    else:
        timePHBuffer2 = timePHBuffer
        while len(timePHBuffer2) > len(fqBuffer3):
            timePHBuffer2.pop(len(timePHBuffer2) - 1)
        
        while len(timePHBuffer2) < len(fqBuffer3):
            timePHBuffer2.append(timePHBuffer2[len(timePHBuffer2) - 1] + 1)

        axisFQ[2].plot(timePHBuffer2, fqBuffer3)

    axisFQ[0].axhline(y = avgFQ01, color = 'r', linestyle = 'dashed')
    axisFQ[1].axhline(y = avgFQ02, color = 'r', linestyle = 'dashed')
    axisFQ[2].axhline(y = avgFQ03, color = 'r', linestyle = 'dashed')

    axisFQ[0].axhline(y = defaultFrequency, color = 'g', linestyle = 'dashed')
    axisFQ[1].axhline(y = defaultFrequency, color = 'g', linestyle = 'dashed')
    axisFQ[2].axhline(y = defaultFrequency, color = 'g', linestyle = 'dashed')

    stdevFQ01String = "Desvio padrão FQ02: " + str(round(stdevFQ01, 2))
    stdevFQ02String = "Desvio padrão FQ02: " + str(round(stdevFQ02, 2))
    stdevFQ03String = "Desvio padrão FQ03: " + str(round(stdevFQ03, 2))

    erro1 = (avgFQ01 * 100) / defaultFrequency
    erro2 = (avgFQ02 * 100) / defaultFrequency
    erro3 = (avgFQ03 * 100) / defaultFrequency

    erro1 = abs(100 - erro1)
    erro2 = abs(100 - erro2)
    erro3 = abs(100 - erro3)

    erro1 += (stdevFQ01 * 100) / defaultFrequency
    erro2 += (stdevFQ02 * 100) / defaultFrequency
    erro3 += (stdevFQ03 * 100) / defaultFrequency

    erroFQ01 = "Erro FQ01: " + str(round(erro1, 2)) + "%"
    erroFQ02 = "Erro FQ02: " + str(round(erro2, 2)) + "%"
    erroFQ03 = "Erro FQ03: " + str(round(erro3, 2)) + "%"

    plt.figtext(0.05,0.25, erroFQ01, fontsize=8, va="top", ha="left")
    plt.figtext(0.05,0.20, erroFQ02, fontsize=8, va="top", ha="left")
    plt.figtext(0.05,0.15, erroFQ03, fontsize=8, va="top", ha="left")
    plt.figtext(0.05,0.10, stdevFQ01String, fontsize=8, va="top", ha="left")
    plt.figtext(0.05,0.05, stdevFQ02String, fontsize=8, va="top", ha="left")
    plt.figtext(0.05,0.00, stdevFQ03String, fontsize=8, va="top", ha="left")

    FQFileName = "FQs\FQ_"+ str(contImgFQs) +".png"
    plt.savefig(os.path.join(workingDirPath, FQFileName), bbox_inches = "tight")
    contImgFQs += 1

    fqBuffer1.clear()
    fqBuffer2.clear()
    fqBuffer3.clear()
    contFQs = 0

def plotPHErrorGraph():
    global timePHBuffer
    global phBuffer2
    global phBuffer3
    global contPHs
    global workingDirPath
    global contImgPHs

    avgPH02 = statcs.median(phBuffer2)
    avgPH03 = statcs.median(phBuffer3)
    stdevPH02 = statcs.stdev(phBuffer2)
    stdevPH03 = statcs.stdev(phBuffer3)

    figPH, axisPH = plt.subplots(2)
    figPH.suptitle('PHs')

    figPH.set_size_inches(7.0, 5.0)
    plt.subplots_adjust(left=0.3)
    plt.ylim([9000, 27000])
        
    # plotting the points
    if len(timePHBuffer) == len(phBuffer2):
        axisPH[0].plot(timePHBuffer, phBuffer2)
    else:
        timePHBuffer2 = timePHBuffer
        while len(timePHBuffer2) > len(phBuffer2):
            timePHBuffer2.pop(len(timePHBuffer2) - 1)
        
        while len(timePHBuffer2) < len(phBuffer2):
            timePHBuffer2.append(timePHBuffer2[len(timePHBuffer2) - 1] + 1)

        axisPH[0].plot(timePHBuffer2, phBuffer2)
    
    if len(timePHBuffer) == len(phBuffer3):
        axisPH[1].plot(timePHBuffer, phBuffer3)
    else:
        timePHBuffer2 = timePHBuffer
        while len(timePHBuffer2) > len(phBuffer3):
            timePHBuffer2.pop(len(timePHBuffer2) - 1)
        
        while len(timePHBuffer2) < len(phBuffer3):
            timePHBuffer2.append(timePHBuffer2[len(timePHBuffer2) - 1] + 1)

        axisPH[1].plot(timePHBuffer2, phBuffer3)

    axisPH[0].axhline(y = avgPH02, color = 'r', linestyle = 'dashed')
    axisPH[1].axhline(y = avgPH03, color = 'r', linestyle = 'dashed')

    axisPH[0].axhline(y = defaultPhaseAC02, color = 'g', linestyle = 'dashed')
    axisPH[1].axhline(y = defaultPhaseAC03, color = 'g', linestyle = 'dashed')

    stdevPH02String = "Desvio padrão PH02: " + str(round(stdevPH02, 2))
    stdevPH03String = "Desvio padrão PH03: " + str(round(stdevPH03, 2))

    erro2 = (avgPH02 * 100) / defaultPhaseAC02
    erro3 = (avgPH03 * 100) / defaultPhaseAC03

    erro2 = abs(100 - erro2)
    erro3 = abs(100 - erro3)

    erro2 += (stdevPH02 * 100) / defaultPhaseAC02
    erro3 += (stdevPH03 * 100) / defaultPhaseAC03

    erroPH02 = "Erro PH02: " + str(round(erro2, 2)) + "%"
    erroPH03 = "Erro PH03: " + str(round(erro3, 2)) + "%"

    plt.figtext(0.05,0.15, erroPH02, fontsize=8, va="top", ha="left")
    plt.figtext(0.05,0.10, erroPH03, fontsize=8, va="top", ha="left")
    plt.figtext(0.05,0.05, stdevPH02String, fontsize=8, va="top", ha="left")
    plt.figtext(0.05,0.00, stdevPH03String, fontsize=8, va="top", ha="left")

    PHFileName = "PHs\PH_"+ str(contImgPHs) +".png"
    plt.savefig(os.path.join(workingDirPath, PHFileName), bbox_inches = "tight")
    contImgPHs += 1

    phBuffer2.clear()
    phBuffer3.clear()
    contPHs = 0

def plotRMSErrorGraph():
    global timePHBuffer
    global rmsBuffer1
    global rmsBuffer2
    global rmsBuffer3
    global contRMSs
    global workingDirPath
    global contImgRMSs

    avgRMS01 = statcs.median(rmsBuffer1)
    avgRMS02 = statcs.median(rmsBuffer2)
    avgRMS03 = statcs.median(rmsBuffer3)
    stdevRMS01 = statcs.stdev(rmsBuffer1)
    stdevRMS02 = statcs.stdev(rmsBuffer2)
    stdevRMS03 = statcs.stdev(rmsBuffer3)
    
    figRMS, axisRMS = plt.subplots(3)
    figRMS.suptitle('RMSs')

    figRMS.set_size_inches(7.0, 5.0)
    plt.subplots_adjust(left=0.3)
    plt.ylim([10000, 13500])
        
    # plotting the points
    if len(timePHBuffer) == len(rmsBuffer1):
        axisRMS[0].plot(timePHBuffer, rmsBuffer1)
    else:
        timePHBuffer2 = timePHBuffer
        while len(timePHBuffer2) > len(rmsBuffer1):
            timePHBuffer2.pop(len(timePHBuffer2) - 1)
        
        while len(timePHBuffer2) < len(rmsBuffer1):
            timePHBuffer2.append(timePHBuffer2[len(timePHBuffer2) - 1] + 1)

        axisRMS[0].plot(timePHBuffer2, rmsBuffer1)

    if len(timePHBuffer) == len(rmsBuffer2):
        axisRMS[1].plot(timePHBuffer, rmsBuffer2)
    else:
        timePHBuffer2 = timePHBuffer
        while len(timePHBuffer2) > len(rmsBuffer2):
            timePHBuffer2.pop(len(timePHBuffer2) - 1)
        
        while len(timePHBuffer2) < len(rmsBuffer2):
            timePHBuffer2.append(timePHBuffer2[len(timePHBuffer2) - 1] + 1)

        axisRMS[1].plot(timePHBuffer2, rmsBuffer2)

    if len(timePHBuffer) == len(rmsBuffer3):
        axisRMS[2].plot(timePHBuffer, rmsBuffer3)
    else:
        timePHBuffer2 = timePHBuffer
        while len(timePHBuffer2) > len(rmsBuffer3):
            timePHBuffer2.pop(len(timePHBuffer2) - 1)
        
        while len(timePHBuffer2) < len(rmsBuffer3):
            timePHBuffer2.append(timePHBuffer2[len(timePHBuffer2) - 1] + 1)

        axisRMS[2].plot(timePHBuffer2, rmsBuffer3)

    axisRMS[0].axhline(y = avgRMS01, color = 'r', linestyle = 'dashed')
    axisRMS[1].axhline(y = avgRMS02, color = 'r', linestyle = 'dashed')
    axisRMS[2].axhline(y = avgRMS03, color = 'r', linestyle = 'dashed')

    axisRMS[0].axhline(y = defaultRMS, color = 'g', linestyle = 'dashed')
    axisRMS[1].axhline(y = defaultRMS, color = 'g', linestyle = 'dashed')
    axisRMS[2].axhline(y = defaultRMS, color = 'g', linestyle = 'dashed')

    stdevRMS01String = "Desvio padrão RMS02: " + str(round(stdevRMS01, 2))
    stdevRMS02String = "Desvio padrão RMS02: " + str(round(stdevRMS02, 2))
    stdevRMS03String = "Desvio padrão RMS03: " + str(round(stdevRMS03, 2))

    erro1 = (avgRMS01 * 100) / defaultRMS
    erro2 = (avgRMS02 * 100) / defaultRMS
    erro3 = (avgRMS03 * 100) / defaultRMS3

    erro1 = abs(100 - erro1)
    erro2 = abs(100 - erro2)
    erro3 = abs(100 - erro3)

    erro1 += (stdevRMS01 * 100) / defaultRMS
    erro2 += (stdevRMS02 * 100) / defaultRMS
    erro3 += (stdevRMS03 * 100) / defaultRMS3

    erroRMS01 = "Erro RMS01: " + str(round(erro1, 2)) + "%"
    erroRMS02 = "Erro RMS02: " + str(round(erro2, 2)) + "%"
    erroRMS03 = "Erro RMS03: " + str(round(erro3, 2)) + "%"

    plt.figtext(0.05,0.25, erroRMS01, fontsize=8, va="top", ha="left")
    plt.figtext(0.05,0.20, erroRMS02, fontsize=8, va="top", ha="left")
    plt.figtext(0.05,0.15, erroRMS03, fontsize=8, va="top", ha="left")
    plt.figtext(0.05,0.10, stdevRMS01String, fontsize=8, va="top", ha="left")
    plt.figtext(0.05,0.05, stdevRMS02String, fontsize=8, va="top", ha="left")
    plt.figtext(0.05,0.00, stdevRMS03String, fontsize=8, va="top", ha="left")

    RMSFileName = "RMSs\RMS_"+ str(contImgRMSs) +".png"
    plt.savefig(os.path.join(workingDirPath, RMSFileName), bbox_inches = "tight")
    contImgRMSs += 1

    rmsBuffer1.clear()
    rmsBuffer2.clear()
    rmsBuffer3.clear()
    contRMSs = 0

def main():
    global timeBuffer
    global timePHBuffer
    global dataText

    global acBuffer1
    global acBuffer2
    global acBuffer3

    global rmsBuffer1
    global rmsBuffer2
    global rmsBuffer3

    global fqBuffer1
    global fqBuffer2
    global fqBuffer3

    global phBuffer2
    global phBuffer3

    global contPHs
    global contFQs
    global contRMSs

    isAC01 = True
    isAC02 = False
    isPrint = False
    
    PHSample = 30
    FQSample = 30
    RMSSample = 30

    isPH02 = False
    isPH03 = False

    global axis

    for i in range(160):
        timeBuffer.append(i)
    for i in range(PHSample):
        timePHBuffer.append(i)
        
    while True:
        sInput = ser.readline().strip()

        try:
            sInputDecoded = sInput.decode("utf-8")
            if sInputDecoded == "$":
                isPrint = False
                while len(acBuffer3) < 160:
                    value = ser.readline().strip()

                    if isAC01:
                        acBuffer1.append(int(value))
                        isAC01 = False
                        isAC02 = True
                    else:
                        if isAC02:
                            acBuffer2.append(int(value))
                            isAC02 = False
                        else:
                            acBuffer3.append(int(value))
                            isAC01 = True
                
                avg1 = 0
                avg2 = 0
                avg3 = 0
                for k in range(160):
                    avg1 += acBuffer1[k]
                    avg2 += acBuffer2[k]
                    avg3 += acBuffer3[k]
                
                avg1 = avg1 / 160
                avg2 = avg2 / 160
                avg3 = avg3 / 160

                for l in range(160):
                    acBuffer1[l] -= avg1
                    acBuffer2[l] -= avg2
                    acBuffer3[l] -= avg3

            elif sInputDecoded == "%":
                isPrint = True

            if isPrint:
                if sInputDecoded != "%":
                    dataText.append(sInputDecoded)
                    if sInputDecoded == "AC01":
                        isPH02 = False
                        isPH03 = False
                    elif sInputDecoded == "AC02":
                        isPH02 = True
                        isPH03 = False
                    elif sInputDecoded == "AC03":
                        isPH02 = False
                        isPH03 = True

                    phase = 0
                    if sInputDecoded.find('ph_i') >= 0:
                        if isPH02:
                            phase = int(sInputDecoded[sInputDecoded.find(':') + 2:len(sInputDecoded)])
                            phBuffer2.append(phase)
                        elif isPH03:
                            phase = int(sInputDecoded[sInputDecoded.find(':') + 2:len(sInputDecoded)])
                            phBuffer3.append(phase)
                            contPHs += 1

                    frequency = 0
                    if sInputDecoded.find('f_i') >= 0:
                        if isPH02 == False and isPH03 == False:
                            frequency = int(sInputDecoded[sInputDecoded.find(':') + 2:len(sInputDecoded)])
                            fqBuffer1.append(frequency)
                        elif isPH02:
                            frequency = int(sInputDecoded[sInputDecoded.find(':') + 2:len(sInputDecoded)])
                            fqBuffer2.append(frequency)
                        elif isPH03:
                            frequency = int(sInputDecoded[sInputDecoded.find(':') + 2:len(sInputDecoded)])
                            fqBuffer3.append(frequency)
                            contFQs += 1

                    rms = 0
                    if sInputDecoded.find('rms_i') >= 0:
                        if isPH02 == False and isPH03 == False:
                            rms = int(sInputDecoded[sInputDecoded.find(':') + 2:len(sInputDecoded)])
                            rmsBuffer1.append(rms)
                        elif isPH02:
                            rms = int(sInputDecoded[sInputDecoded.find(':') + 2:len(sInputDecoded)])
                            rmsBuffer2.append(rms)
                        elif isPH03:
                            rms = int(sInputDecoded[sInputDecoded.find(':') + 2:len(sInputDecoded)])
                            rmsBuffer3.append(rms)
                            contRMSs += 1

            if len(acBuffer1) >= 160:
                plotACGraph()

            if contRMSs >= RMSSample:
                plotRMSErrorGraph()

            if contPHs >= PHSample:
                plotPHErrorGraph()

            if contFQs >= FQSample:
                plotFQErrorGraph()

        except UnicodeDecodeError:
            print("Invalid CHAR")


if __name__ == "__main__":
    main()
