#poolPrac.py
from multiprocessing import Pool
import time
def func(interval) :
    print(interval)
    time.sleep(interval)
    return interval
def caculate(func,args):
    return func(*args)
def plus (a,b) :
    return a+b
def minus (a,b) :
    return a-b


resultList=[]
def func_result(ret) :
    resultList.append(ret)
    print ('return :',ret)

TASKS=[ (plus,(i,10)) for i in range(10) ] + \
      [ (minus,(i,10)) for i in range(10)]
if __name__ == '__main__' :
        with Pool (processes=6) as pool :
            mul_res=[ pool.apply_async(caculate,f) for f in TASKS ]
            pool.close()
            pool.join()
        result = [ re.get() for re in mul_res]
        print (result)



        with Pool (processes=4) as pool :
            mult_res=[]
            for x in range(4):
                res=pool.apply_async(func,(x,),callback=func_result)
                mult_res.append(res)
            print ('is here')
            pool.close()
            pool.join()
        print (resultList)
       # print ([r.get(timeout=5) for r in mult_res])



'''

'''

