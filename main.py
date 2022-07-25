from sys import exit
from argparse import ArgumentParser


separator = "%^"
yesno = ('y', 'n')


def make_column_output(line: list, first: int, second: int, third: int) -> str:
    result = line[0].ljust(first) + '|'
    result += line[1].ljust(second) + '|'
    result += line[2].ljust(third)
    return result


def make_bad_answer_message(*variants) -> str:
    message = 'Cannot recognize your answer. Please, type only '
    varstring = ", ".join(variants)
    varstring = " or ".join(varstring.rsplit(", ", 1))
    message += varstring + '.'
    return message


def get_pure_contents(filestream) -> list:
    return list(map(lambda x: x.rstrip(), filestream.readlines()))


def check_mistake_question(service: str, login: str, password: str) -> str:
    message = 'Is it right:\n'
    message += "Service: " + service + "\n"
    message += "Login: " + login + "\n"
    message += "Password: " + password + "?\n"
    message += "[y/n/abort]')"
    answer = input(message)
    return answer

def main():
    parser = ArgumentParser(prog='SPM', description='small password manager', epilog='Use at your own risk')
    parser.add_argument('storagefile', nargs='?', default='p.txt')
    parser.add_argument('mode', nargs='?', default='r')
    args = parser.parse_args()
    param_mode, param_filename = args.mode, args.storagefile
    try:
        with open(param_filename, "r") as stream:
            contents = get_pure_contents(stream)
            longest = [0, 0, 0]
            for line in contents[0:-1]:
                for j, k in enumerate(line.split('%^')):
                    if len(k) > longest[j]:
                        longest[j] = len(k)
            print(param_filename, "with", len(contents), "entries is opened")
    except FileNotFoundError:
        print('There is no file with name', param_filename)
        exit()
    if param_mode == 'r':
        with open(param_filename, "r") as stream:
            contents = get_pure_contents(stream)
            print(make_column_output("SERVICE%^LOGIN%^PASSWORD", *longest))
            for line in contents:
                line = line.split("%^")
                print(make_column_output(line, *longest))
    elif param_mode == 'a':
        ask = False
        while not ask:
            _serv = input('Service name (or names, splitted by "_"): ')
            _login = input('Login: ')
            _pwd = input('Password: ')
            question = check_mistake_question(_serv, _login, _pwd)
            while question not in ('y', 'n', 'abort'):
                print(make_bad_answer_message(list(yesno) + ['abort']))
                question = check_mistake_question(_serv, _login, _pwd)
            if question == 'y':
                ask = True
            elif question == 'n':
                print('Ok, once again...')
            elif question == 'abort':
                print('Ok, exiting then...')
        with open('p.txt', 'a') as stream:
            pwd_entry = "%^".join([_serv, _login, _pwd]) + '\n'
            stream.write(pwd_entry)
            print('Successfully written to file')
    elif param_mode == 'd':
        message = "Which entries you'd like to delete?\n"
        message += "Type services' names: "
        servicenames = input(message).split()
        for_saving = []
        deleted = 0
        with open(param_filename, "r") as stream:
            file = stream.readlines()
            for line in file:
                temp = line.rstrip().split('%^')
                if (temp[0] not in servicenames) or (line[0] == '#'):
                    for_saving += [line]
                else:
                    print('Are you sure to delete')
                    print(make_column_output(temp, *longest))
                    confirmation = input("? [y/n] ")
                    while confirmation not in yesno:
                        print(make_bad_answer_message(yesno))
                        print('Are you sure to delete')
                        print(make_column_output(temp, *longest))
                        confirmation = input("? [y/n] ")
                    if confirmation == 'n':
                        for_saving += [line]
                    elif confirmation == 'y':
                        deleted += 1
        if deleted == 0:
            print('No entries found.\nAborting')
        else:
            with open('p.txt', 'w') as stream:
                stream.write("\n".join(for_saving))
            print('Successfully deleted')


if __name__ == "__main__":
    main()
 
