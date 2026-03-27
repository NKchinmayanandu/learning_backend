def gen():
    print("start")
    yield 5
    print("end")


g = gen()
next(g)
next(g)