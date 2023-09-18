MULTIPLY = "*"
DIVIDE = "/"
ADD = "+"
SUBTRACT = "-"
MOD = "%"
EXPONENTIATE = "^"

SHIFT_LEFT = "<<"
SHIFT_RIGHT = ">>"
AND = "AND"
OR = "OR"
XOR = "XOR"


GREATER_THAN = ">"
LESS_THAN = "<"
EQUAL_TO = "="

GREATER_THAN_OR_EQUAL_TO = "\u2265"
LESS_THAN_OR_EQUAL_TO = "\u2264"
NOT_EQUAL_TO = "\u2260"


lambda_operations = {
    MULTIPLY: lambda a, b: int(a * b),
    DIVIDE: lambda a, b: int(a / b),
    ADD: lambda a, b: int(a + b),
    SUBTRACT: lambda a, b: int(a - b),
    MOD: lambda a, b: int(a % b),
    EXPONENTIATE: lambda a, b: int(a ** b),

    SHIFT_LEFT: lambda a, b: int(a << b),
    SHIFT_RIGHT: lambda a, b: int(a >> b),
    AND: lambda a, b: int(a and b),
    OR: lambda a, b: int(a or b),
    XOR: lambda a, b: int(a ^ b),


    GREATER_THAN: lambda a, b: int(a > b),
    LESS_THAN: lambda a, b: int(a < b),
    EQUAL_TO: lambda a, b: int(a == b),

    GREATER_THAN_OR_EQUAL_TO: lambda a, b: int(a >= b),
    LESS_THAN_OR_EQUAL_TO: lambda a, b: int(a <= b),
    NOT_EQUAL_TO: lambda a, b: int(a != b)
}