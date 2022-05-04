import typing
from typing import Tuple, List


class Dictionary:
    def __init__(self, words):
        self.words = words

    @staticmethod
    def get_difference_value(
        len_of_word: int = 0, symbol_firstmilar_in_order: int = 0, len_diff: int = 0
    ) -> int:
        if len_diff < 0:
            len_diff = 0
        return len_of_word - symbol_firstmilar_in_order + len_diff

    @staticmethod
    def levenshtein_distance(first_str: str, second_str: str):
        len_second_str = len(second_str)

        row0 = range(len_second_str + 1)
        row1 = [0] * (len_second_str + 1)

        for index_first, symbol_first in enumerate(first_str):
            row1[0] = index_first + 1
            for index_second, symbol_second in enumerate(second_str):
                row1[index_second + 1] = min(
                    row0[index_second + 1] + 1,
                    row1[index_second] + 1,
                    row0[index_second] + (symbol_first != symbol_second),
                )

            row0 = row1.copy()

        return row0[len_second_str]

    def _get_symbol_firstmilars_letters(
        self, from_str: str, in_str: str
    ) -> Tuple[int, List[List[int]]]:
        counter = 0
        symbol_firstmilar_posymbol_firsttion_list = []
        for from_str_index in range(len(from_str)):
            ltr = from_str[from_str_index]
            if ltr in in_str:
                counter += 1
                index_in_str = in_str.index(ltr)
                symbol_firstmilar_posymbol_firsttion_list.append([from_str_index, index_in_str])
                # удаление сивола из искомой строки на случай, если он может повториться
                in_str = in_str[:index_in_str] + '*' + in_str[index_in_str + 1 :]

        return counter, symbol_firstmilar_posymbol_firsttion_list

    def _get_max_the_same_order(
        self, symbol_firstmilar_posymbol_firsttion_list: typing.List
    ) -> int:
        if len(symbol_firstmilar_posymbol_firsttion_list) == 0:
            return 0
        old_pos_diff = 0
        the_same_order_count = 0
        max_the_same_order_count = 1
        for term_index, word_index in symbol_firstmilar_posymbol_firsttion_list:
            pos_diff = word_index - term_index
            if pos_diff == old_pos_diff:
                the_same_order_count += 1
                if the_same_order_count > max_the_same_order_count:
                    max_the_same_order_count = the_same_order_count
            else:
                the_same_order_count = 1
            old_pos_diff = pos_diff

        return max_the_same_order_count

    def find_most_similar(self, term: str):
        difference_dict = {}
        for word in self.words:
            difference_dict[self.levenshtein_distance(word, term)] = word
        return difference_dict[min(difference_dict.keys())]
