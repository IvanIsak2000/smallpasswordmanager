from os import remove
import unittest
from main import *


class FunctionalTesting(unittest.TestCase):
    # There is no test for `check_mistake_question` function,
    # as it just makes some output to stdout
    def test_make_column_output(self):
        _line_ = ['service', 'login', 'password']
        example = make_column_output(_line_, 10, 20, 30)
        right_answer = "service   |login               |password                      "
        self.assertEqual(example, right_answer)
    
    def test_make_bad_answer_message(self):
        _params_ = ('text', 'text2', 'text3')
        example = make_bad_answer_message(*_params_)
        right_answer = 'Cannot recognize your answer. Please, type only text, text2 or text3.'
        self.assertEqual(example, right_answer)
    
    def test_get_pure_contents(self):
        with open("example.txt", "w") as filestream:
            text = """text1
text2
text3
"""
            filestream.write(text)
        with open("example.txt", "r") as filestream:
            example = get_pure_contents(filestream)
            right_answer = ['text1', 'text2', 'text3']
            self.assertEqual(example, right_answer)
        remove("example.txt")
    
    

