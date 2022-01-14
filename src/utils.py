def xyz_required(question: str) -> bool:
    """Ask question until correct choice is not provided"""
    input_invalid = True
    while input_invalid:
        ask_for_input = input(question + " ([y]/n)" + " " * 2)
        if not bool(ask_for_input):
            ask_for_input = "y"
        if ask_for_input in (
            "y",
            "n",
        ):
            input_invalid = False
        else:
            print("Input invalid!!!")

    return ask_for_input == "y"


def is_termination_required() -> bool:
    return xyz_required("Would You like to terminate script execution?")
