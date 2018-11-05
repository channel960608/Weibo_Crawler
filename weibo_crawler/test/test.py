def yield_test(n):
    for j in range(n):
        yield call(j)
        print("j=",j)
    #做一些其它的事情
    print("do something.")
    print("end.")

def call(j):
    return j*2

#使用for循环
# for i in yield_test(5):
#     print(i,",")

def createGenerator():
    mylist = range(3)
    for i in mylist:
        yield i*i
    
mygenerator = createGenerator()
print(mygenerator)
for i in mygenerator:
    print(i)