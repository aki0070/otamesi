class Student:
    def __init__(self,name, math, japanese,
                  english, science, society):
        self.name = name
        self.math = math
        self.japanese = japanese
        self.english = english
        self.science = science
        self.society = society
    def average_score(self):
        avg = (self.math + self.japanese +  self.english
                + self.science + self.society ) / 5
        return avg

student_1 = Student("斎藤相馬", 99, 85, 89, 99, 30)
s1_avg = student_1.average_score()
print(s1_avg)
