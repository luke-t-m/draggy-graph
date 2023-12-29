



def consec_func(func1, func2):
    def func3(*args):
        func1(*args)
        func2(*args)
    return func3

