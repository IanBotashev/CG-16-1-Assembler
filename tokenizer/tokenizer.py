from pyparsing import Word, nums, alphas, Combine, DelimitedList, Literal, Optional, hexnums
from core.assembler_types import Instruction, Argument
from core.exceptions import InvalidSyntax


class Tokenizer:
    """
    Takes a list of raw strings and converts them into Instruction objects
    """
    def __init__(self, hex_indicator="0x", binary_indicator="0b", address_indicator="$", allow_overflow=False):
        """
        :param hex_indicator: Character(s) used to indicate a hex number
        :param binary_indicator: Character(s) used to indicate a binary number
        :param address_indicator: Character(s) used to indicate an address
        :param allow_overflow: Allow values higher than 16-bit int limit.
        """
        # Settings
        self.allow_overflow = allow_overflow
        self.hex_indicator = hex_indicator
        self.binary_indicator = binary_indicator
        self.address_indicator = address_indicator

        # Pyparsing definitions
        mnemonic = Word(alphas).setResultsName("mnemonic").set_parse_action(lambda x: str(x[0]).lower())
        hex_value = Combine(Literal(self.hex_indicator) + Word(hexnums)).set_parse_action(lambda x: int(x[0][2:], 16))
        binary_value = Combine(Literal(self.binary_indicator) + Word("01")).set_parse_action(lambda x: int(x[0][2:], 2))
        decimal_value = Word(nums).set_parse_action(lambda x: int(x[0]))
        label = Word(alphas)
        argument = Combine(Optional(Literal(self.address_indicator)).set_results_name("address") + (
                    hex_value | binary_value | decimal_value | label).set_results_name("arg_value")).set_parse_action(
            self.parse_action_for_argument)
        self.instruction = mnemonic + Optional(DelimitedList(argument, ",")).setResultsName("arguments")

    def parse_file(self, file_path):
        """
        Parses a file from a path
        :param file_path: Path of file to parse
        :return: A list of instruction objects.
        """
        result = []
        with open(file_path, "r") as f:
            lines = f.readlines()
            for index in range(len(lines)):
                line = lines[index].strip()  # Remove spaces and /n
                result.append(self.parse_string(line))

        return result

    def parse_string(self, string):
        """
        Parses a single string and, should, return a single Instruction object
        :param string:
        :return:
        """
        data = self.instruction.parse_string(string, parse_all=True)
        arguments = list(data.arguments) if hasattr(data, 'arguments') else None
        result = Instruction(data.mnemonic, arguments=arguments)

        if not result.check_if_valid_instruction():
            raise InvalidSyntax(f"Unknown mnemonic {result.mnemonic}")

        return result

    def parse_action_for_argument(self, x):
        """
        pyparsing parse action for an argument
        :return:
        """
        if isinstance(x.arg_value, int) and x.arg_value >= (2 ** 16) and not self.allow_overflow:
            raise InvalidSyntax(f"Value higher than 16-bits ({x.arg_value})")

        return Argument(x.arg_value, address=x.address == self.address_indicator)
