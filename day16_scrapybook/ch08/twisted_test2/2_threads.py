import threading
import installation

"""多线程"""


@installation.timeit
def developer_day(customers):
    lock = threading.Lock()

    def dev_day(id):
        print("Good morning from developer ", id)
        lock.acquire()
        while customers:
            customer = customers.pop(0)
            lock.release()
            installation.install_wordpress(customer)
            lock.acquire()

        lock.release()
        print("Bye from developer ", id)

    devs = [threading.Thread(target=dev_day, args=(i,))
            for i in range(5)]  # 派5个开发者进行安装
    [dev.start() for dev in devs]
    [dev.join() for dev in devs]


developer_day(["Customer %d" % i for i in range(15)])

# 5位开发者同时为15位顾客安装，耗时9秒
