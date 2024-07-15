import pytest
from tokenizer.tokenizer import Tokenizer
from core.assembler_types import Instruction, Argument
from core.exceptions import InvalidSyntax


@pytest.fixture
def tokenizer():
    return Tokenizer()


def test_tokenizer_fixture(tokenizer):
    """
    Tests if the fixture is working correctly.
    :param tokenizer:
    :return:
    """
    assert isinstance(tokenizer, Tokenizer)


@pytest.mark.parametrize(
    "string_to_parse, expected_token",
    [
        ("mOV", Instruction("mov")),
        ("AdC", Instruction("adc")),
        ("int", Instruction("int")),
        ("MOv", Instruction("mov")),
    ])
def test_instruction_tokenizing(tokenizer, string_to_parse, expected_token):
    """
    Make sure that the tokenizer returns the correct token when passing in just an instruction with no arguments.
    :return:
    """
    print(string_to_parse)
    tokens = tokenizer.parse_string(string_to_parse)
    assert tokens == expected_token


@pytest.mark.parametrize(
    "string_to_parse, expected_exception",
    [
        ("NOT_AN_INSTRUCTION", Exception),
        ("notaninstruction", Exception),
        ("3", Exception),
    ])
def test_instruction_tokenizing_with_illegal_syntax(tokenizer, string_to_parse, expected_exception):
    """
    Tests if the tokenizer raises the appropriate exception when attempting to parse invalid strings.
    :param tokenizer:
    :param string_to_parse:
    :param expected_exception:
    :return:
    """
    with pytest.raises(expected_exception):
        tokens = tokenizer.parse_string(string_to_parse)


@pytest.mark.parametrize(
    "string_to_parse, expected_token",
    [
        ("MOV 0b1001, 0x1234, 9876", Instruction("mov", arguments=[Argument(9, address=False), Argument(4660, address=False), Argument(9876, address=False)])),
        ("aDC $2, a, $b", Instruction("adc", arguments=[Argument(2, address=True), Argument("a", address=False), Argument("b", address=True)])),
        ("int $0b1010, 0xA15,$5, $0xB16A ,      7", Instruction("int", arguments=[Argument(10, address=True), Argument(2581, address=False), Argument(5, address=True), Argument(45418, address=True), Argument(7, address=False)])),
    ])
def test_argument_tokenizing(tokenizer, string_to_parse, expected_token):
    """
    Tests if the tokenizer can properly tokenize an instruction with arguments into the right token.
    :return:
    """
    tokens = tokenizer.parse_string(string_to_parse)
    assert tokens == expected_token


@pytest.mark.parametrize(
    "string_to_parse, expected_exception",
    [
        ("MoV 1 2 $3", Exception),
        ("MoV $1 $2", Exception),
        ("MoV $$1, 2, 3", Exception),
        ("MoV 0b2001, 0xZ", Exception),  # Invalid binary and hex
        ("MoV 0x10001", InvalidSyntax),  # Past 16-bit
        ("MoV 0b10000000000000000", InvalidSyntax),  # Past 16-bit
        ("MoV 65536", InvalidSyntax),  # Past 16-bit
        ("MoV 0xb5151", Exception)
    ])
def test_argument_tokenizing_with_illegal_syntax(tokenizer, string_to_parse, expected_exception):
    """
    Tests if these cases end up as expected exceptions
    :param tokenizer:
    :param string_to_parse:
    :param expected_exception:
    :return:
    """
    with pytest.raises(expected_exception):
        tokenizer.parse_string(string_to_parse)
