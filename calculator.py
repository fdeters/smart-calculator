class Calculator:
    commands = {
        'help': 'This application reads a one-line expression and outputs the '
                'result.\n'
                'Recognizes the + and - operators and integer numbers (both '
                'positive and negative).\n'
                'Please separate numbers from operators using at least one '
                'space.'
    }

    def __init__(self):
        pass

    def run(self):
        """Main application loop for the smart calculator."""
        while True:
            user_input = input().strip()

            # commands
            if len(user_input) == 0:
                continue
            elif user_input == '/exit':
                print('Bye!')
                break
            elif user_input[1:] in self.commands:
                print(self.commands[user_input[1:]])
                continue

            # operations
            else:
                clean_expression = self.clean_input(user_input)
                print(self.evaluate(clean_expression))

    def evaluate(self, expression: str):
        """
        Takes a cleaned expression and evaluates it.
        Currently supports only addition and subtraction.

        :param expression: A clean string expression with no subtraction.
        :return: (int) The result of the evaluation.
        """
        # first, convert all subtraction to the addition of negative numbers
        addition_problem = self.sub_to_add(expression)

        # then, split up the terms and add them
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
        numbers:

        Ex: '-4+13-9' --> '-4+13+-9'

        :param expression: An expression cleaned via self.clean_input.
        :return: (str) Expression with subtraction converted to negative
            numbers.
        """
        if expression[0] == '-':
            lst = expression[1:].split('-')
            string_to_evaluate = '-' + '+-'.join(lst)
        else:
            lst = expression.split('-')
            string_to_evaluate = '+-'.join(lst)

        return string_to_evaluate

    @staticmethod
    def clean_input(expression: str):
        """
        "Cleans" an input expression by collapsing repeated operators (e.g '+++'
        becomes '+', '---' becomes '-', and '--' becomes '+'.
        Ensures that expressions like '2 - -3' collapse to '2+3'.

        :param expression: Raw user-input expression.
        :return: (str) Cleaned expression—no repeating operators and no spaces
            between elements.
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

        return ''.join(symbols)


if __name__ == '__main__':
    my_calculator = Calculator()
    my_calculator.run()
