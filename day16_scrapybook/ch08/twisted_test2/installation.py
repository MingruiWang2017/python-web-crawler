import time


def install_wordpress(customer):
    """派开发者安装软件，没安装一个需要3s"""
    print("Start installation for ", customer)
    time.sleep(3)
    print("All done for ", customer)


def timeit(func):
    def wapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        used_time = time.time() - start_time
        print("The func used %f seconds" % used_time)

    return wapper
