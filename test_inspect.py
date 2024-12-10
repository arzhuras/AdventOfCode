import inspect


def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]


# print(retrieve_name(y))


def foo(bar):
    print(retrieve_name(bar), bar)
    return


def showVar(*vars):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    print(type(callers_local_vars))
    print(type(vars), vars)
    for var_name, var_val in callers_local_vars:
        print("->", var_name, var_val, id(var_val))
        for var in vars:
            if var_val is var:
                print(f"@ {var_name}: {var_val}")
    # print([var_name for var_name, var_val in callers_local_vars if var_val is var],var)

    # for var in vars:


# print(retrieve_name(zebask), zebask)
# foo(zebask)

x, y, z = 1, 2, 3

zebask = "azerty"
zebask2 = zebask
zebask3 = "azerty"

toto = "sdf"

showVar(zebask, zebask2, zebask3, x, y, z)

myvar = "karthikeyan"
print(f"{myvar=}")

"""
def fonction(**kwargs):
    for key,value in kwargs.items():
        print('{} -> {}'.format(key,value))

fonction(a = 1, b = 2, c = 5, zebask = "")
"""
"""
nom = "karthikeyan"
    print(f"{nom=}")
"""
