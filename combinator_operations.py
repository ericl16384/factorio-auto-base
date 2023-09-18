# arithmetic

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


# decider

GREATER_THAN = ">"
LESS_THAN = "<"
EQUAL_TO = "="

GREATER_THAN_OR_EQUAL_TO = "\u2265"
LESS_THAN_OR_EQUAL_TO = "\u2264"
NOT_EQUAL_TO = "\u2260"


arithmetic = {
    MULTIPLY: lambda a, b: a * b,
    DIVIDE: lambda a, b: a // b,
    ADD: lambda a, b: a + b,
    SUBTRACT: lambda a, b: a - b,
    MOD: lambda a, b: a % b,
    EXPONENTIATE: lambda a, b: a ** b,

    SHIFT_LEFT: lambda a, b: a << b,
    SHIFT_RIGHT: lambda a, b: a >> b,
    AND: lambda a, b: a and b,
    OR: lambda a, b: a or b,
    XOR: lambda a, b: a ^ b,
}

decider = {
    GREATER_THAN: lambda a, b: a > b,
    LESS_THAN: lambda a, b: a < b,
    EQUAL_TO: lambda a, b: a == b,

    GREATER_THAN_OR_EQUAL_TO: lambda a, b: a >= b,
    LESS_THAN_OR_EQUAL_TO: lambda a, b: a <= b,
    NOT_EQUAL_TO: lambda a, b: a != b
}




# for operation in arithmetic:
#     f = arithmetic[operation]
#     arithmetic[operation] = lambda a, b: int(f(a, b))

# for operation in decider:
#     f = decider[operation]
#     decider[operation] = lambda a, b: int(f(a, b))


# def arithmetic_handle_boolean(value, do_boolean):
#     assert not do_boolean
#     return int(value)
# def decider_handle_boolean(value, do_boolean):
#     if do_boolean:
#         value = bool(value)
#     return int(value)


# lambda_operations = {
#     MULTIPLY: lambda a, b, boolean: int(a * b),
#     DIVIDE: lambda a, b, boolean: int(a / b),
#     ADD: lambda a, b, boolean: int(a + b),
#     SUBTRACT: lambda a, b, boolean: int(a - b),
#     MOD: lambda a, b, boolean: int(a % b),
#     EXPONENTIATE: lambda a, b, boolean: int(a ** b),

#     SHIFT_LEFT: lambda a, b: int(a << b),
#     SHIFT_RIGHT: lambda a, b: int(a >> b),
#     AND: lambda a, b: int(a and b),
#     OR: lambda a, b: int(a or b),
#     XOR: lambda a, b: int(a ^ b),


#     GREATER_THAN: lambda a, b, boolean: decider_handle_boolean(a > b, boolean),
#     LESS_THAN: lambda a, b, boolean: decider_handle_boolean(a < b, boolean),
#     EQUAL_TO: lambda a, b, boolean: decider_handle_boolean(a == b, boolean),

#     GREATER_THAN_OR_EQUAL_TO: lambda a, b, boolean: decider_handle_boolean(a >= b, boolean),
#     LESS_THAN_OR_EQUAL_TO: lambda a, b, boolean: decider_handle_boolean(a <= b, boolean),
#     NOT_EQUAL_TO: lambda a, b, boolean: decider_handle_boolean(a != b, boolean)
# }
