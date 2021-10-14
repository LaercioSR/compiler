class Analyzer:
    def __init__(self, input):
        self.input = input 
        self.lookahead = input[0]
        self.i = 0

    def match(self, t):
        if t == self.lookahead['lexeme']:
            self.lookahead = self.next_terminal()
        else:
            print(self.lookahead['lexeme'], t, " sintax error match")

    def next_terminal(self):
        if(self.i < len(input)-1): self.i = self.i+1
        return self.input[self.i]

    def start(self):
        if self.lookahead['lexeme'] == 'algoritmo':
            self.match('algoritmo')
            return self.algoritmo()
        print("sintax error start"); return False

    def algoritmo(self):
        if self.lookahead['lexeme'] == '{':
            self.match('{')
            self.conteudo()
            self.match('}')
            return True
        print(self.lookahead, " sintax error algoritmo"); return False

    def conteudo(self):
        if self.lookahead['lexeme'] == 'escreva':
            self.match('escreva')
            return self.escreva()
        print(self.lookahead['lexeme'], " sintax error escreva")

    def escreva(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            if self.escont():
                return True
        # caso alguma função retorne um erro ou o erro esteja no escreva, imprime msg de erro
        return False

    def escont(self):
        if self.acessovar() or self.cadeia() or self.char():
            return self.esfim()
        print("sintax error"); return False

    def esfim(self):
        if self.lookahead['lexeme'] == ',':
            self.match(',')
            self.escont()
        elif self.lookahead['lexeme'] == ')':
            self.match(')')
            self.match(';')
        else:
            print("sintax error"); return False
        return True
            
    def acessovar(self):
        return self.ide() and self.acessovarcont()

    def acessovarcont(self):
        if self.lookahead['lexeme'] == '.':
            self.match('.')
            self.acessovar()
        elif self.lookahead['lexeme'] == '[':
            self.match('[')
            self.nro()
            self.match(']')
            self.acessovarcontb()
        else: 
            return False
        return True

    def acessovarcontb(self):
        if self.lookahead['lexeme'] == '[':
            self.match('[')
            self.nro()
            self.match(']')
            self.acessovarcontc()
            return True
        print("sintax error"); return False
        

    def acessovarcontc(self):
        if self.lookahead['lexeme'] == '[':
            self.match('[')
            self.nro()
            self.match(']')
            return True
        print("sintax error"); return False

    def cadeia(self):
        if self.lookahead['type'] == 'CAD':
            self.match(self.lookahead['lexeme'])
            return True
        return False

    def char(self):
        if self.lookahead['type'] == 'CAR':
            self.match(self.lookahead['lexeme'])
            return True
        return False

    def ide(self):
        if self.lookahead['type'] == 'IDE':
            self.match(self.lookahead['lexeme'])
            return True
        return False
    
    def nro(self):
        if self.lookahead['type'] == 'NRO':
            self.match(self.lookahead['lexeme'])
            return True
        print("sintax error"); return False

    def simbolo(self):
        if self.lookahead['type'] == 'SIB':
            self.match(self.lookahead['lexeme'])
            return True
        print("sintax error"); return False

# teste
input = [{'lexeme': 'algoritmo', 'type': 'PRE', 'line': '01'}, 
        {'lexeme': '{', 'type': 'DEL', 'line': '01'}, 
        {'lexeme': 'escreva', 'type': 'PRE', 'line': '02'}, 
        {'lexeme': '(', 'type': 'DEL', 'line': '02'}, 
        {'lexeme': '"Hello world"', 'type': 'CAD', 'line': '02'}, 
        {'lexeme': ')', 'type': 'DEL', 'line': '02'}, 
        {'lexeme': ';', 'type': 'DEL', 'line': '02'}, 
        {'lexeme': '}', 'type': 'DEL', 'line': '03'}]

ans = Analyzer(input).start()
print(ans)