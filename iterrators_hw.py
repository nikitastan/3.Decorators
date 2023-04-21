import types
from decorator import logger2

# 1. Должен получиться итератор, который принимает список списков
# и возвращает их плоское представление,
# т. е. последовательность, состоящую из вложенных элементов.
class FlatIterator:
    @logger2('logs/FlatIterator')
    def __init__(self, list_of_list):
        self.new_list = list_of_list
        self.__index = 0
        self.__second_index = 0

    def __iter__(self):
        self.__index = 0
        self.__second_index = 0
        return self

    def __next__(self):
        if self.__second_index == len(self.new_list[self.__index]):
            self.__index += 1
            if self.__index >= len(self.new_list):
                raise StopIteration
            self.__second_index = 0
        item = self.new_list[self.__index][self.__second_index]
        self.__second_index += 1
        return item

# 2. Должен получиться генератор, который принимает
# список списков и возвращает их плоское представление.
@logger2('logs/flat_generator')
def flat_generator(list_of_lists):
    for list_ in list_of_lists:
        for item in list_:
            yield item

# 3.* Необязательное задание.
# Написать итератор, аналогичный итератору из задания 1,
# но обрабатывающий списки с любым уровнем вложенности.
class FlatIterator2:

    @logger2('logs/FlatIterator2')
    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.__index = 0

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index == len(self.list_of_list):
            raise StopIteration
        while isinstance(self.list_of_list[self.__index], list):
            if self.list_of_list[self.__index] == []:
                del self.list_of_list[self.__index]
                if self.__index == len(self.list_of_list):
                    raise StopIteration
            else:
                if self.__index != len(self.list_of_list)-1:
                    self.list_of_list = self.list_of_list[:self.__index] + self.list_of_list[self.__index] + self.list_of_list[self.__index+1:]
                else:
                    self.list_of_list = self.list_of_list[:self.__index] + self.list_of_list[self.__index]
        item = self.list_of_list[self.__index]
        self.__index += 1
        return item


# 4. 4.* Необязательное задание.
# Написать генератор, аналогичный генератору из задания 2,
# но обрабатывающий списки с любым уровнем вложенности.
@logger2('logs/flat_generator2')
def flat_generator2(main_list):
    for main_item in main_list:
        if isinstance(main_item, list):
            for sub_item in flat_generator2(main_item):
                yield sub_item
        else:
            yield main_item


def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator2(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator2(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


def test_4():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator2(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator2(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator2(list_of_lists_2), types.GeneratorType)


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()
