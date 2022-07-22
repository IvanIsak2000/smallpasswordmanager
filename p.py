from argparse import ArgumentParser
from sys import exit

parser = ArgumentParser(prog='p%^m%^',
        description='you-know-what saver',
        epilog='используйте на свой страх и риск, анонимусы')
# modes: read r, append a, delete d
parser.add_argument('mode', nargs='?', default='r') 
mode = parser.parse_args().mode
"""service&site | login | password"""
stream = open('p.txt', 'r')
file = list(map(lambda x: x.rstrip(), stream.readlines()))
print('p.txt opened successfully')
longest = [0, 0, 0]
for line in file[0:-1]:
    if line[0] == '#':
        continue
    for j, k in enumerate(line.split('%^')):
        if len(k) > longest[j]:
            longest[j] = len(k)
print(len(file), 'entries in file')
if mode == 'r':
    print("SERVICE".center(longest[0]) + '|' + 
            "LOGIN".center(longest[1]) + '|' + 
            "PASSWORD".center(longest[2]))
    for line in file:
        if line[0] == '#':
            print(''.center(sum(longest), '-'))
            print(line.capitalize())
        else:
            temp = line.split('%^')
            print(temp[0].ljust(longest[0]) + '|' + 
                    temp[1].ljust(longest[1]) + '|' + 
                    temp[2].ljust(longest[2]))
    stream.close()
    exit()
elif mode == 'a':
    stream.close()
    ask = False
    while not ask:
        _serv = input('Service name (or names, splitted by "_"): ')
        _login = input('Login: ')
        _pwd = input('Password: ')
        question = input(f'Is it right:\n\
Service: {_serv}\n\
Login: {_login}\n\
Password:{_pwd}\n?: [y/n/abort]')
        if question == 'y':
            ask = True 
        elif question == 'abort':
            print('Ok, exiting then...')
            exit()
        else:
            print('Ok, once again...')
    with open('p.txt', 'a') as stream:
        pwd_entry = "%^".join([_serv, _login, _pwd]) + '\n'
        stream.write(pwd_entry)
    print('Successfully written to file')
    exit()
elif mode == 'd':
    ask = input("Which service's entry you'd like to delete? ")
    for_saving = []
    done = False
    for line in file:
        temp = line.split('%^')
        if temp[0] != ask or done is True or line[0] == '#':
            for_saving += [line]
        else:
            confirmation = input(f'are you sure to delete\n\
{temp[0].ljust(longest[0])}|{temp[1].ljust(longest[1])}|{temp[2].ljust(longest[2])}\n\
? [y/n]')
            if confirmation == 'n':
                continue
            elif confirmation == 'y':
                done = True
                continue
    stream.close()
    if not done:
        print('No entries found.\nAborting')
        exit()
    with open('p.txt', 'w') as stream:
        stream.write("\n".join(for_saving))
    print('Successfully deleted')
    exit()

