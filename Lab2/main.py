
from serializer_lib.serialization.serializer import Serializer

class Aboba:
    name = "zalupa"
    count = 34.5

    def aboba_print(self):
        print(self.name)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    d = {5 : 5, 6 : "dfd", "sf" : 45.3}
    s = Serializer()

    print(s.serialize(print_hi))
    #print(s.deserialize(s.serialize(d)))


