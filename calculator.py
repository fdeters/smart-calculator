import re
from string import ascii_letters


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
        self.variables = {}

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

            # variable declaration
            elif '=' in user_input:
                arguments = [s.strip() for s in user_input.split('=')]
                if len(arguments) != 2:
                    print('Invalid assignment')
                else:
                    if not self.is_valid_varname(arguments[0]):
                        print('Invalid identifier')
                    elif not self.is_declared_var(arguments[1]):
                        print('Invalid assignment')
                    else:
                        self.variables[arguments[0]] = arguments[1]

            # operations
            else:
                # collapse repeating operators
                expression = self.collapse(user_input)

                # plug in variables
                try:
                    expression = self.plug_and_chug(expression)
                except KeyError:
                    print('Unknown variable')
                else:

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

    def plug_and_chug(self, expression: str):
        """
        Accepts an expression collapsed by self.collapse() but not yet converted
        by self.sub_to_add(). Reads through the expression for variable names
        and plugs in appropriate values until the expression contains no Latin
        letters.
        """
        new_exp = expression
        has_letters = any(symbol in ascii_letters for symbol in new_exp)

        while has_letters:
            elements = new_exp.split()

            for i in range(len(elements)):
                if any(c in ascii_letters for c in elements[i]):
                    elements[i] = str(self.variables[elements[i]])

            new_exp = ' '.join(elements)
            has_letters = any(symbol in ascii_letters for symbol in new_exp)

        return new_exp

    def is_declared_var(self, name: str):
        """Checks to see whether a given variable has been declared.

        Also returns True if 'name' is an integer."""
        try:
            int(name)
        except ValueError:
            pass
        else:
            return True

        try:
            self.variables[name]
        except KeyError:
            return False
        else:
            return True

    @staticmethod
    def is_valid_varname(name: str):
        """True if the proposed variable name is valid (uses only Latin letters,
        False otherwise."""
        for c in name:
            if c not in ascii_letters:
                return False

        return True

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
        Ensures that expressions like '2 - -3' collapse to '2 + 3'.

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
