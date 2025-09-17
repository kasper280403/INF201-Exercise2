import sys

def get_int(message, a, b, allow_empty=False):
    if a is None:
        a_temp = "<-"
        a = -999
    else:
        a_temp = int(a)

    if b is None:
        b_temp = "->"
        b = 999
    else:
        b_temp = int(b)

    while True:
        user_input = input(message + f"(type a number [{a_temp}, {b_temp}]): ")

        if user_input.lower() == "q" or user_input.lower() == "quit" or user_input.lower() == "exit" or user_input.lower() == "esc":
            print("Program terminated...")
            sys.exit()
        elif user_input.lower() == "" and allow_empty:
            return None

        try :
            user_input = int(user_input)
            if a <= user_input <= b:
                return user_input
            else:
                print("Number out of range, please try again.")
        except ValueError:
            print("Invalid input, please type a number.")
