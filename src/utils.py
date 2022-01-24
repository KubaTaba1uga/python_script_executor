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


def waiting_termination_continue_input(
    waiting_str: str, waiting_period: int, termination_str: str, continue_str: str
) -> str:
    """Ask user to wait/terminate script/continue to next script or
    if any of those are not specified takes input"""

    print(
        "\n"
        + f'Type "{termination_str}" to terminate script '
        + f'"{waiting_str}" to wait {waiting_period}s'
        + f' "{continue_str}" to skip to next script'
        + "or anythig else to pass input to script.",
        end="\n" * 2,
    )

    result = input(f"[{termination_str}/{waiting_str}/{continue_str}/...]?  ")

    print()

    return result
