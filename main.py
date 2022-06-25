from handler import open_and_save_file
from parser import parser, get_handler


def main():
    open_and_save_file(0)
    exit_words = ["good bye", "close", "exit", '.']
    kort = None  # будующий кортеж где первый эллемент - команда, воторой - данные
    while True:
        command = input("Введите команду: ")
        if command.lower() in exit_words:
            print("Bye")
            break
        kort = parser(command)
        if kort is None:
            print(f"Команды {command} не найдено")
            continue
        handler = get_handler(kort[0])
        print(handler(kort[1]))
    open_and_save_file(1)



if __name__ == "__main__":
    main()
