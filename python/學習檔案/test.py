import functools


def demo(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        '''
        這是一個列印函式名稱的裝飾器
        '''
        print(f"function name is {f.__name__}.")
        print(f"{f.__doc__}")
        return f(*args, **kwargs)
    return wrapper


class Students:
    def __init__(self, age, name, grade):
        self.age = age
        self.name = name
        self.grade = grade


    def say_hi(self, name):
        print(f"Hi, my name is {name}.")   


    @demo
    def say_age(self):
        '''
        this is the function of Student's age
        '''
        print(f"I am {self.age} years old.")


if __name__ == "__main__":
    stu1 = Students(10, "Gary", 1)
    stu1.say_age()


