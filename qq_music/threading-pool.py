'''
python 线程池
使用submit和map来调用函数
'''


from concurrent.futures import ThreadPoolExecutor
import time

def sayhello(a):
    print('hello'+a)
    time.sleep(2)

def main():
    seed = ['a','b','c','f','e']
    start = time.time()
    for i in seed:
        sayhello(i)
    end = time.time()
    print('time'+str(end-start))
    start2 = time.time()
    with ThreadPoolExecutor(3) as executor:
        for each in seed:
            executor.submit(sayhello, each)
    end2 = time.time()
    print("time2: " + str(end2 - start2))
    start3 = time.time()
    with ThreadPoolExecutor(3) as executor1:
        executor1.map(sayhello, seed)
    end3 = time.time()
    print("time3: " + str(end3 - start3))


if __name__ == '__main__':
    main()