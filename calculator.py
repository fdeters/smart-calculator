class Calculator:
    commands = {
        'help': 'The program calculates the sum of numbers'
    }

    def __init__(self):
        pass

    def run(self):
        """Main application loop for the smart calculator."""
        while True:
            user_input = input().strip()

            # commands
            if user_input == '/exit':
                print('Bye!')
                break
            elif user_input[1:] in self.commands:
                print(self.commands[user_input[1:]])
                continue

            # operations
            else:
                # addition
                terms = [int(s) for s in user_input.split()]
                total = self.add(terms)
                if total is not None:
                    print(total)

    @staticmethod
    def add(terms: list):
        """
        Sums a list of integers and returns the total.

        :param terms: A list of integers to be summed.
        :return: (int) The sum. If no arguments are passed, returns None.
        """
        if len(terms) > 0:
            return sum(terms)
        else:
            return None


if __name__ == '__main__':
    my_calculator = Calculator()
    my_calculator.run()
