from os import error
import os.path

final_states = [
    2, 4, 7, 12, 18, 21, 
    23, 25, 28, 29, 31, 
    32, 35, 36, 37, 38
]
retroactive_states = [
    1, 3, 5, 6, 8, 9, 
    10, 11, 13, 14, 15, 
    39, 16, 17, 22, 37
]
matrix = [[0] * 32] * 40
matrix = [
  # [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,     30,  31],
  # [ L,  D,  _,  ",  ',  +,  -,  *,  /,  =,  !,  >,  <,  &,  |,  %,  #,  {,  },  (,  ),  [,  ],  ;,  .,  ,,   ,  \, \n,  S, outros, EOF],
    [ 1,  3, 37, 30, 33,  8, 10, 12, 12, 13, 17, 15, 16, 19, 20, 24, 37, 22, 23, 23, 23, 23, 23, 23, 23, 23,  0, 37,  0, 37,     38,   0],
    [ 1,  1,  1,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,     38,   0],
    [],
    [ 7,  3,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  5,  4,  4,  4,  4,  4,     38,   0],
    [],
    [ 7,  6,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,     38,   0],
    [ 7,  6,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  7,  4,  4,  4,  4,  4,     38,   0],
    [],
    [12, 12, 12, 12, 12,  9, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,     38,   0],
    [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,     38,   0],
    [12, 12, 12, 12, 12, 12, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,     38,   0],
    [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,     38,   0],
    [],
    [18, 18, 18, 18, 18, 18, 18, 18, 18, 14, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,     38,   0],
    [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,     38,   0],
    [18, 18, 18, 18, 18, 18, 18, 18, 18, 39, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,     38,   0],
    [18, 18, 18, 18, 18, 18, 18, 18, 18, 39, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,     38,   0],
    [21, 21, 21, 21, 21, 21, 21, 21, 21, 18, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,     38,   0],
    [],
    [37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 21, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,     38,   0],
    [37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 21, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,     38,   0],
    [],
    [23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 26, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23,     38,   0],
    [],
    [24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 25, 24,     24,   0],
    [],
    [26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 27, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26,     26,  29],
    [26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 28, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26,     26,  29],
    [],
    [],
    [30, 30, 30, 31, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 32, 30,     38,  32],
    [],
    [],
    [34, 34, 34, 34, 35, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34,     38,  36],
    [36, 36, 36, 36, 35, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,     38,  36],
    [],
    [],
    [],
    [],
    [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,     38,   0]
]

type = {2: "IDE", 4:"NRO", 7:"NMF", 12:"ART", 18:"REL", 
        21:"LOG", 23:"DEL", 29:"CoMF", 31:"CAD", 32:"CMF",
        35:"CAR", 36:"CaMF", 37:"SIB", 38:"SII", 40:"PRE"}

error_states = [38, 32, 7, 36, 29, 41, 37]

reserved_words = ["algoritmo", "variaveis", "constantes", "registro",
 "funcao", "retorno", "vazio", "se", "senao", "enquanto",
 "para", "leia", "escreva", "inteiro", "real", "booleano", "char",
 "cadeia", "verdadeiro", "falso"]

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
    elif character == '\n':
        return 28
    elif (code_ascii >= 32 and code_ascii <= 126) and code_ascii != 34 and code_ascii != 39:
        return 29
    elif code_ascii == 3 or code_ascii == 4 or code_ascii == 26:
        return 31
    else: # Invalid character
        return 30

index = 1
while os.path.isfile(f'input/entrada{index}.txt'):
    input = open(f'input/entrada{index}.txt', 'r')
    output = open(f'output/saida{index}.txt', 'w')
    text = input.readlines()
    tokens = []
    errors = []
    #para cada linha do arquivo
    num_line = 1
    state = 0
    lexeme = ''
    for line in text:
        i = 0
        while i < len(line):
            char = line[i]
            lexeme += char
            column = getColumn(char)
            previous_state = state
            state = matrix[previous_state][column]
            # print(f"char: {char} - ascii: {ord(char)} - state: {state} - lexeme: {lexeme}")
            if state in final_states:
                if previous_state in retroactive_states:
                    i -= 1
                    lexeme = lexeme[:-1]
                lexeme = lexeme.strip()
                if lexeme in reserved_words:
                    state = 40
                if state != 25 and state != 28:
                    if state not in error_states:
                        tokens.append({'lexeme': lexeme, 'state': state, 'line': num_line})
                    else:
                        errors.append({'lexeme': lexeme, 'state': state, 'line': num_line})
                    # if num_line<10: output.write("0")
                    # output.write(f"{num_line} {type[state]} {lexeme}\n")
            
                state = 0
                lexeme = ''
            i += 1
        num_line += 1
    if state == 26 or state == 27:
        lexeme = lexeme.replace('\n', ' ').strip()
        errors.append({'lexeme': lexeme, 'state': 29, 'line': num_line})
    for token in tokens:
        if token['line'] < 10:
            token['line'] = f"0{token['line']}"
        output.write(f"{token['line']} {type[token['state']]} {token['lexeme']}\n")
    output.write("\n")   
    for error in errors:
        if error['line'] < 10:
            error['line'] = f"0{error['line']}"
        output.write(f"{error['line']} {type[error['state']]} {error['lexeme']}\n") 
    output.close()

    index += 1