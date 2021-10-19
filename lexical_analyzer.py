from os import error

final_states = [
    2, 4, 12, 18, 21, 
    23, 25, 28, 29, 31, 
    35, 37, 38, 41
]
retroactive_states = [
    1, 3, 5, 6, 8, 9, 
    10, 11, 13, 14, 15, 
    39, 15, 16, 22, 37, 
    19, 20, 42, 7,
]
matrix = {
      # [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,     30,  31],
      # [ L,  D,  _,  ",  ',  +,  -,  *,  /,  =,  !,  >,  <,  &,  |,  %,  #,  {,  },  (,  ),  [,  ],  ;,  .,  ,,   ,  \, \n,  S, outros, EOF],
     0: [ 1,  3, 37, 30, 33,  8, 10, 12, 12, 13, 17, 15, 16, 19, 20, 24, 37, 22, 23, 23, 23, 23, 23, 23, 23, 23,  0, 37,  0, 37,     38,   0],
     1: [ 1,  1,  1,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,     38,   0],
     3: [ 7,  3,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  5,  4,  4,  4,  4,  4,     38,   0],
     5: [ 7,  6,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,     38,   0],
     6: [ 7,  6,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  7,  4,  4,  4,  4,  4,     38,   0],
     7: [ 7,  7,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  7,  0,  0,  0,  0,  0,      0,   0],
     8: [12, 12, 12, 12, 12,  9, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,     38,   0],
     9: [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,     38,   0],
    10: [12, 12, 12, 12, 12, 12, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,     38,   0],
    11: [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,     38,   0],
    13: [18, 18, 18, 18, 18, 18, 18, 18, 18, 14, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,     38,   0],
    14: [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,     38,   0],
    15: [18, 18, 18, 18, 18, 18, 18, 18, 18, 39, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,     38,   0],
    16: [18, 18, 18, 18, 18, 18, 18, 18, 18, 39, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,     38,   0],
    17: [21, 21, 21, 21, 21, 21, 21, 21, 21, 18, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,     38,   0],
    19: [41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41,     38,   0],
    20: [41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41,     38,   0],
    22: [23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 26, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23,     38,   0],
    24: [24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 25, 24,     24,   0],
    26: [26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 27, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26,     26,  29],
    27: [26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 28, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26,     26,  29],
    30: [30, 30, 30, 31, 32, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 43, 32, 30,     32,  32],
    32: [32, 32, 32,  0, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32,  0, 32,     32,  32],
    33: [34, 34, 34, 36, 35, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 44, 34, 34,     36,  36],
    34: [36, 36, 36, 36, 35, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,     36,  36],
    36: [36, 36, 36, 36,  0, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,  0, 36,     36,  36],
    39: [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,     38,   0],
    42: [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,     21,   0],
    43: [32, 32, 32, 30, 30, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 30, 32, 32,     32, 32],
    44: [36, 36, 36, 34, 34, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 34, 36, 36,     36, 36]
}

type = {
    2: "IDE", 4:"NRO", 7:"NMF", 12:"ART", 18:"REL", 
    21:"LOG", 23:"DEL", 29:"CoMF", 31:"CAD", 32:"CMF",
    35:"CAR", 36:"CaMF", 37:"SIB", 38:"SII", 40:"PRE",
    41:"OpMF"
}

error_states = [7, 29, 32, 36, 37, 38, 41]

reserved_words = [ 
    "algoritmo", "variaveis", "constantes", "registro",
    "funcao", "retorno", "vazio", "se", "senao", "enquanto",
    "para", "leia", "escreva", "inteiro", "real", "booleano", 
    "char", "cadeia", "verdadeiro", "falso" 
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
    elif character == ' ' or character == '\t':
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

'''
Paramêtros:
    folder_in - caminho da pasta onde estão os arquivos de entrada
    folder_out - caminho da pasta onde estão os arquivos de saída
    index - número do arquivo que será lido

Retorno:
    tokens - lista com os tokens extraidos pela analise léxica de um arquivo
'''
def scanner(folder_in, folder_out, index) -> list:
    input = open(folder_in + f'entrada{index}.txt', 'r')
    output = open(folder_out + f'saida{index}.txt', 'w')
    text = input.readlines()
    tokens = []
    errors = []
    num_line = 1    # line counter
    state = 0
    lexeme = ''
    for line in text:
        i = 0
        if num_line < 10:
            nl = f"0{num_line}"
        else: 
            nl = "num_line"
        while i < len(line):
            char = line[i]
            lexeme += char
            column = getColumn(char)
            previous_state = state
            state = matrix[previous_state][column]
            
            if state in final_states:
                if previous_state in retroactive_states:
                    i -= 1
                    lexeme = lexeme[:-1]
                lexeme = lexeme.strip()
                if state == 2 and lexeme in reserved_words:
                    state = 40
                if state != 25 and state != 28:
                    if state not in error_states:
                        tokens.append({'lexeme': lexeme, 'type': type[state], 'line': nl})
                    else:
                        errors.append({'lexeme': lexeme, 'state': state, 'line': nl})
            
                state = 0
                lexeme = ''
            if previous_state in error_states and state == 0:
                if previous_state in retroactive_states:
                    i -= 1
                    lexeme = lexeme[:-1]
                lexeme = lexeme.strip()
                errors.append({'lexeme': lexeme, 'state': previous_state, 'line': nl})
                lexeme = ''
            i += 1
        if state in error_states:
            lexeme = lexeme.strip()
            errors.append({'lexeme': lexeme, 'state': state, 'line': nl})
            lexeme = ''
            state = 0
        num_line += 1
    
    # Condition for if the file ends and certain lexemes are open
    if state in [26, 27, 30, 34]:
        num_line -= lexeme.count('\n')
        if num_line < 10:
            nl = f"0{num_line}"
        else: 
            nl = "num_line"
        lexeme = lexeme.replace('\n', ' ').strip()
        errors.append({'lexeme': lexeme, 'state': 29, 'line': nl})
    
    if len(errors) == 0: output.write("SUCESSO!\n")
    for error in errors:
        output.write(f"{error['line']} {type[error['state']]} {error['lexeme']}") 
   
    input.close()
    output.close()
    return tokens