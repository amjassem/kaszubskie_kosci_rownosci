class A:
    def __init__(self):
        self.a = 1
        self.b = 2


def func(**kwargs):
    print(kwargs)


a = A()
func(**a.__dict__)
print(hash((1, 2, 5)))
