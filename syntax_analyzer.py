class SintaxAnalyzer:
    def __init__(self, input):
        self.input = input 
        self.lookahead = input[0]
        self.i = 0

    def match(self, t):
        # print(f"{self.lookahead} == {t} : {t == self.lookahead['lexeme']}")
        if t == self.lookahead['lexeme']:
            self.lookahead = self.next_terminal()
            return True
        else:
            print(self.lookahead['lexeme'], t, " sintax error match")
            return False

    def next_terminal(self):
        if(self.i < len(self.input)-1): self.i = self.i+1
        return self.input[self.i]

    def error(self):
        sync_tokens = [';']
        print("sintax error linha: ", self.lookahead['line'])
        
        while(self.lookahead['lexeme'] not in sync_tokens):
            self.lookahead = self.next_terminal()
            if(self.i == len(self.input)-1):
                break
        self.lookahead = self.next_terminal()

    def start(self):
        ans = False
        if self.lookahead['lexeme'] == 'algoritmo':
            self.match('algoritmo')
            ans = self.algoritmo()
        elif self.lookahead['lexeme'] == 'funcao':
            #self.match('funcao')
            #ans = self.funcao()
            ans = True
        elif self.lookahead['lexeme'] == 'variaveis':
            #self.match('variaveis')
            #ans = self.variaveis()
            ans = True
        elif self.lookahead['lexeme'] == 'constantes':
            #self.match('constantes')
            #ans = self.constantes()
            ans = True
        elif self.lookahead['lexeme'] == 'registro':
            #self.match('registro')
            #ans = self.registro()
            ans = True
        if ans:
            return True
        # print("sintax error linha: ", self.lookahead['line']); return False
        return False

    def algoritmo(self):
        if self.lookahead['lexeme'] == '{':
            self.match('{')
            ans=True
            # while(ans and self.lookahead['lexeme'] != '}'):
            #     ans = self.conteudo()
            while(self.lookahead['lexeme'] != '}' and self.i < len(self.input)-1):
                result = self.conteudo()
                if not result:
                    self.error()
                    ans = result
            return ans and self.match('}')
        return False

    def conteudo(self):
        if self.lookahead['lexeme'] == 'variaveis':
            #self.match('variaveis')
            #return self.variaveis()
            return True
        elif self.lookahead['lexeme'] == 'constantes':
            #self.match('constantes')
            #return self.constantes()
            return True
        elif self.lookahead['lexeme'] == 'se':
            #self.match('se')
            #return self.se()
            return True
        elif self.lookahead['lexeme'] == 'enquanto':
            #self.match('enquanto')
            #return self.enquanto()
            return True
        elif self.lookahead['lexeme'] == 'escreva':
            self.match('escreva')
            return self.escreva()
        elif self.lookahead['lexeme'] == 'leia':
            self.match('leia')
            return self.leia()
        elif self.lookahead['lexeme'] == 'para':
            #self.match('para')
            #return self.para()
            return True
        elif self.lookahead['lexeme'] == 'registro':
            #self.match('registro')
            #return self.registro()
            return True
        return False

    def escreva(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            return self.escont()
        return False

    def escont(self):
        if self.acessovar() or self.cadeia() or self.char():
            return self.esfim()
        return False

    def esfim(self):
        if self.lookahead['lexeme'] == ',':
            self.match(',')
            return self.escont()
        elif self.lookahead['lexeme'] == ')':
            self.match(')')
            self.match(';')
            return True
        return False

    def leia(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            return self.leiacont()
        return False

    def leiacont(self):
        if self.acessovar():
            return self.leiafim()
        return False

    def leiafim(self):
        if self.lookahead['lexeme'] == ',':
            self.match(',')
            return self.leiacont()
        elif self.lookahead['lexeme'] == ')':
            self.match(')')
            self.match(';')
            return True
        return False
            
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
        # else: 
        #     return False
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
