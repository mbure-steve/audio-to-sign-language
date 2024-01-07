import unittest
from utils import synonym, show_num_videos, prep_num_videos, text2int 
from speech import add_finger_spelling, sign_sentence
import spacy

class TestAddFingerSpelling(unittest.TestCase):
    def test_correct_synonym(self):
        query = "eat"
        result = synonym(query)
        expected_result = ["food.mp4"]
        self.assertEqual(result, expected_result)

    def test_correct_reversed_synonym(self):
        query = "food"
        result = synonym(query)
        expected_result = ["eat.mp4"]
        self.assertEqual(result, expected_result)
    def test_correct_show_num_videos_20to99(self):
        list_video =["20","2"]
        result = show_num_videos(list_video)
        expected_result = ["2.mp4","0.mp4","2.mp4"]
        self.assertEqual(result, expected_result)
    def test_correct_show_num_videos_10to19(self):
        list_video =["10","2"]
        result = show_num_videos(list_video)
        expected_result = ["10.mp4","0.mp4","2.mp4"]
        self.assertEqual(result, expected_result)
    def test_correct_prep_num_videos(self):
        num = 123
        result = prep_num_videos(num)
        expected_result = ["100","23"]
        self.assertEqual(result, expected_result)

    def test_correct_add_fingerspelling(self):
        query = ["school"]
        result = add_finger_spelling(query)
        expected_result =  ['s.mp4', 'c.mp4', 'h.mp4', 'o.mp4', 'o.mp4', 'l.mp4']
        self.assertEqual(result, expected_result)

    def test_correct_sign_sentence(self):
        query = "The boy ate the mango"
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(query)
        result = sign_sentence(doc)
        expected_result = ["boy","mango","eat"]
        self.assertEqual(result, expected_result)

    #Integrated test
    def test_correct_text2int(self):
        query = "thirty six"
        result = text2int(query)
        expected_result =  ["3.mp4","6.mp4"]
        self.assertEqual(result, expected_result)

    
    

if __name__ == '__main__':
    unittest.main()