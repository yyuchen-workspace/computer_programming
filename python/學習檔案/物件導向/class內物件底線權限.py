class Student:
    course = 'Programming'

    def __init__(self, name, age):
          self.name = name
          self.age = age
          self._protect_var = 10
          self.__private_var = 100
    
    def prints(self):
         print(f"self.__private_var = {self.__private_var}")
    
    def test(self, var):
        self.__private_var = var
        print(f"{self.__private_var}")


stu_1  = Student('Gary', 23)

print(f"_protect_var = {stu_1._protect_var}")
#print(stu_1.__private_var) #在class外面訪問會error
stu_1.prints() 
stu_1.test(50)
print(f"__private_var out of class : {stu_1._Student__private_var}")