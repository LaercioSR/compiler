import os.path

final_states = [
    2, 4, 7, 8, 9, 10, 12, 13, 14, 15, 17, 
    18, 20, 21, 23, 24, 26, 27, 29, 31, 32, 33, 
    34, 35, 36, 37, 38, 39, 40, 42, 46, 48, 51
]
matrix = [
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
    # [L, D, _, ", ', +, -, *, /, =,  !,  >,  <,  &,  |,  %,  #,  {,  },  (,  ),  [,  ],  ;,  .,  ,,  \, \n,  S, outros],
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 33, 37, 38, 39, 40, 34, 36, 35, '-', '-', '-', '-'],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
]

def getColumn(character):
    code_ascii = ord(character)
    if (code_ascii >= 65 and code_ascii <= 90) or (code_ascii >= 97 and code_ascii <= 122):
        return 0
    elif (code_ascii >= 48 and code_ascii <= 57):
        return 1
    elif character == '_':
        return 2
    elif character == '"':
        return 3
    elif character == '\'':
        return 4
    elif character == '+':
        return 5
    elif character == '-':
        return 6
    elif character == '*':
        return 7
    elif character == '/':
        return 8
    elif character == '=':
        return 9
    elif character == '!':
        return 10
    elif character == '>':
        return 11
    elif character == '<':
        return 12
    elif character == '&':
        return 13
    elif character == '|':
        return 14
    elif character == '%':
        return 15
    elif character == '#':
        return 16
    elif character == '{':
        return 17
    elif character == '}':
        return 18
    elif character == '(':
        return 19
    elif character == ')':
        return 20
    elif character == '[':
        return 21
    elif character == ']':
        return 22
    elif character == ';':
        return 23
    elif character == '.':
        return 24
    elif character == ',':
        return 25
    elif character == ' ':
        return 26
    elif character == '\\':
        return 27
    elif character == '\n' or character == '\t':
        return 28
    elif (code_ascii >= 32 and code_ascii <= 126) and code_ascii != 34 and code_ascii != 39:
        return 29

index = 1
while os.path.isfile(f'input/entrada{index}.txt'):
    input = open(f'input/entrada{index}.txt', 'r')
    output = open(f'output/saida{index}.txt', 'w')
    text = input.read()

    i = 0
    state = 0
    lexeme = ''
    while i < len(text):
        char = text[i]
        lexeme += char
        column = getColumn(char)
        state = matrix[state][column]
        # output.write(f"{char} - {column}\n")
        if state in final_states:
            output.write(f"State: {state} - Token: {lexeme}\n")
            state = 0
            lexeme = ''
        elif state == '-':
            state = 0
            lexeme = ''
        i += 1
    
    # output.write(f'Output number {index}')
    output.close()

    index += 1