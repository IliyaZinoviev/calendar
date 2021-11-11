"""
    Этот модуль содержит фабрику генераторов, предназначенных для распределения целого числа "равномерно" по, например,
        последовательности целых чисел.
"""
from dataclasses import dataclass
from typing import Callable
from itertools import repeat


@dataclass
class Part:
    count: int
    interval: list[int]

    def __add__(self, part):
        if len(part.interval) > len(self.interval):
            fst_part = part
            snd_part = self
        else:
            fst_part = self
            snd_part = part
        fst_interval = fst_part.interval
        fst_part.interval = snd_part.interval + fst_interval
        snd_count = snd_part.count
        if fst_part.count > snd_part.count:
            snd_part.count = fst_part.count - snd_count
            fst_part.count = snd_count
            snd_part.interval = fst_interval
        else:
            snd_part.count = snd_count - fst_part.count
        part = snd_part
        return fst_part


def less_length_dist_gen(number: int, length: int) -> int:
    length_quotient = length // number
    length_remainder = length % number
    base_interval = list(repeat(0, length_quotient - 1)) + [1]
    if length_remainder == 0:
        for _ in range(number):
            for val in base_interval:
                yield val
    else:  # length_remainder > 0
        part = Part(number, base_interval)
        part_ = Part(length_remainder, [0])
        while part_.count > 0:
            part += part_
        for _ in range(part.count):
            for val in part.interval:
                yield val


def more_length_dist_gen(number: int, length: int) -> int:
    number_quotient = number // length
    number_remainder = number % length
    gen = less_length_dist_gen(length, number_remainder)
    for _ in range(length):
        yield number_quotient + next(gen)


class IntDistGenFactory:
    """
        Integer Distribution Generator Factory. Фабрика генераторов распределения целого числа.
    """
    @staticmethod
    def get_int_dist_gen(number: int, length: int) -> Callable[[], int]:
        """
            Метод строит генератор "равномерного" распределения целого числа number по длине length некоторой
            последовательности.
            На каждый вызов генератор будет "равномерно" возвращать целую часть от number. Генератор заканчивает свою
            работу через length вызовов. К последнему вызову сумма возвращённых генератором целых чисел становится равна
            целому числу number. Общее описание работы генератора раскрывает значение слова "равномерный"
            Общее описание работы генератора:
                1. Как равномерно распределить number между length кол-ом элементов?
                3. Для этого делим number на length и получаем n_q частное и n_r остаток .
                2. К каждому элементу из последовательности длины length добавляем частное n_q.
                Что делать с остатком n_r?
                3. Равномерно распределить n_r остаток по единичке между length частями. Как?
                4. Для начала делим length на n_r остаток, чтобы получить n_r интервалов равных l_q частному и l_r
                остатку. Что делать с l_r остатком и l_q частным?
                5. Считать, что все интервалы равны l_q частному,
                а что происходит с l_r смотреть в less_length_dist_gen.
        """
        if number > length:
            res = more_length_dist_gen(number, length)
        elif number == length:
            res = less_length_dist_gen(number, 0)
        else:  # rest_days < interval_count
            res = less_length_dist_gen(number, length)
        return res
