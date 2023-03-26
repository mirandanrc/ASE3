import pyaudio
import numpy as np
import time
import sounddevice as sd
from scipy.io.wavfile import write
import whisper

#variables amplitude
CHUNK = 1024
RATE = 44100
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

global operation_mode
global flag_audio_continua
global amplitud_to_whisper
global amplitud_to_audio
operation_mode = "spike"
flag_audio_continua = True

#variables recorder
global flag_record
global flag_record_option
global flag_corte
global audio_to_amplitud
global audio_to_whisper
flag_record = False
flag_record_option = ""
flag_corte = False

#variables whisper
global command_finished
global check_audio
global whisper_to_amplitud
global whisper_to_audio
command_finished = False
check_audio = False

#functions amplitude
def amplitude_whisper(msg):
    global operation_mode
    if msg.data == "set_to_spike":
        print("From Whisper Set operation mode to SPIKE")
        operation_mode = "spike"
    elif msg.data == "set_to_silence":
        print("From Whisper Set operation mode to SILENCE")
        operation_mode = "silence"

def amplitud_audio(msg):
    global flag_audio_continua
    if msg.data == "continua":
        print("Audio recorder esta libre, continua")
        flag_audio_continua = True
    elif msg.data == "espera":
        print("Audio recorder esta grabando, esperando")
        flag_audio_continua = False

def listening():
    THRESHOLD_HIGH = 500
    THRESHOLD_LOW = 200
    THRESHOLD_SILENCE = 200

    global operation_mode
    global flag_audio_continua
    global amplitud_to_whisper
    global amplitud_to_audio
    silence_time = 0
    count_silence = 0

    while True:
        data = stream.read(CHUNK)
        data = np.fromstring(data, dtype=np.int16)
        ampl = np.abs(np.average(data))
        #print("Amplitude:", ampl)

        if operation_mode == "spike" and flag_audio_continua:
            if ampl > THRESHOLD_LOW and ampl < THRESHOLD_HIGH:
                print("Amplitude SPIKE:", ampl)
                amplitud_to_audio="spike"

        if operation_mode == "silence":
            print("Amplitude:", ampl)
            if ampl < THRESHOLD_SILENCE:
                count_silence += 1
            elif ampl > THRESHOLD_SILENCE:
                count_silence = 0
            if count_silence > 150:
                print("Amplitude SILENCE:", ampl)
                amplitud_to_whisper="silence"
                amplitud_to_audio="silence"
                count_silence = 0

#functions recorder
def audio_amplitud(msg):
    global flag_record
    global flag_record_option
    global flag_corte

    if msg.data == "spike":
        print("Record SPIKE")
        flag_record = True
        flag_record_option = "spike"
    elif msg.data == "silence":
        print("Recording STOP")
        flag_corte = True

def audio_whisper(msg):
    global flag_corte
    global flag_record
    global flag_record_option
    if msg.data == "stop_recording_command":
        print("Recording STOP")
        flag_corte = True
    elif msg.data == "command":
        print("Record COMMAND")
        flag_record = True
        flag_record_option = "command"

def recorder():
    global flag_record
    global flag_record_option
    global flag_corte
    global audio_to_amplitud
    global audio_to_whisper

    while True:
        if flag_record_option == "spike":
            audio_to_amplitud="espera"

            print("Recording wakeup call")
            seconds = 1
            wakeupcallrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()
            nombre = "audio.wav"
            write(nombre, fs, wakeupcallrecording)
            print("Wakeup call recorded")

            audio_to_amplitud="continua"
            audio_to_whisper="check_audio"

            flag_record_option = "none"

        elif flag_record_option == "command":
            for i in range(3):
                print("Recording command")
                seconds = 3
                commandrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
                sd.wait()
                write('audio.wav', fs, commandrecording)
                print("Command recorded")

                audio_to_whisper="check_audio"

                if flag_corte:
                    break
            flag_corte = False

            flag_record_option = "none"

            audio_to_whisper="set_wake"
            audio_to_amplitud="set_spike"

#functions whisper
def whisper_amplitud(msg):
    global command_finished
    if (msg.data == "silence"):
        command_finished = True

def whisper_audio(msg):
    global check_audio
    if msg.data == "check_audio":
        check_audio = True
    print(msg)

def whisper_logic():
    validwakeupcalls = ["Markovito", "Markovito.", "markovito", "markovito.", "Marcovito", "Marcovito.",
                        "marcovito", "marcovito.", "marko Vito", "Marko Vito.", "Marko vito",
                        "Marko vito.", "marko Vito", "marko Vito.", "marko vito", "marko vito.",
                        "Marco Vito", "Marco Vito.", "Marco vito", "Marco vito.", "marco Vito",
                        "marco Vito.", "marco vito", "marco vito.", "Marko", "marko", "Marco", "marco", "Vito", "vito"]
    validexitcalls = ["Exit", "exit", "Exit.", "exit."]
    model = whisper.load_model("base")
    flag_opcion = "wake"
    command = ""

    global check_audio
    global command_finished

    global whisper_to_amplitud
    global whisper_to_audio


    while True:
        time.sleep(0.1)
        if check_audio:
            check_audio = False

            print(f"Traslating option: {flag_opcion}")
            wakeresult = model.transcribe("audio.wav")
            wakeresult_text = wakeresult["text"]
            print(f"Traslate: {wakeresult_text}")

            wakeresult_text_split = wakeresult_text.split()

            if flag_opcion == "wake":
                for word in wakeresult_text_split:
                    if word in validwakeupcalls:
                        print("Valid WAKEUP")
                        whisper_to_amplitud="set_to_silence"
                        whisper_to_audio="command"
                        flag_opcion = "command"

            elif flag_opcion == "command":
                command += wakeresult_text
                for word in wakeresult_text_split:
                    if word in validexitcalls:
                        command_finished = True
                        print("Valid EXIT")

        if command_finished:
            print("Comando finalizado")
            whisper_to_amplitud="set_to_spike"
            whisper_to_audio="stop_recording_command"
            flag_opcion = "wake"
            print("Comando: ", command)
            command = ""
            command_finished = False

        return 

        


if __name__ == '__main__':
    fs = 44100 

    #subscribers amplitude
    amplitud_audio() #amplitud_to_audio
    amplitude_whisper() #amplitud_to_whisper
    listening()

    #subscribers audiorecorder
    audio_amplitud() #audio_to_amplitud
    audio_whisper() #audio_to_whisper
    recorder()

    #subscribers whisper
    whisper_amplitud() #whisper_to_amplitud
    whisper_audio() #whisper_to_audio
    whisper_logic()

    #amplitud
    #pub_audiorecorder from amplitud = amplitud_to_audio
    #pub_whisper from amplitud = amplitud_to_whisper

    #audiorecorder
    #pub_amplitud from audiorecorder = audio_to_amplitud
    #pub_whisper from audiorecorder = audio_to_whisper

    #whisper
    #pub_amplitud from whisper = whisper_to_amplitud
    #pub_audiorecorder from whisper = whisper_to_audio
