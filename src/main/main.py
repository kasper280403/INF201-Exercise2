import resource_getter
import actions


def main():
    print("Program is running. Type q/Q to quit.\n")

    print("-----File reader-----")
    choice = "choose_file"
    file = "none"

    while True:
        if choice == "choose_file":
            file_list = resource_getter.print_res_list()
            file = resource_getter.choose_resource(file_list)
            choice = "perform_action"

        elif choice == "perform_action":
            print("\n---Perform an action---")
            actions.print_actions()
            actions.choose_action(file)

            choice = "choose_file"



if __name__ == "__main__":
    main()


