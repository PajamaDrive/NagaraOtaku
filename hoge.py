
from multiprocessing import Process
from time import sleep

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
    p = Process(target=func_2, args=(10,))
    p.start()
    func_1(10)
