import handler_address_book
import handler_note_book
from parser import parser, parser_notebook
from sort import sort


def main():
    while True:
        job = input('Выбирете с чем работаем: addressbook (введите: 1), notebook (введите: 2),\n'
                    'сортировка файлов в папке (введите: 3), сортировка файлов в папке (введите: 4): \n>>> ')

        if job == '1':
            while True:
                command = input('Введите название комманды и параметры: ')
                if parser(command) in ['exit', 'close', 'good bye']:
                    print('До новых встреч в адрессной книге')
                    break
                print(handler_address_book.handler(command))
            continue

        elif job == '2':
            while True:
                command = input('Введите название комманды и параметры: ')
                if parser_notebook(command) in ['exit', 'close', 'good bye']:
                    print('До новых встреч в заметках')
                    break
                print(handler_note_book.handler(command))
            continue

        elif job == '3':
            path = input(
                'Укажите путь к папке, которую нужно отсортировать: ')
            if parser(path) in ['exit', 'close', 'good bye']:
                print('До новых встреч в сортировке')
                break
            print(sort(path))
            continue

        elif job == '4':
            print('До новых встреч')
            break

        else:
            print('Введите команду из предложеных')


if __name__ == "__main__":
    main()
