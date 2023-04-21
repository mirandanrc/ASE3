import pyaudio
import numpy as np
from time import sleep
import sounddevice as sd
from scipy.io.wavfile import write
import whisper


##GENERAL VARIABLES
CHUNK = 1024
RATE = 44100
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)


THRESHOLD_HIGH = 2000
THRESHOLD_LOW = 500
count_silence = 0


fs = 44100 

#Whisper variables
validwakeupcalls = ["Hola", "hola", "Hola!", "hola!", "Ola", "ola", "¡Hola!", "¡hola!", " Quique", " quique", " Quique!", " quique!", " Kike", " kike", " Kike!", " kike!"]
validexitcalls = ["Para", "para", "alto", "Alto"]
model = whisper.load_model("base")

flag_opcion = "wake"

flag_record_option = "spike"
check_audio = False
wait_restart = False


while True:

    stream.start_stream()
    
    data = stream.read(CHUNK)
    data = np.frombuffer(data, dtype=np.int16)
    ampl = np.abs(np.average(data))
    print("Amplitude:", ampl)

    flag_audio_continua = True

    if wait_restart:
        sleep(2)
        wait_restart=False
 
    if flag_audio_continua:
        wait_restart=False
        if ampl > THRESHOLD_LOW and ampl < THRESHOLD_HIGH:
            flag_audio_continua == False
            #flag_record_option = "spike"
            print("Amplitude SPIKE:", ampl)

            

            #while stream.is_active():
            #    sleep(0.1)

            stream.stop_stream()
            #stream.close()
            
            ##### RECORDING ####
            #if flag_record_option == "spike":
            #flag_record_option == "none"
            print("Recording wakeup call")
            seconds = 2
            wakeupcallrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()
            nombre = "audio.wav"
            write(nombre, fs, wakeupcallrecording)
            print("Wakeup call recorded")
            #flag_audio_continua = True
            check_audio = True

            #### WHISPER LOGIC ######
            if check_audio:
                check_audio = False
                wakeresult = model.transcribe("audio.wav", language="es")
                wakeresult_text = wakeresult["text"]
                print(f"Traslate: {wakeresult_text}")
                wakeresult_text_split = wakeresult_text.split()
            
                for word in wakeresult_text_split:
                    if word in validwakeupcalls:
                        print("Valid Command")
                        print("Comando: ", word)
                        ### MANDA VARIABLE ENCENDIDO###
                        flag_audio_continua = True
                        wait_restart=True
                    elif word in validexitcalls:
                        print("Valid WAKEUP")
                        print("Comando: ", word)
                        ### MANDA VARIABLE APAGADO###
                        flag_audio_continua = True
                        wait_restart=True
                    else:
                        print("Invalid WAKEUP")
                        flag_audio_continua = True
                        wait_restart=True



