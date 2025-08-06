#已經實例化物件後，但是想改動整個類別的屬性，或是你單純想改動整個類別的屬性
class Student:
    course = 'Programming'

    def __init__(self, name, age, sex):
          self.name = name
          self.age = age
          self.sex = sex

    @classmethod
    def change_course(cls, new_course):
        cls.course = new_course

stu_1 = Student('Gary', 23, 'man')
stu_2 = Student('Mary', 36, 'male')
stu_1.change_course('Chinese')
print(f"{stu_1.name} course is: {stu_1.course}")
print(f"{stu_2.name} course is: {stu_2.course}")
print(f"course in Student is: {Student.course}")