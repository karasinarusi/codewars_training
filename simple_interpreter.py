import re
import operator

import typing


def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]


class TestFailed(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


def invalid_identifier_exception(ident: str):
    return TestFailed(f'ERROR: Invalid identifier. No variable with name \'{ident}\' was found.')


def invalid_parenthesis_exception():
    return TestFailed(f'ERROR: No pair for symbol \'(\'.')


def no_operator_exception():
    return TestFailed(f'ERROR: There is no operator.')


def invalid_syntax_near_operator(index: int):
    return TestFailed(f'ERROR: Wrong syntax near operator on position {index}.')


def invalid_syntax_near(val: str):
    return TestFailed(f'ERROR: Wrong syntax near  {val}.')


class Interpreter:
    OPERATOR_PRECEDENCE = [
        ['*', '/', '%'],
        ['+', '-'],
        ['='],
    ]
    OPERATORS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '%': operator.mod,
    }

    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):
        tokens = tokenize(expression)
        if len(tokens) == 0:
            return ''
        self._validate_tokens(tokens)
        res = self._operate_by_levels(tokens)
        return res if type(res) == int else int(res[0])

    def _validate_tokens(self, tokens: typing.List) -> None:
        if len(tokens) > 1:
            has_operators = False
            for token in tokens:
                if self._check_is_operator(token):
                    has_operators = True
            if not has_operators:
                raise no_operator_exception()
        for index, token in enumerate(tokens):
            token_type = self._get_token_type(token)
            if index + 1 < len(tokens):
                next_token = tokens[index + 1]
                if token_type and token_type == self._get_token_type(next_token):
                    raise invalid_syntax_near(f'{token} {next_token}')

    def _check_is_operator(self, value: str) -> bool:
        all_operators = list(self.OPERATORS.keys()) + ['=']
        return True if value in all_operators else False

    def _check_is_digit(self, value: str) -> bool:
        return value.replace('-', '').replace('.', '').isdigit()

    def _check_is_var(self, value: str) -> bool:
        return (
            not self._check_is_digit(value)
            and not self._check_is_operator(value)
            and value not in ['(', ')']
        )

    def _get_token_type(self, token: str) -> typing.Optional[str]:
        type_checker_dict = {
            'operator': self._check_is_operator,
            'digit': self._check_is_digit,
            'var': self._check_is_var,
        }
        for type_name in type_checker_dict.keys():
            if type_checker_dict[type_name](token):
                return type_name

    def _run_operators(self, tokens: typing.List) -> int:
        for operators in self.OPERATOR_PRECEDENCE:
            tokens = self._operate_one_level(tokens, operators)
        return self._get_token_value(tokens[0])

    def _operate_by_levels(self, tokens: typing.List) -> typing.Union[typing.List, int]:
        left_parenthesis = '('
        right_parenthesis = ')'

        if left_parenthesis not in tokens and right_parenthesis not in tokens:
            return self._run_operators(tokens)
        else:
            meetings = 0
            left_parenthesis_index = 0
            right_parenthesis_index = 0
            for index, token in enumerate(tokens):
                old_meetings = meetings
                if token == left_parenthesis:
                    meetings += 1
                elif token == right_parenthesis:
                    meetings -= 1
                if old_meetings == 0 and meetings == 1:
                    left_parenthesis_index = index
                elif old_meetings == 1 and meetings == 0:
                    right_parenthesis_index = index
            if not meetings == 0:
                raise invalid_parenthesis_exception()
            res = []
            if not left_parenthesis_index == 0:
                res += tokens[:left_parenthesis_index]
            operated = self._operate_by_levels(
                tokens[left_parenthesis_index + 1 : right_parenthesis_index]
            )
            if type(operated) == int:
                res += [str(operated)]
            else:
                res += operated
            if right_parenthesis_index < len(tokens) - 1:
                res += tokens[right_parenthesis_index + 1 :]

            return (
                [str(self._run_operators(res))]
                if left_parenthesis not in tokens and right_parenthesis not in res
                else self._operate_by_levels(res)
            )

    def _operate_one_level(self, tokens: typing.List, operators: typing.List[str]) -> typing.List:
        operator_found = False
        for index, token in enumerate(tokens):
            if token in operators:
                operator_found = True
                try:
                    prev_token = tokens[index - 1]
                    next_token = tokens[index + 1]
                    if token == '=':
                        self.vars[prev_token] = next_token
                        return [next_token]
                    else:
                        tokens[index] = self._apply_operator(
                            token_before=self._get_token_value(prev_token),
                            op=token,
                            token_after=self._get_token_value(next_token),
                        )
                        tokens.pop(index - 1)
                        tokens.pop(index)
                        return self._operate_one_level(tokens, operators)
                except IndexError:
                    raise invalid_syntax_near_operator(index)
        if not operator_found:
            return tokens

    def _apply_operator(
        self, token_before: typing.Union[str, int], op: str, token_after: typing.Union[str, int]
    ) -> str:
        token_before, token_after = int(token_before), int(token_after)
        return str(self.OPERATORS[op](token_before, token_after))

    def _get_token_value(self, token: str) -> int:
        if self._check_is_digit(token):
            return int(token[: token.index('.')]) if '.' in token else int(token)
        else:
            return int(self._get_var_value(token))

    def _get_var_value(self, var: str) -> str:
        if var not in self.vars.keys():
            raise invalid_identifier_exception(var)
        return self.vars[var]
