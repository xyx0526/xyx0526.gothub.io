import time
start=time.time()

i=1
a=0
b=1
temp=0
while i<=1000000:
   
   temp=a
   a=b
   b=temp+b
   i+=1

end=time.time()
time=end-start
print(f"{time}")

    