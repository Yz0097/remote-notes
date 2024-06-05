# 主文件

import sys
# from fruit import Pear  # 引入Pear类
from release.trace_function import enhanced_trace_calls_with_modules
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput


class Pear:
    def __init__(self):
        print("Pear: init")

    def eat(self):
        print("Pear: eat")

    def throw(self):
        print("Pear: throw")


class Apple:
    def __init__(self):
        print("Apple: init")

    def eat(self):
        print("Apple: eat_apple")

    def throw(self):
        print("Apple: throw")


class Banana:
    def __init__(self):
        print("Banana: init")

    def eat(self):
        print("Banana: eat")

    def throw(self):
        print("Banana: throw")


class Person:
    age = 0
    sex = 0
    bag = None

    def __init__(self, _age, _sex):
        self.age = _age
        self.sex = _sex
        self.bag_init()

    def bag_init(self):
        print("person: bag_init")
        self.bag = []

    def add_banana(self, banana):
        print("person: add_banana")
        self.bag.append(banana)

    def add_apple(self, apple):
        print("person: add_apple")
        self.bag.append(apple)

    def add_pear(self, pear):
        print("person: add_pear")
        self.bag.append(pear)

    def eat_bananas(self):
        # [fruit.eat() for fruit in self.bag if isinstance(fruit, Banana)]
        for fruit in self.bag:
            if isinstance(fruit, Banana):
                fruit.eat()
        self.bag_init()

    def eat_pears(self):
        # [fruit.eat() for fruit in self.bag if isinstance(fruit, Pear)]
        for fruit in self.bag:
            if isinstance(fruit, Pear):
                fruit.eat()
        self.bag_init()

    def set_age(self, _age):
        print("person: set_age")
        self.age = _age


def main():
    age = 4  # Simulating input for testing
    person = Person(age, 0)
    if person.age > 5:
        person.add_apple(Apple())
    person.add_pear(Pear())  # Adding a Pear to the scenario

    for _ in range(3):
        person.add_banana(Banana())
    person.eat_pears()
    person.eat_bananas()


if __name__ == '__main__':

    # graphviz_1 = GraphvizOutput(output_file='../release/test_d.gv', output_type='dot')
    # with PyCallGraph(output=graphviz_1):
    ignored_modules = {'re', 'subprocess', 'sre_compile', 'sre_parse', 'sre_constants', 'pycallgraph', 'os', 'argparse'}  # 忽略标准库和第三方库
    # ignored_modules = {}
    call_relations = []
    sys.settrace(lambda frame, event, arg: enhanced_trace_calls_with_modules(frame, event, arg, call_relations, ignored_modules))

    # graphviz_1 = GraphvizOutput(output_file='../release/test_d.gv', output_type='dot')
    # with PyCallGraph(output=graphviz_1):
    #     main()
    main()

    sys.settrace(None)
    # call_relations = filter_call_relations(call_relations)
    with open('../analysis/0325fly/test_func_calls.log', 'w') as file:
        for relation in call_relations:
            print(relation, file=file)
