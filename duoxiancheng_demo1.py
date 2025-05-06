import multiprocessing
import time


def sing(num: int):
    for i in range(num):
        print(f"sing{i + 1}")
        time.sleep(0.5)


def dance(num: int):
    for i in range(num):
        print(f"dance{i + 1}")
        time.sleep(0.5)


if __name__ == "__main__":
    sing_pro = multiprocessing.Process(target=sing, args=(3,))
    dance_pro = multiprocessing.Process(target=dance, kwargs={"num": 4})
    sing_pro.start()
    dance_pro.start()
