# do not set default value for `a`
def f(a, *args, **kwargs):
    print('a is ', a)
    print('args is ', args)
    print('kwargs is ', kwargs)

def f_wrapper(*args, **kwargs):
    f(3, args, kwargs)

command = ['cmd', 'param1', 'param2']
f_wrapper(command)

f(1, 2, 3, 4)  # same as a=1, args=2,3,4

# SyntaxError: non-keyword arg after keyword arg
# fun(a=4, 1, 2, 3, 4)
