# from pygame_video import pygame_video
# import pygame
# from moviepy.editor import VideoFileClip
import os
import spacy

def text2int(textnum2, numwords={}):
    textnum = textnum2.lower()
    textnum = textnum.replace("-"," ")
    textnum = textnum.replace("."," ")
    textnum = textnum.replace("!"," ")
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    # return result + current
    return show_num_videos(prep_num_videos(result+current))
def prep_num_videos(num):
    num_string = f"{num}"
    len_num_string = len(num_string)
    numbers = []

    for index, value in enumerate(num_string):
        if index == len_num_string - 2 :
            numbers.append(value+num_string[index+1])
            break
        else:
            len_to_end = (len_num_string - index) - 1
            numbers.append(value+"0"*len_to_end)
    # print(numbers)
    return numbers
def show_num_videos(list_num):
    video_names=[]
    for value in list_num:
        if len(value) == 4:
            video_names.append(f"{value}.mp4")
        elif len(value) == 3:
            video_names.append(f"{value}.mp4")
        elif len(value) == 2:
            if(value[0])=="1":
                video_names.append(f"10.mp4")
                video_names.append(f"{value[1]}.mp4")
            else:
                video_names.append(f"{value[0]}.mp4")
                video_names.append(f"{value[1]}.mp4")
        elif len(value) == 1:
            video_names.append(f"{value}.mp4")
    # print(video_names)
    return video_names
    # pygame_video(pygame,VideoFileClip,video_names)


def synonym(query):
    final_result = []
    added_synonyms = ["eatfood","abstainavoid","fightbattle"]
    for i in added_synonyms:
        if query in i :
            final_result.append(f'{i.replace(f"{query}","")}.mp4') 
    return final_result

def transcribe(audio,pipe):
    text = pipe(audio)["text"]
    return text

def sign_sentence(doc):

    # for i in doc:
    #     print(i,i.pos_, i.dep_)
    subject = None
    verb = None
    obj = None

    # Iterate through the tokens in the sentence
    for token in doc:
        # Check if the token is the main verb of the sentence
        if "ROOT" in token.dep_:
            verb = token.lemma_
        
        # Check if the token is a subject
        if "subj" in token.dep_:
            subject = token.lemma_
        
        # Check if the token is an object
        if "obj" in token.dep_:
            obj = token.lemma_

    # Print the extracted subject, verb, and object
    # print("Subject:", subject)
    # print("Verb:", verb)
    # print("Object:", obj)
    if subject is not None and verb is not None and obj is not None:
        adverbs = []
        obj_adjectives = []
        subj_adjectives = []
        for token in doc:
            if token.text == verb:
                for child in token.children:
                    if child.pos_ == "ADV":
                        adverbs.append(child.lemma_)
            elif token.text == subject:
                for child in token.children:
                    if child.pos_ == "ADJ":
                        subj_adjectives.append(child.lemma_)
            elif token.text == obj:
                for child in token.children:
                    if child.pos_ == "ADJ":
                        obj_adjectives.append(child.lemma_)
        sentence = []
        sentence.append(subject)
        sentence.extend(subj_adjectives)
        sentence.append(obj)
        sentence.extend(obj_adjectives)
        sentence.append(verb)
        sentence.extend(adverbs)
        return sentence
    else:
        return doc




