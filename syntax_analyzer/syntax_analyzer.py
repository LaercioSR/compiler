class Analyzer:
    def __init__(self, input):
        self.input = input 
        self.lookahead = 0
        self.i = 0

    def match(self, t):
        if t == self.lookahead:
            self.lookahead = self.next_terminal()
        else:
            print("sintax error")

    def next_terminal(self):
        self.i = self.i+1
        return self.input[self.i]

    def escreva(self):
        if self.lookahead == '(':
            self.match('(')
            if self.escont():
                return True
        # caso alguma função retorne um erro ou o erro esteja no escreva, imprime msg de erro
        print("sintax error"); return False

    def escont(self):
        if self.acessovar() or self.cadeia() or self.char():
            return self.esfim()
        else:
            print("sintax error"); return False

    def esfim(self):
        if self.lookahead == ',':
            self.match(',')
            self.escont()
        elif self.lookahead == ')':
            self.match(')')
            self.match(';')
        else:
            print("sintax error"); return False
        return True
            
    def acessovar(self):
        return self.ide() and self.acessovarcont()

    def acessovarcont(self):
        if self.lookahead == '.':
            self.match('.')
            self.acessovar()
        elif self.lookahead == '[':
            self.match('[')
            self.nro()
            self.match(']')
            self.acessovarcontb()
        else:
            print("sintax error"); return False
        return True

    def acessovarcontb(self):
        if self.lookahead == '[':
            self.match('[')
            self.nro()
            self.match(']')
            self.acessovarcontc()
        else:
            print("sintax error"); return False
        return True

    def acessovarcontc(self):
        if self.lookahead == '[':
            self.match('[')
            self.nro()
            self.match(']')
        else:
            print("sintax error"); return False
        return True

    def cadeia(self):
        if self.lookahead == '\"':
            self.match('\"')
            self.cadcont()
            self.match('\"')
        else:
            print("sintax error"); return False

    def cadcont(self):
        if(self.letra() or self.digito() or self.simbolo or self.charspec):
            return self.cadcont()
        else: 
            print("sintax error"); return False

    def char(self):
        if self.lookahead == '\'':
            self.match('\'')
            self.letra()
            self.match('\'')
        elif self.lookahead == '\'':
            self.match('\'')
            self.digito()
            self.match('\'')
        elif self.lookahead == '\'':
            self.match('\'')
            self.simbolo()
            self.match('\'')
        elif self.lookahead == '\'':
            self.match('\'')
            self.charspec()
            self.match('\'')
        else:
            print("sintax error"); return False
        return True

    def charspec(self):
        if self.lookahead == '\\\'' or self.lookahead == '\\\"':
            self.match(self.lookahead)
        else:
            print("sintax error"); return False
        return True

    def letra(self):
        if self.lookahead >= 'a' and self.lookahead <= 'z':
            self.match(self.lookahead)
        elif self.lookahead >= 'A' and self.lookahead <= 'Z':
            self.match(self.lookahead)
        else:
            print("sintax error"); return False
        return True

    def ide(self):
        return self.letra() and self.idecont()

    def idecont(self):
        if self.lookahead == '_' or self.lookahead == ' ':
            self.match(self.lookahead)
            return self.ide()
        elif self.letra() or self.digito():
            return self.ide()

        print("sintax error")
        return False

    def digito(self):
        if self.lookahead >= 0 or self.lookahead <=9:
            self.match(self.lookahead)
            return True
        print("sintax error")
        return False

    def nro(self):
        return self.digito() and self.nrocont()

    def nrocont(self):
        if self.lookahead != ' ':
            if self.digito():
                return self.nrocont()

            print("sintax error")
            return False
            

input = "escreva(\"hello world\");"       
Analyzer(input).escreva()