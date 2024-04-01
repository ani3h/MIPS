def BinaryToDecimal(binary):
    binary = int(binary)
    decimal, i = 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1

    return decimal


def DecimalToBinary(decimal):
    return bin(decimal).replace("0b", "")


def StringToBinary(string):
    return str(bin(int(string)).replace("0b", ""))


def DecimalToBinaryNum(decimal_number, num):
    binary_representation = bin(decimal_number)[2:]
    padding_length = num - len(binary_representation)

    binary_result = '0' * padding_length + binary_representation

    return binary_result
