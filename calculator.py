import re


class Calculator:
    commands = {
        'help': 'This application reads a one-line expression and outputs the '
                'result.\n'
                'Recognizes the + and - operators and integer numbers (both '
                'positive and negative).\n'
                'Please separate numbers from operators using at least one '
                'space.'
    }
    expression_regex = r'[+-]?([0-9]+)( [+-] [0-9]+)*'

    def __init__(self):
        pass

    def run(self):
        """Main application loop for the smart calculator."""
        while True:
            user_input = input().strip()

            # blank input
            if len(user_input) == 0:
                continue

            # commands
            elif user_input.startswith('/'):
                try:
                    result = self.do_command(user_input[1:])
                    if result is None:  # exit command
                        print('Bye!')
                        break
                    else:
                        print(result)
                except KeyError:
                    print('Unknown command')

            # operations
            else:
                # collapse repeating operators
                expression = self.collapse(user_input)

                # check to be sure it matches regex
                if self.is_valid_expression(expression):

                    # convert subtraction to addition of negative numbers
                    addition_problem = self.sub_to_add(expression)

                    try:
                        result = self.evaluate(addition_problem)
                        print(result)
                    except ValueError:
                        print('Invalid expression (ValueError)')
                else:
                    print('Invalid expression')

    def do_command(self, command: str):
        """
        Returns the given command.
        Returns None if the command is 'exit'.
        """
        if command == 'exit':
            return None
        else:
            return self.commands[command]

    def is_valid_expression(self, expression: str):
        """
        To be used on an expression which has been collapsed, but still may have
        subtraction and spaces.

        :param expression: The given clean expression.
        :return: (bool) True if the expression matches the regex, False
            otherwise.
        """
        return re.fullmatch(self.expression_regex, expression)

    @staticmethod
    def evaluate(addition_problem: str):
        """
        Takes a cleaned expression and evaluates it.
        Currently supports only addition and subtraction.

        :param addition_problem: A clean string expression with no subtraction.
        :return: (int) The result of the evaluation.
        """
        # remove leading + if necessary
        if addition_problem[0] == '+':
            addition_problem = addition_problem[1:]

        # split up the terms and add them
        if addition_problem.find('+') != -1:  # isn't just one number
            terms = [int(x) for x in addition_problem.split('+')]
        else:
            terms = [int(addition_problem)]

        result = sum(terms)

        return result

    @staticmethod
    def sub_to_add(expression: str):
        """
        Converts all subtraction in an expression to the addition of negative
        numbers. Also removes spaces.

        Ex: '-4 + 13 - 9' --> '-4+13+-9'

        :param expression: An expression cleaned via self.clean_input.
        :return: (str) Expression with subtraction converted to negative
            numbers and spaces removed.
        """
        no_spaces = ''.join(expression.split())

        if no_spaces[0] == '-':
            lst = no_spaces[1:].split('-')
            s = '-' + '+-'.join(lst)
        else:
            lst = no_spaces.split('-')
            s = '+-'.join(lst)

        return s

    @staticmethod
    def collapse(expression: str):
        """
        "Cleans" an input expression by collapsing repeated operators (e.g '+++'
        becomes '+', '---' becomes '-', and '--' becomes '+'.
        Ensures that expressions like '2 - -3' collapse to '2+3'.

        :param expression: Raw user-input expression.
        :return: (str) Cleaned expression---no repeating operators, elements
            space-separated.
        """
        symbols = expression.split()
        for i in range(len(symbols)):

            # collapse repeated +
            if symbols[i].startswith('++'):
                symbols[i] = '+'

            # collapse repeated -
            elif symbols[i].startswith('--'):
                if len(symbols[i]) % 2 == 0:
                    symbols[i] = '+'
                else:
                    symbols[i] = '-'

        # collapse subtraction of negative numbers
        for i in range(len(symbols) - 1):
            if symbols[i] == '-' and symbols[i+1][0] == '-':
                symbols[i] = '+'
                symbols[i+1] = symbols[i+1][1:]

        return ' '.join(symbols)


if __name__ == '__main__':
    my_calculator = Calculator()
    my_calculator.run()
