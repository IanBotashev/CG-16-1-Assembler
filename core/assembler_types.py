POSSIBLE_INSTRUCTIONS = ["mov", "adc", "int"]


class Instruction:
    """
    Represents an instruction, such as MOV, LDA, ADC, etc.
    """
    def __init__(self, mnemonic, arguments=None):
        if arguments is None:
            arguments = []

        self.arguments = arguments
        self.mnemonic = mnemonic

    def check_if_valid_instruction(self):
        """
        Checks if the value of this instruction is in the POSSIBLE_INSTRUCTIONS list.
        :return:
        """
        return self.mnemonic in POSSIBLE_INSTRUCTIONS

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        equal_arguments = True
        if len(self.arguments) != len(other.arguments):
            equal_arguments = False

        else:
            for i in range(len(self.arguments)):
                if self.arguments[i] != other.arguments[i]:
                    equal_arguments = False

        return self.mnemonic.lower() == other.mnemonic.lower() and equal_arguments

    def __repr__(self):
        return f"Instruction({self.mnemonic}, Arguments={self.arguments})"


class Argument:
    """
    Represents an argument that an instruction could have.
    i.e. `MOV 1` 1 is an immediate-value argument.
    """
    def __init__(self, value, address=False):
        """
        :param value: The value of this argument
        :param address: Set to true if this argument was preceded with a '$' character.
        """
        self.value = value
        self.address = address

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.value == other.value and self.address == other.address

    def __repr__(self):
        return f"Argument({self.value}, address={self.address})"
