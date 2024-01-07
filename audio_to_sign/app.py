from tkinter import *
import pyaudio
import wave
import threading
from tkVideoPlayer import TkinterVideo
from moviepy.editor import *
from moviepy.editor import VideoFileClip
import subprocess
from signtoaudio import sign_language_to_audio
import cv2
from PIL import Image, ImageTk
import os
from queue import Queue
from transformers import pipeline
from utils import transcribe
from speech import speech
import pygame

result_queue = Queue()
pipe = pipeline(task = "automatic-speech-recognition", model = "voice_model")


root = Tk()
paudio = pyaudio.PyAudio()
sample_rate=16000 
channels=2
format=pyaudio.paInt16

cached_transcription = ""

audio_record_file_name = "audio_recording.wav"
audio_data = []
recording_finished = threading.Event()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

audio_to_sign_language_response = []

audio_is_recording = 0

lock = threading.Lock()

# Set the window geometry to full screen
root.geometry(f"{screen_width}x{screen_height}")

# Create a frame and pack it to fill the window
audio_thread = ""
stack_of_screens = ["root"]
# Create frames for each page
home_page = Frame(root,bg="white")

audio_record_screen = Frame(root, bg="white")

video_display_screen = Frame(root)

header_color = "#42c8f5"
image_path="resources/back.png"
image_width = 100
image_height = 40

header_frame = Frame(root, bg=header_color, height=50)

original_image = Image.open(image_path)
resized_image = original_image.resize((image_width, image_height))
back_button_image = ImageTk.PhotoImage(resized_image)
#back_button_image = PhotoImage(file = "back.png")


# header_frame.rowconfigure(0,weight=1)
# header_frame.columnconfigure(0,weight=1)
# header_frame.columnconfigure(1,weight=1)

header_frame_home = Frame(root, bg=header_color, height=50)

videoplayer = TkinterVideo(master=video_display_screen, scaled=True)
videoplayer.pack(expand=True, fill="both")

label_video_display_screen = Label(video_display_screen,text="Video Here")
label_video_display_screen.pack()

# Initially, display only the first page
def show_initial_home_page():
    header_frame_home.pack(fill='x')
    home_page.pack()
    home_page.pack(fill="both", expand=True)

# Define functions to switch between pages
def show_home_page():
    header_frame_home.pack(fill='x')
    home_page.pack()
    home_page.pack(fill="both", expand=True)
    audio_record_screen.pack_forget()
    header_frame.pack_forget()

def show_audio_record():
    stack_of_screens.append("audio_record")
    header_frame.pack(fill="both")
    audio_record_screen.pack()
    audio_record_screen.pack(fill="both", expand=True)
    home_page.pack_forget()
    video_display_screen.pack_forget()
    header_frame_home.pack_forget()

def go_back():
    stack_of_screens.pop()
    show_screen = stack_of_screens[-1]
    navigate(show_screen)



def navigate(screen_name):
    if screen_name == "root":
        show_home_page()
    elif screen_name == "audio_record":
         stack_of_screens.pop()
         show_audio_record()
def launch_recorder(button_start,button_stop,button_translate):
     global cached_transcription
     cached_transcription = ""
     button_translate.config(state=DISABLED)
     global audio_thread
     audio_thread = threading.Thread(target=record_audio)
     audio_thread.start()
     button_start.config(state= DISABLED)
     button_stop.config(state= NORMAL)
def record_audio():
    global audio_is_recording 
    audio_is_recording = 1
    stream = paudio.open(format=pyaudio.paInt16,
                    channels=2,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024)
    global audio_data 
    audio_data = bytearray()
    num = 0
    while True:
            with lock:
                if audio_is_recording != 1:
                     break
            data = stream.read(1024)
            audio_data.extend(data)
            num +=1
    stream.stop_stream()
    stream.close()
    recording_finished.set()
    
    
def finalize_audio_recording(button_start,button_stop,button_translate):
     global audio_is_recording
     audio_is_recording = 0
     recording_finished.wait()
     audio_thread.join()
     with wave.open(audio_record_file_name, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(pyaudio.get_sample_size(format))
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data)
     print("File saved.")
     button_start.config(state=NORMAL)
     button_stop.config(state=DISABLED)
     button_translate.config(state=NORMAL)
     #CHANGE 
def translate_to_sign_language():
    stack_of_screens.append("video_display")
    video_display_screen.pack()
    audio_record_screen.pack(fill="both", expand=True)
    audio_record_screen.pack_forget()
    home_page.pack_forget()

# def close_window():
#     root.destroy()

     
    

# Replace 'example_script.py' with the actual name of your Python script
def run_script(script_path):
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
     
def display_videos():
    script_path = 'pygame_video.py'
    #print(transcribe("audio_recording.wav",pipe))
    my_thread = threading.Thread(target=audio_processing)
    my_thread.start()
def launch_cv2():
     cv2_thread = threading.Thread(target=sign_language_to_audio,args=(cv2,))
     cv2_thread.start()

def audio_processing():
    global cached_transcription
    if cached_transcription == "":
        text = transcribe("audio_recording.wav",pipe)
        text = text.lower()
        text = text.replace("."," ")
        text = text.replace("!"," ")
        text = text.replace("!"," ")
        text = text.replace("?"," ")
        text = text.replace("-"," ")
        text = text.replace(","," ")
        text = text.replace("'"," ")
        cached_transcription = text
    else:
        text = cached_transcription
    #  script_thread = threading.Thread(target=run_script, args=("pygame_video.py",))
    script_thread = threading.Thread(target = speech, args=(pygame,VideoFileClip,text))
    script_thread.start()
    script_thread.join()
     
     
     
    
# Create buttons to trigger page navigation
home_page.columnconfigure(0, weight=1)
home_page.columnconfigure(1, weight=1)
home_page.columnconfigure(2, weight=1)
home_page.rowconfigure(0,weight=1)
home_page.rowconfigure(1,weight=1)
home_page.rowconfigure(2,weight=1)
home_page.rowconfigure(3,weight=1)
home_page.rowconfigure(4,weight=1)

audio_record_screen.columnconfigure(0, weight=1)
audio_record_screen.columnconfigure(1, weight=1)
audio_record_screen.columnconfigure(2, weight=1)
audio_record_screen.rowconfigure(0,weight=1)
audio_record_screen.rowconfigure(1,weight=1)
audio_record_screen.rowconfigure(2,weight=1)
audio_record_screen.rowconfigure(3,weight=1)
audio_record_screen.rowconfigure(4,weight=1)
audio_record_screen.rowconfigure(5,weight=1)
audio_record_screen.rowconfigure(6,weight=1)



translate_sign_language_to_audio_button = Button(home_page, text="Audio To Sign Language", command=show_audio_record)
translate_sign_language_to_audio_button.grid(column=1,row=1)
translate_sign_language_to_audio_button = Button(home_page, text="Sign Language To Audio",command=launch_cv2)
translate_sign_language_to_audio_button.grid(column=1,row=3)


start_audio_recording = Button(audio_record_screen, text="Start Recording", command = lambda :launch_recorder(start_audio_recording,stop_audio_recording,translate_to_audio))
start_audio_recording.grid(column=1,row=1)

stop_audio_recording = Button(audio_record_screen, text="Stop Recording", command= lambda: finalize_audio_recording(start_audio_recording,stop_audio_recording,translate_to_audio),state=DISABLED)
stop_audio_recording.grid(column=1,row=3)
translate_to_audio = Button(audio_record_screen, text="Translate", command= display_videos, state=DISABLED)
translate_to_audio.grid(column=1,row=5)

back_button = Button(header_frame,text="Back",command=go_back,image=back_button_image,width=100, height=40)
back_button.pack(side="left")



play_video = Button(video_display_screen,text="Play Video",command=display_videos)
play_video.pack()

show_initial_home_page()

# root.protocol("WM_DELETE_WINDOW", close_window)

root.mainloop()
