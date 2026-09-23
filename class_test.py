class Cat():
    #an attempt to model a cat
    def __init__(self, name, age):
        #assign the cats name and age
        self.name = name
        self.age = age

    def sleep(self):
        #The cat can sleep
        print(f"{self.name} is fast asleep like a little angel")

    def climb(self):
        #The cat can sleep
        print(f"Quick! {self.name} is climbing on the roof!")

my_cat = Cat('Weasley', 1)

my_second_cat = Cat('Noche', 3)

my_cat.sleep()

my_second_cat.climb()