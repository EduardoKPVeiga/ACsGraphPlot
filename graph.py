import serial
import matplotlib.pyplot as plt
from dash import Dash, html, dcc, Input, Output
import pandas as pd

ser = serial.Serial(
   port='COM3',
   baudrate=38400,
   parity=serial.PARITY_ODD,
   stopbits=serial.STOPBITS_TWO,
   bytesize=serial.EIGHTBITS
)

def main():
    timeBuffer = []
    acBuffer1 = []
    acBuffer2 = []
    acBuffer3 = []
    dataText = []
    isAC01 = True
    isAC02 = False
    isPrint = False
    contImg = 57

    for i in range(160):
        timeBuffer.append(i)
        
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

                fig, axis = plt.subplots(3)
                fig.suptitle('ACs')

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

                # plotting the points
                axis[0].plot(timeBuffer, acBuffer1)
                axis[1].plot(timeBuffer, acBuffer2)
                axis[2].plot(timeBuffer, acBuffer3)
                
                axis[0].axhline(y = 0, color = 'r', linestyle = 'dashed')
                axis[1].axhline(y = 0, color = 'r', linestyle = 'dashed')
                axis[2].axhline(y = 0, color = 'r', linestyle = 'dashed')

            elif sInputDecoded == "%":
                isPrint = True

            if isPrint:
                if sInputDecoded != "%":
                    dataText.append(sInputDecoded)

            if len(acBuffer1) >= 160:

                # function to show the plot
                fig.set_size_inches(7.0, 5.0)
                plt.subplots_adjust(left=0.3)

                dataText.reverse()
                for j in range(len(dataText)):
                    plt.figtext(0.05,0.00 + (3*j/100), dataText[j], fontsize=8, va="top", ha="left")
                
                plt.savefig("AC_"+ str(contImg) +".png", bbox_inches = "tight")
                contImg += 1
                #plt.draw()
                #plt.pause(10.0)
                #plt.close()

                acBuffer1.clear()
                acBuffer2.clear()
                acBuffer3.clear()
                dataText.clear()

        except UnicodeDecodeError:
            print("Invalid CHAR")


if __name__ == "__main__":
    main()
