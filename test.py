def doggy(n):
    print("hey")
    for i in range(n):
        yield f"{i}I am a dog"


print(type(doggy))
dg = doggy(5)
print(next(dg))
print(next(dg))
print(next(dg))
print(next(dg))
print(next(dg))
print(next(dg))
print(type(dg))
