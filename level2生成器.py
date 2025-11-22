import time
start=time.time()

def fei():
    a=0
    b=1
    temp=0
    while True:
        yield a
        temp=a
        a=b
        b=b+temp
gen=fei()

f10=[next(gen) for i in range(1000000)]
print("end")

end=time.time()
time=end-start
print(f"{time}")

    