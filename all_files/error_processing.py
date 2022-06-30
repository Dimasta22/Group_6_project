def input_error(func):
    def inner(sentence: str):
        try:
            result = func(sentence)
        except IndexError:
            return "Incomplete data entered"
        except TypeError:
            return "Added something extra"
        except KeyError:
            return "Incomplete data entered"
        except StopIteration:
            return "Contact limit exceeded"
        except ValueError:
            return 'Invalid data entered'
        except AttributeError:
            return 'The entered data does not meet the requirements'
        return result
    return inner
