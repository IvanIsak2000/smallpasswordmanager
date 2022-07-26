from sys import exit
#  from dataclasses import dataclass
from typing import Callable, Union, List
from argparse import ArgumentParser


old_exit_func = exit


def cute_exit(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        print("Exiting")
        old_exit_func(*args, **kwargs)
    return wrapper


exit = cute_exit(exit)


class Config:
    def __init__(self):
        self.yesno = {"y", "n", "abort"}
        self.separator = "%^"
        parser = ArgumentParser(
            prog="SPM",
            description="small password manager",
            epilog="Use at your own risk")
        parser.add_argument("mode", nargs="?", default="r")
        parser.add_argument("storagefile", nargs="?", default="p.txt")
        args = parser.parse_args()
        self.mode = args.mode
        self.filename = args.storagefile


class StorageFile:
    def __init__(self, file: str):
        self.filename = file
        contents = self.get_pure_contents()
        length = [0, 0, 0]
        for line in contents:
            for index, string in enumerate(line.split("%^")):
                current_len = len(string)
                if current_len > length[index]:
                    length[index] = current_len
        print(self.filename, "with", len(contents) - 1, "entries is opened")
        self.column_length = length
    
    def get_pure_contents(self) -> list:
        with open(self.filename, mode="r", encoding="utf8") as stream:
            contents = list(map(lambda x: x.rstrip(), stream.readlines()))
        return contents

    def save_new_buffer(self, new_stuff: list) -> None:
        with open(self.filename, mode="w", encoding="utf8") as stream:
            text = "\n".join(new_stuff) + "\n"
            stream.write(text)
        print(StatusMessage(event="written"))
    
    def append(self, new_line) -> None:
        if new_line[-1] != "\n":
            new_line += "\n"
        stream = open(self.filename, mode="a", encoding="utf8")
        stream.write(new_line)
        stream.close()
        
class StatusMessage:
    def __init__(self, event: str, value: int = None, error: Exception = None):
        self.event = event
        self.value = value
        self.error = error
    
    def __repr__(self) -> str:
        event = self.event
        if event == "written":
            return "Successfully written"
        elif event == "no_written":
            return f"Error occured when writing to file: {self.error}"
        elif event == "no_entries":
            return "No entries found"
        elif event == "entries_deleted":
            return f"{self.value} entries deleted"


class ProvideOutput:
    @staticmethod
    def make_column_output(line       : List[Union[str, str, str]],
                           col_lengths: List[Union[int, int, int]]) -> str:
        result = str()
        for column_content_index, column_len in zip(range(len(line)), col_lengths):
            result += line[column_content_index].ljust(column_len)
            if column_content_index != len(line) - 1:
                result += "|"
        return result

    @staticmethod
    def make_bad_answer_message(*variants) -> str:
        message = "Cannot recognize your answer. Please, type only "
        variant_string = ", ".join(variants)
        variant_string = " or ".join(variant_string.rsplit(", ", 1))
        message += variant_string + "."
        return message

    @staticmethod
    def make_input_check(service: str, login: str, password: str) -> str:
        message = "Is it right:\n"
        message += "Service: " + service + "\n"
        message += "Login: " + login + "\n"
        message += "Password: \"" + password + "\" ?\n"
        message += "[y/n/abort])"
        answer = input(message)
        return answer
    
    @staticmethod
    def encode_strings(args: list) -> list:
        for index in range(len(args)):
            args[index] = args[index].encode("utf8")
        return args



def main():
    config = Config()
    try:
        file = StorageFile(config.filename)
    except FileNotFoundError:
        print("No storagefile found")
        exit(1)
    contents = file.get_pure_contents()
    if config.mode == "r":
        header_list = "SERVICE%^LOGIN%^PASSWORD".split("%^")
        header = ProvideOutput.make_column_output(header_list, file.column_length)
        print(header)
        for line in contents:
            rendered_line = line.split("%^")
            print(ProvideOutput.make_column_output(rendered_line, file.column_length))
    elif config.mode == "a":
        while True:
            _serv = input("Service name (or names, splitted by _): ")
            _login = input("Login: ")
            _pwd = input("Password: ")
            form = [_serv, _login, _pwd]
            question = ProvideOutput.make_input_check(*form)
            while question not in config.yesno:
                print(ProvideOutput.make_bad_answer_message(*config.yesno))
                question = ProvideOutput.make_input_check(_serv, _login, _pwd)
            if question == "y":
                break
            elif question == "n":
                print("Ok, once again...")
            elif question == "abort":
                exit()
        try:
            file.append("%^".join(form))
            form = ProvideOutput.encode_strings(form)
            print(StatusMessage("written"))
        except FileNotFoundError as error:
            print(StatusMessage("no_written", error=error))
            exit(1)
    elif config.mode == "d":
        question = "Which entries you would like to delete?\n"
        question += "Type service names: "
        servicenames = input(question).split()
        saving_buffer = []
        deleted = 0
        for line in contents:
            temp = line.split("%^")
            if (temp[0] not in servicenames) or (line[0] == "#"):
                saving_buffer += [line]
            else:
                print("Are you sure to delete")
                print(ProvideOutput.make_column_output(temp, file.column_length))
                confirmation = input("? [y/n] ")
                while confirmation not in config.yesno:
                    print(ProvideOutput.make_bad_answer_message(config.yesno))
                    print("Are you sure to delete")
                    print(ProvideOutput.make_column_output(temp, file.longest))
                    confirmation = input("? [y/n] ")
                if confirmation == "n":
                    saving_buffer += [line]
                    print("Not deleted")
                elif confirmation == "y":
                    deleted += 1
        if deleted == 0:
            print(StatusMessage(event="no_entries"))
        else:
            file.save_new_buffer(saving_buffer)
            print(StatusMessage(event="entries_deleted", value=deleted))


if __name__ == "__main__":
    main()
    exit(0)
