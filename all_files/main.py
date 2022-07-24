import handler_address_book
import handler_note_book
from parser import parser, parser_notebook
from sort import sort


def main():
    while True:
        job = input('Choose what we work with: addressbook (enter: 1), notebook (enter: 2),\n'
                    'sorting files in a folder (enter: 3), exit (enter: 4): \n>>> ')

        if job == '1':
            try:
                handler_address_book.handler('file read')
            except:
                pass
            while True:
                command = input('Enter command name and parameters: ')
                if parser(command) in ['exit', 'close', 'good bye']:
                    print('See you in the address book')
                    handler_address_book .handler('file write')
                    break
                print(handler_address_book .handler(command))
            continue

        elif job == '2':
            handler_note_book.handler('file read')
            while True:
                command = input('Enter command name and parameters: ')
                if parser_notebook(command) in ['exit', 'close', 'good bye']:
                    print('See you soon in notes')
                    handler_note_book.handler('file write')
                    break
                print(handler_note_book.handler(command))
            continue

        elif job == '3':
            path = input('Specify the path to the folder to be sorted: ')
            if parser(path) in ['exit', 'close', 'good bye']:
                print('See you in sorting')
                break
            print(sort(path))
            continue

        elif job == '4':
            print('See you soon!')
            break

        else:
            print('Enter a command from the list of suggested')


if __name__ == "__main__":
    main()
