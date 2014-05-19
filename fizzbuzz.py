
def output(n):
    return ('fizz' if not n%3 else '') + ('buzz' if not n%5 else '') + (str(n) if (n%3 and n%5) else '')

def fizzbuzz(x):
    for i in range(x):
        print output(i)

def fizzbuzz(x, n=1):
    if n > x:
        return
    print output(n)
    fizzbuzz(x, n+1)

fizzbuzz(20)



