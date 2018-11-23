#fileName
class Student:
	count=0
	def __init__(self,name):
		self.name=name
		Student.count+=1
	@classmethod
	def show_count(cls):
		print(Student.count)

tom = Student("Tom")
Student.count=2
Student.show_count()
tom.count=3
tom.show_count()
tom.name="Tom Cat"
print(tom.name)

class Parent:
	__slots__=('name')
	def __init__(self,name):
		self.name=name
	def print_name(self):
		print(self.name)

class Child(Parent):
	__slots__=('name','age','sex')
	def __init__(self):
		super(Child,self).__init__("default Son")
child = Child()
child.print_name()
child.age=12


