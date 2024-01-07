from utils import text2int, synonym, sign_sentence
from pygame_video import pygame_video
import spacy
import os
import json



#Missing / special characters

def speech(pygame,VideoFileClip,string2):
    try :
        video_names = text2int(string2)
        pygame_video(pygame,VideoFileClip,video_names)
    except Exception as e:
        print("Not an int")
        nlp = spacy.load("en_core_web_sm")
        print(string2)
        doc = nlp(string2)
        result = []
        if len(doc) > 1:
            result = sign_sentence(doc)
            result = add_finger_spelling(result)
        else:
            text = doc[0].lemma_
            list_of_videos=[f"{text}"]
            result = add_finger_spelling(list_of_videos)
        pygame_video(pygame,VideoFileClip,result)

# speech(pygame,VideoFileClip,"jsand.")

def add_finger_spelling(video):
    new_video_list = []
    file_path = "resources"
    list_of_available_video = os.listdir(file_path)
    video_list = video[:]
    video_list = [f"{i}.mp4"for i in video_list]
    for name in video_list:
        if name not in list_of_available_video:
                if len(synonym(name[:-4])) != 0:
                    new_video_list.extend(synonym(name[:-4])) 
                    continue
                for letter in name[:-4]:
                    new_video_list.append(f"{letter}.mp4")
        else:
            new_video_list.append(name)
    return new_video_list





    # if video_list[0] in list_of_available_video:
    #     return video_list
    # word = "".join(video_list)
    # word = word.replace(".mp4","")
    # video_list = synonym(word) 
    # video_list = [f"{i}.mp4"for i in video_list]
    # print(f"{video_list}:s")
    # if len(video_list) > 0:
    #     for i in video_list:
    #         if i in list_of_available_video:
    #             return [f"{i}"]
    # else:    
    #     for name in video:
    #         if name not in list_of_available_video:
    #             for letter in name[:-4]:
    #                 new_video_list.append(f"{letter}.mp4")
    #         else:
    #             new_video_list.append(name)
    #     return new_video_list
# import pygame
# from moviepy.editor import VideoFileClip
# speech(pygame,VideoFileClip,"r'n")
# print(synonym("avoid.mp4"[:-4]))
