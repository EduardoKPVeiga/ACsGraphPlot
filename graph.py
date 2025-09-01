import serial
import matplotlib.pyplot as plt
import statistics as statcs
import os
import subprocess

ser = serial.Serial(
   port='COM11',
   baudrate=38400,
   parity=serial.PARITY_ODD,
   stopbits=serial.STOPBITS_TWO,
   bytesize=serial.EIGHTBITS
)

# Buffers de dados
timeBuffer = []
timePHBuffer = []
dataText = []
acBuffer1, acBuffer2, acBuffer3 = [], [], []
rmsBuffer1, rmsBuffer2, rmsBuffer3 = [], [], []
fqBuffer1, fqBuffer2, fqBuffer3 = [], [], []
phBuffer2, phBuffer3 = [], []

# Contadores
contImg, contPHs, contFQs, contRMSs = 0, 0, 0, 0
contImgPHs, contImgFQs, contImgRMSs = 0, 0, 0

# Valores Padrão (Default) para comparação
defaultPhaseAC02 = 0
defaultPhaseAC03 = 0
defaultFrequency = 6000
defaultRMS = 12700
defaultRMS2 = 2400
defaultRMS3 = 0

workingDirPath = os.path.dirname(os.path.abspath(__file__))

def plotACGraph():
    """
    Gera o gráfico das formas de onda AC com legendas individuais e organizadas.
    """
    global workingDirPath, acBuffer1, acBuffer2, acBuffer3, contImg, dataText, timeBuffer

    fig, axis = plt.subplots(3, 1, figsize=(10, 7))
    fig.suptitle('Formas de Onda (ACs)', fontsize=16)
    plt.subplots_adjust(left=0.35, top=0.9, hspace=0.5)

    axis[0].plot(timeBuffer, acBuffer1)
    axis[1].plot(timeBuffer, acBuffer2)
    axis[2].plot(timeBuffer, acBuffer3)

    for ax in axis:
        ax.axhline(y=0, color='r', linestyle='dashed')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_ylabel('Amplitude')
    axis[2].set_xlabel('Amostra')

    try:
        idx1 = dataText.index("AC01")
        idx2 = dataText.index("AC02")
        idx3 = dataText.index("AC03")

        info_ac1, info_ac2, info_ac3 = dataText[idx1:idx2], dataText[idx2:idx3], dataText[idx3:]
        text_ac1, text_ac2, text_ac3 = "\n".join(info_ac1), "\n".join(info_ac2), "\n".join(info_ac3)

        props = {'family': 'monospace', 'fontsize': 9}
        axis[0].text(-0.5, 0.5, text_ac1, transform=axis[0].transAxes, va='center', ha='left', fontdict=props)
        axis[1].text(-0.5, 0.5, text_ac2, transform=axis[1].transAxes, va='center', ha='left', fontdict=props)
        axis[2].text(-0.5, 0.5, text_ac3, transform=axis[2].transAxes, va='center', ha='left', fontdict=props)
    except ValueError:
        print("Aviso: Marcadores 'AC01', 'AC02' ou 'AC03' não encontrados.")

    ACFileName = f"ACs\\AC_{contImg}.png"
    plt.savefig(os.path.join(workingDirPath, ACFileName))
    contImg += 1
    plt.close(fig)

    acBuffer1.clear(); acBuffer2.clear(); acBuffer3.clear(); dataText.clear()

def plotFQErrorGraph():
    """
    Gera o gráfico de análise de Frequência (FQ) com estatísticas individuais.
    """
    global workingDirPath, contImgFQs, contFQs
    global fqBuffer1, fqBuffer2, fqBuffer3

    if not all([fqBuffer1, fqBuffer2, fqBuffer3]):
        print("Aviso: Buffers de frequência vazios. Gráfico FQ não gerado.")
        fqBuffer1.clear(); fqBuffer2.clear(); fqBuffer3.clear(); contFQs = 0
        return

    stats_data = []
    buffers = [fqBuffer1, fqBuffer2, fqBuffer3]
    defaults = [defaultFrequency, defaultFrequency, defaultFrequency]
    ac_names = ["AC01", "AC02", "AC03"]

    for i in range(3):
        avg = statcs.median(buffers[i])
        stdev = statcs.stdev(buffers[i]) if len(buffers[i]) > 1 else 0
        if defaults[i] != 0:
            erro_percent = abs(100 - (avg * 100 / defaults[i])) + (stdev * 100 / defaults[i])
        else:
            erro_percent = float('inf') if avg != 0 or stdev != 0 else 0.0
        stats_data.append({"name": ac_names[i], "avg": avg, "stdev": stdev, "error": erro_percent, "default": defaults[i]})

    figFQ, axisFQ = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    figFQ.suptitle('Análise de Frequência (FQ)', fontsize=16)
    plt.subplots_adjust(left=0.35, top=0.9, hspace=0.6)
    
    for i, ax in enumerate(axisFQ):
        data, stats = buffers[i], stats_data[i]
        x_axis = range(len(data))
        
        ax.plot(x_axis, data, marker='.', linestyle='-', markersize=4, label='Medição')
        ax.axhline(y=stats["avg"], color='r', linestyle='--', label=f'Mediana: {stats["avg"]:.0f}')
        ax.axhline(y=stats["default"], color='g', linestyle='--', label=f'Padrão: {stats["default"]}')
        
        ax.set_title(f'Frequência - {stats["name"]}')
        ax.set_ylabel('Frequência (Hz * 100)')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='upper right')

        text_info = f"Mediana: {stats['avg']:.2f}\nDesvio Padrão: {stats['stdev']:.2f}\nErro Total: {stats['error']:.2f}%"
        props = {'family': 'monospace', 'fontsize': 9}
        ax.text(-0.55, 0.5, text_info, transform=ax.transAxes, va='center', ha='left', fontdict=props)

    axisFQ[-1].set_xlabel('Amostra')

    FQFileName = f"FQs\\FQ_{contImgFQs}.png"
    plt.savefig(os.path.join(workingDirPath, FQFileName))
    contImgFQs += 1
    plt.close(figFQ)

    fqBuffer1.clear(); fqBuffer2.clear(); fqBuffer3.clear(); contFQs = 0

def plotPHErrorGraph():
    """
    Gera o gráfico de análise de Fase (PH) com estatísticas individuais.
    """
    global workingDirPath, contImgPHs, contPHs
    global phBuffer2, phBuffer3

    if not all([phBuffer2, phBuffer3]):
        print("Aviso: Buffers de fase vazios. Gráfico PH não gerado.")
        phBuffer2.clear(); phBuffer3.clear(); contPHs = 0
        return

    stats_data = []
    buffers = [phBuffer2, phBuffer3]
    defaults = [defaultPhaseAC02, defaultPhaseAC03]
    ac_names = ["AC02 vs AC01", "AC03 vs AC01"]

    for i in range(2):
        avg = statcs.median(buffers[i])
        stdev = statcs.stdev(buffers[i]) if len(buffers[i]) > 1 else 0
        if defaults[i] != 0:
            erro_percent = abs(100 - (avg * 100 / defaults[i])) + (stdev * 100 / defaults[i])
        else:
            erro_percent = float('inf') if avg != 0 or stdev != 0 else 0.0
        stats_data.append({"name": ac_names[i], "avg": avg, "stdev": stdev, "error": erro_percent, "default": defaults[i]})
        
    figPH, axisPH = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    figPH.suptitle('Análise de Fase (PH)', fontsize=16)
    plt.subplots_adjust(left=0.35, top=0.85, hspace=0.6)

    for i, ax in enumerate(axisPH):
        data, stats = buffers[i], stats_data[i]
        x_axis = range(len(data))

        ax.plot(x_axis, data, marker='.', linestyle='-', markersize=4, label='Medição')
        ax.axhline(y=stats["avg"], color='r', linestyle='--', label=f'Mediana: {stats["avg"]:.0f}')
        ax.axhline(y=stats["default"], color='g', linestyle='--', label=f'Padrão: {stats["default"]}')
        
        ax.set_title(f'Fase - {stats["name"]}')
        ax.set_ylabel('Defasagem')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='upper right')

        text_info = f"Mediana: {stats['avg']:.2f}\nDesvio Padrão: {stats['stdev']:.2f}\nErro Total: {stats['error']:.2f}%"
        props = {'family': 'monospace', 'fontsize': 9}
        ax.text(-0.55, 0.5, text_info, transform=ax.transAxes, va='center', ha='left', fontdict=props)

    axisPH[-1].set_xlabel('Amostra')
    
    PHFileName = f"PHs\\PH_{contImgPHs}.png"
    plt.savefig(os.path.join(workingDirPath, PHFileName))
    contImgPHs += 1
    plt.close(figPH)
    
    phBuffer2.clear(); phBuffer3.clear(); contPHs = 0

def plotRMSErrorGraph():
    """
    Gera o gráfico de análise de Tensão Eficaz (RMS) com estatísticas individuais.
    """
    global workingDirPath, contImgRMSs, contRMSs
    global rmsBuffer1, rmsBuffer2, rmsBuffer3

    if not all([rmsBuffer1, rmsBuffer2, rmsBuffer3]):
        print("Aviso: Buffers de RMS vazios. Gráfico RMS não gerado.")
        rmsBuffer1.clear(); rmsBuffer2.clear(); rmsBuffer3.clear(); contRMSs = 0
        return

    stats_data = []
    buffers = [rmsBuffer1, rmsBuffer2, rmsBuffer3]
    defaults = [defaultRMS, defaultRMS2, defaultRMS3]
    ac_names = ["AC01", "AC02", "AC03"]

    for i in range(3):
        avg = statcs.median(buffers[i])
        stdev = statcs.stdev(buffers[i]) if len(buffers[i]) > 1 else 0
        if defaults[i] != 0:
            erro_percent = abs(100 - (avg * 100 / defaults[i])) + (stdev * 100 / defaults[i])
        else:
            erro_percent = float('inf') if avg != 0 or stdev != 0 else 0.0
        stats_data.append({"name": ac_names[i], "avg": avg, "stdev": stdev, "error": erro_percent, "default": defaults[i]})

    figRMS, axisRMS = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    figRMS.suptitle('Análise de Tensão Eficaz (RMS)', fontsize=16)
    plt.subplots_adjust(left=0.35, top=0.9, hspace=0.6)

    for i, ax in enumerate(axisRMS):
        data, stats = buffers[i], stats_data[i]
        x_axis = range(len(data))
        
        ax.plot(x_axis, data, marker='.', linestyle='-', markersize=4, label='Medição')
        ax.axhline(y=stats["avg"], color='r', linestyle='--', label=f'Mediana: {stats["avg"]:.0f}')
        ax.axhline(y=stats["default"], color='g', linestyle='--', label=f'Padrão: {stats["default"]}')
        
        ax.set_title(f'RMS - {stats["name"]}')
        ax.set_ylabel('Valor RMS')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='upper right')

        text_info = f"Mediana: {stats['avg']:.2f}\nDesvio Padrão: {stats['stdev']:.2f}\nErro Total: {stats['error']:.2f}%"
        props = {'family': 'monospace', 'fontsize': 9}
        ax.text(-0.55, 0.5, text_info, transform=ax.transAxes, va='center', ha='left', fontdict=props)

    axisRMS[-1].set_xlabel('Amostra')

    RMSFileName = f"RMSs\\RMS_{contImgRMSs}.png"
    plt.savefig(os.path.join(workingDirPath, RMSFileName))
    contImgRMSs += 1
    plt.close(figRMS)

    rmsBuffer1.clear(); rmsBuffer2.clear(); rmsBuffer3.clear(); contRMSs = 0

def main():
    try:
        print("Executando script de limpeza de diretórios...")
        subprocess.run(["python", "clean_graphs.py"], check=True)
        print("Limpeza concluída.")
    except FileNotFoundError:
        print("ERRO: O arquivo 'clean_graphs.py' não foi encontrado.")
        return
    except subprocess.CalledProcessError as e:
        print(f"ERRO: O script de limpeza falhou com o erro: {e}")
        return
    
    global timeBuffer, timePHBuffer, dataText
    global acBuffer1, acBuffer2, acBuffer3
    global rmsBuffer1, rmsBuffer2, rmsBuffer3
    global fqBuffer1, fqBuffer2, fqBuffer3
    global phBuffer2, phBuffer3
    global contPHs, contFQs, contRMSs

    isAC01, isAC02, isPrint = True, False, False
    PHSample, FQSample, RMSSample = 30, 30, 30
    isPH02, isPH03 = False, False

    fq_graph_plotted = False
    ph_graph_plotted = False
    rms_graph_plotted = False
    
    for i in range(160):
        timeBuffer.append(i)
    for i in range(PHSample):
        timePHBuffer.append(i)
        
    print("Iniciando leitura da porta serial. Aguardando dados...")
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
                        isAC01, isAC02 = False, True
                    elif isAC02:
                        acBuffer2.append(int(value))
                        isAC02 = False
                    else:
                        acBuffer3.append(int(value))
                        isAC01 = True
                
                avg1 = statcs.mean(acBuffer1)
                avg2 = statcs.mean(acBuffer2)
                avg3 = statcs.mean(acBuffer3)

                for l in range(160):
                    acBuffer1[l] -= avg1
                    acBuffer2[l] -= avg2
                    acBuffer3[l] -= avg3

            elif sInputDecoded == "%":
                isPrint = True

            if isPrint and sInputDecoded != "%":
                dataText.append(sInputDecoded)
                if sInputDecoded == "AC01":
                    isPH02, isPH03 = False, False
                elif sInputDecoded == "AC02":
                    isPH02, isPH03 = True, False
                elif sInputDecoded == "AC03":
                    isPH02, isPH03 = False, True

                if 'ph_i' in sInputDecoded:
                    phase = int(sInputDecoded.split(': ')[1])
                    if isPH02: phBuffer2.append(phase)
                    elif isPH03:
                        phBuffer3.append(phase)
                        contPHs += 1
                elif 'f_i' in sInputDecoded:
                    frequency = int(sInputDecoded.split(': ')[1])
                    if not isPH02 and not isPH03: fqBuffer1.append(frequency)
                    elif isPH02: fqBuffer2.append(frequency)
                    elif isPH03:
                        fqBuffer3.append(frequency)
                        contFQs += 1
                elif 'rms_i' in sInputDecoded:
                    rms = int(sInputDecoded.split(': ')[1])
                    if not isPH02 and not isPH03: rmsBuffer1.append(rms)
                    elif isPH02: rmsBuffer2.append(rms)
                    elif isPH03:
                        rmsBuffer3.append(rms)
                        contRMSs += 1

            if len(acBuffer3) >= 160:
                plotACGraph()

            if contRMSs >= RMSSample and not rms_graph_plotted:
                plotRMSErrorGraph()
                rms_graph_plotted = True

            if contPHs >= PHSample and not ph_graph_plotted:
                plotPHErrorGraph()
                ph_graph_plotted = True

            if contFQs >= FQSample and not fq_graph_plotted:
                plotFQErrorGraph()
                fq_graph_plotted = True

            if fq_graph_plotted and ph_graph_plotted and rms_graph_plotted:
                print("\nTodos os gráficos de análise (FQ, PH, RMS) foram gerados. Encerrando o programa.")
                break

        except (UnicodeDecodeError, ValueError, IndexError):
            pass

if __name__ == "__main__":
    main()