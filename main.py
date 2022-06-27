import handler_address_book
from parser import parser, parser_notebook


def main():
    while True:
        job = input('Выбирете с чем работаем: addressbook (введите: 1), notebook (введите: 2),'
                    'сортировка файлов в папке (введите: 3): \n>>> ')

        if job == '1':
            while True:
                command = input('Введите название комманды и параметры: ')
                if parser(command) in ['exit', 'close', 'good bye']:
                    print('До новых встреч')
                    break
                print(handler_address_book.handler(command))
            break

        elif job == '2':
            while True:
                command = input('Введите название комманды и параметры: ')
                if parser_notebook(command) in ['exit', 'close', 'good bye']:
                    print('До новых встреч')
                    break
                #print(handler_solver.handler(command))
            break

        elif job == '3':
            # Тут будет сортировка файлов
            break

        else:
            print('Введите команду из предложеных')

if __name__ == "__main__":
    main()
