from handler import handler
from parser import parser


def main():
    job = int(input('Выбирете с чем работаем: addressbook (введите: 1), notebook (введите: 2): \n>>> '))

    if job == 1:
        while True:
            command = input('Введите название комманды и параметры: ')
            if parser(command) in ['exit', 'close', 'good bye']:
                print('До новых встреч')
                break
            print(handler(command))

    if job == 2:
        #Тут будет ноутбук
        pass


if __name__ == "__main__":
    main()
