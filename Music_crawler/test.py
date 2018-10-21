class student:
    def __init__(self):
        self.__age = 15
    def change(self, age):
        self.__age = age
    def __str__(self):
        return "{}".format(self.__age)


if __name__=="__main__":
    s = student()
    print(s)
    s.change(30)
    print(s)
    s.change(40)
    print(s)