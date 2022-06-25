def input_error(func):
    def inner(sentence: str):
        try:
            result = func(sentence)
        except IndexError:
            return "Вы ввели не полные данные"
        except TypeError:
            return "Вы ввели что-то лишнее"
        except KeyError:
            return "Вы ввели не полные данные. Попробуйте снова"
        except StopIteration:
            return "Столько контактов нет"
        except ValueError:
            return 'Вы ввели неверные данные'
        except AttributeError:
            return 'Это не номер'
        return result
    return inner
