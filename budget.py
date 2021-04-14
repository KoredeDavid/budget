# This ensures that the figure inputted is valid
def clean_amount(action):
    invalid_amount = False
    while not invalid_amount:
        # This catches an error that is raised if the user inputs a str instead of an int or a float
        try:
            amount = int(input(f'\nHow much will you like to {action} Zuri? '))
        except ValueError:
            amount = None
        if amount:
            return amount
        else:
            print(f'\nPlease enter a valid amount, Zuri. Try Again.')


# This checks if the budget has sufficient funds to perform a withdrawal or a transfer.
def funds_validation(action, category, budget):
    insufficient_funds = False
    while not insufficient_funds:
        amount = clean_amount(action)
        # this checks if the amount inputted is > or < the user's account balance.
        if amount <= budget:
            insufficient_funds = True
            budget -= amount
            print(
                f'\nTake your cash Zuri. Your balance for {category} is now ${budget}' if action == 'withdraw' else '')
            return budget, amount
        else:
            print(f'\nInsufficient  funds, your current account balance is ${budget}. Try Again #kpk')


def perform_another_transaction_or_terminate():
    operations = [1, 2]

    operations_text = "\n1. Perform another transaction \n2. Terminate transaction\n"
    print(operations_text)

    operation_available = False
    while not operation_available:
        # This catches an error that is raised if the user inputs a str instead of an int
        try:
            operation = int(input(f'What will you like to do Zuri? '))
        except ValueError:
            operation = None

        # this checks if the selected operation is available
        if operation in operations:
            operation_available = True
            if operation == 1:
                transaction()
            if operation == 2:
                terminate()
        else:
            print(f'\nPlease select either of 1-2. Try Again \n{operations_text}')


def create_new_category():
    category = input('\nName of your new category? ').capitalize()
    balance = clean_amount('budget')
    new_category = Budget(category, balance)
    categories.append(new_category)
    print(f'\n{new_category.category} has been created and its budget is ${new_category.budget}')
    perform_another_transaction_or_terminate()


def terminate():
    exit('\nBye Zuri')


class Budget:
    def __init__(self, category, budget):
        self.category = category
        self.budget = budget

    def deposit(self):
        amount_to_deposit = clean_amount('deposit')
        self.budget += amount_to_deposit
        print(f'\nYour {self.category} budget has been credited with ${amount_to_deposit} and your mew account '
              f'balance is ${self.budget}')
        perform_another_transaction_or_terminate()

    def withdraw(self):
        self.budget, amount = funds_validation('withdraw', self.category, self.budget)
        perform_another_transaction_or_terminate()

    def balance(self):
        print(f'Your balance for {self.category} ${self.budget}')
        perform_another_transaction_or_terminate()

    def transfer(self):
        self.budget, amount_to_transfer = funds_validation('transfer', self.category, self.budget)
        categories.remove(self)
        operation_available = False
        while not operation_available:
            #
            for category in categories:
                print(f'{categories.index(category) + 1}.', category.category, f'${category.budget}')
            try:
                # This catches an error that is raised if the user inputs a str instead of an int
                category = int(input(f'\nWhat category will you like to transfer your {self.category} budget to? '))
                # This raises an error if the user input is greater than the list index +1 of the categories
                # available or if the input is 0
                if category > len(categories) or category == 0:
                    raise ValueError
            except ValueError:
                print('\nPlease select a valid response')
                continue

            # this checks if the selected operation is available and calls the appropriate function
            # assigned to it
            if categories[category - 1] in categories:
                operation_available = True
                category = categories[category - 1]
                category.budget = category.budget + amount_to_transfer
                categories.append(self)
                print(
                    f'${amount_to_transfer} has been transferred to {category.category}, your {self.category} budget '
                    f'is now ${self.budget}  ')
                perform_another_transaction_or_terminate()
            else:
                print(f'\nPlease select either of the numbers listed. Try Again')


# It create instances for the Budget classes and the objects are saved in the list named categories
categories = [Budget('Data', 10000), Budget('Clubbing', 20000)]


def transaction():
    operation_available = False
    while not operation_available:
        operations = [1, 2, 3, 4]

        # This prints all the available categories
        for category in categories:
            print(f'{categories.index(category) + 1}.', category.category, f'${category.budget}')

        # create_new and cancel variables are used to access the create_new_category() and terminate()
        create_new = int(len(categories)) + 1
        cancel = int(len(categories)) + 2
        print(f'{create_new}. Create a new category \n{cancel}. Terminate ')

        # This catches an error that is raised if the user inputs a str instead of an int
        try:
            category = int(input(f'\nWhat budget category will you like to access or what other activity do you want '
                                 f'to perform ({create_new}&{cancel}) boss? '))

            # This raises an error if the user input is greater than the list index +1 of the categories
            # available or if the input is 0
            if category > cancel or category == 0:
                raise ValueError
        except ValueError:
            print('\nPlease select a valid response')
            continue

        # Once the user input for which transaction or category it then gives them further options based on what chose
        try:
            if categories[category - 1] in categories:
                operation_available = True

                def what_transaction_to_perform(category_obj):
                    selected_transaction_available = False

                    while not selected_transaction_available:
                        print("\n1. Withdraw \n2. Transfer \n3. Balance \n4. Deposit")
                        try:
                            selected_transaction = int(
                                input(f'\nWhat will you like todo to your {category_obj.category} budget boss? '))
                        except ValueError:
                            selected_transaction = None
                        if selected_transaction == 1:
                            category_obj.withdraw()
                        if selected_transaction == 2:
                            category_obj.transfer()
                        if selected_transaction == 3:
                            category_obj.balance()
                        if selected_transaction == 4:
                            category_obj.deposit()
                        if selected_transaction in operations:
                            selected_transaction_available = True
                        else:
                            print('Please select a valid response boss')

                what_transaction_to_perform(categories[category - 1])
        except IndexError:
            if category == create_new:
                create_new_category()
            elif category == cancel:
                terminate()
            else:
                print(f'\nPlease select either of the numbers listed. Try Again ')


transaction()