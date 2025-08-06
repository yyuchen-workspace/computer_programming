#已經實例化物件後，但是想改動整個類別的屬性，或是你單純想改動整個類別的屬性
class Student:
    course = 'Programming'

    def __init__(self, name, age, sex):
          self.name = name
          self.age = age
          self.sex = sex

    @staticmethod
    def is_weekend(day):
         if day.weekday() == 5 or day.weekday() == 6:
            return True
         return False
         
import datetime
print(datetime.datetime.now())
print(Student.is_weekend(datetime.datetime.now()))
