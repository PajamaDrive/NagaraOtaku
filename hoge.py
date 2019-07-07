
from multiprocessing import Process
from time import sleep
import time
# メインプロセスで動かす関数
def func_1(num):
    print('メインプロセスStart')
    for i in range(num):
        print('メインプロセス:', i)
        sleep(1)
    print('メインプロセスEnd')

# サブプロセスで動かす関数
def func_2(num):
    print('サブプロセスStart')
    for i in range(num):
        print('サブプロセス:', i)
        sleep(0.5)
    print('サブプロセスEnd')


if __name__ == '__main__':
    start = time.time()
    p = Process(target=func_2, args=(10,))
    p.start()

    func_1(10)
    print(time.time() - start)

    start = time.time()

    func_1(10)
    func_2(10)
    print(time.time() - start)
