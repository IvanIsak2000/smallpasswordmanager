from os import remove
from unittest import TestCase
from main import *


objects = {}


def try_assign_attr(thing: object) -> None:
    setattr_args = [thing, "arguement_name", "value"]
    delattr_args = [thing, "arguement_value"]
    thing.setattr(*setattr_args)
    thing.delattr(*delattr_args)


class AlwaysDo:

    def tearDown(self):
        objects= {}


class ConfigTest(TestCase, AlwaysDo):

    def setUp(self):
        objects["config"] = Config()

    def test_main(self):
        testing_object = objects["config"]
        self.assertEqual(testing_object.mode, "r")
        self.assertEqual(testing_object.filename, "passwords.txt")
        self.assertTrue(type(testing_object.yesno), set)
        self.assertRaises(AttributeError, try_assign_attr, [testing_object])
        self.assertRaises(AttributeError, try_assign_attr, [testing_object])


class StorageFileTest(TestCase, AlwaysDo):

    def setUp(self):
        stream = open("passwords.txt", "a", encoding="utf8")
        stream.write("\n")
        stream.close()
        objects["config"] = Config()
        config = objects["config"]
        objects["testing_object"] = StorageFile(config.filename)
    
    def test_main(self):
        testing_object = objects["testing_object"]
        self.assertRaises(AttributeError, try_assign_attr, [testing_object])
        self.assertRaises(AttributeError, try_assign_attr, [testing_object])
        remove("passwords.txt")


class  FreezerTest(TestCase, AlwaysDo):

    def setUp(self):
        objects["testing_object"] = Freezer()
    
    def test_main(self):
        testing_object = objects["testing_object"]
        self.assertRaises(AttributeError, try_assign_attr, [testing_object])
        self.assertRaises(AttributeError, try_assign_attr, [testing_object])
    

class StatusMessageTest(TestCase, AlwaysDo):

    def setUp(self):
        objects["message1"] = StatusMessage("written")
        objects["message2"] = StatusMessage("no_written", error=BaseException)
        objects["message3"] = StatusMessage("no_entries")
        objects["message4"] = StatusMessage("entries_deleted", 12)
        objects["message5"] = StatusMessage("written", 16, error=AttributeError)
        objects["wrong_message_4"] = StatusMessage("entries_deleted")
    
    def test_main(self):
        testing_object = objects["message1"]
        self.assertRaises(AttributeError, try_assign_attr, [testing_object])
        self.assertRaises(AttributeError, try_assign_attr, [testing_object])
        self.assertEqual("Successfully written", str(objects["message1"]))
        self.assertEqual("Error occured when writing to file: <class 'BaseException'>",
            str(objects["message2"]))
        self.assertEqual("No entries found", str(objects["message3"]))
        self.assertEqual("12 entries deleted", str(objects["message4"]))
        self.assertEqual("Successfully written", str(objects["message5"]))
        self.assertRaises(AttributeError, str, objects["wrong_message_4"])
        self.assertRaises(TypeError, StatusMessage)


class ProvideOutputTest(TestCase):

    def setUp(self):
        objects["contents"] = ["a", "b", "c"]

    def test_make_column_output(self):
        columns = [5, 5, 5]
        result = ProvideOutput.make_column_output(objects["contents"], columns)
        self.assertEqual("a    |b    |c    ", result)
    
    def test_make_bad_answer_message(self):
        result = ProvideOutput.make_bad_answer_message(*objects["contents"])
        right = "Cannot recognize your answer. Please, type only a, b or c."
        self.assertEqual(right, result)
    
    def test_make_input_check(self):
        ...
