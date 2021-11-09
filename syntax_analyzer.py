class SintaxAnalyzer:
    def __init__(self, input,output_file):
        self.input = input 
        self.lookahead = input[0]
        self.i = 0
        self.symbol_table = []
        self.last_ide = None
        self.expected = None
        self.output = open(output_file, 'a')

    def run(self):
        #ans = self.start()
        #print(self.symbol_table)
        ans = self.start()
        if ans:
            self.output.write("Sucesso!\n") 
            self.output.close()
        return ans

    def match(self, t):
        self.expected = t
        if t == self.lookahead['lexeme']:
            self.lookahead = self.next_terminal()
            return True
        else:
            #print(f"Expected: {t} Found: {self.lookahead['lexeme']} sintax error match")
            return False

    def next_terminal(self):
        if(self.i < len(self.input)-1): self.i = self.i+1
        return self.input[self.i]

    def follow(self, k=1):
        return self.input[self.i+k]

    def save_symbol(self, category):
        symbol = { "lexeme": self.last_ide, "category": category }
        self.symbol_table.append(symbol)

    def error(self):
        sync_tokens = [';']
        self.output.write(f"Syntax Error: Found: '{self.lookahead['lexeme']}', line: {self.lookahead['line']}\n") 

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
            self.match('funcao')
            if self.funcao():
                ans = self.start()
        elif self.lookahead['lexeme'] == 'variaveis':
            self.match('variaveis')
            ans = self.variaveis() and self.a()
        elif self.lookahead['lexeme'] == 'constantes':
            self.match('constantes')
            ans = self.constantes() and self.b()
        elif self.lookahead['lexeme'] == 'registro':
            self.match('registro')
            ans = self.registro() and self.start()            
        if not ans:
            self.error()
        return ans

    def a(self):
        ans = False
        if self.lookahead['lexeme'] == 'algoritmo':
            self.match('algoritmo')
            ans = self.algoritmo()
        elif self.lookahead['lexeme'] == 'funcao':
            self.match('funcao')
            if self.funcao():
                ans = self.a()
        elif self.lookahead['lexeme'] == 'constantes':
            self.match('constantes')
            ans = self.constantes() and self.c()
        elif self.lookahead['lexeme'] == 'registro':
            self.match('registro')
            ans = self.registro() and self.a()
        return ans

    def b(self):
        ans = False
        if self.lookahead['lexeme'] == 'algoritmo':
            self.match('algoritmo')
            ans = self.algoritmo()
        elif self.lookahead['lexeme'] == 'funcao':
            self.match('funcao')
            if self.funcao():
                ans = self.b()
        elif self.lookahead['lexeme'] == 'variaveis':
            self.match('variaveis')
            ans = self.variaveis() and self.c()
        elif self.lookahead['lexeme'] == 'registro':
            self.match('registro')
            ans = self.registro() and self.b()
        return ans

    def c(self):
        ans = False
        if self.lookahead['lexeme'] == 'algoritmo':
            self.match('algoritmo')
            ans = self.algoritmo()
        elif self.lookahead['lexeme'] == 'funcao':
            self.match('funcao')
            if self.funcao():
                ans = self.c()
        elif self.lookahead['lexeme'] == 'registro':
            self.match('registro')
            ans = self.registro() and self.c()
        return ans

    def algoritmo(self):
        if self.lookahead['lexeme'] == '{':
            self.match('{')
            ans=True
            while(self.lookahead['lexeme'] != '}' and self.i < len(self.input)-1):
                result = self.conteudo()
                if not result:
                    self.error()
                    ans = result
            return ans and self.match('}')
        return False

    def conteudo(self):
        if self.lookahead['lexeme'] == 'variaveis':
            self.match('variaveis')
            return self.variaveis()
        elif self.lookahead['lexeme'] == 'constantes':
            self.match('constantes')
            return self.constantes()
        elif self.lookahead['lexeme'] == 'se':
            self.match('se')
            return self.se()
        elif self.lookahead['lexeme'] == 'enquanto':
            self.match('enquanto')
            return self.enquanto()
        elif self.lookahead['lexeme'] == 'escreva':
            self.match('escreva')
            return self.escreva()
        elif self.lookahead['lexeme'] == 'leia':
            self.match('leia')
            return self.leia()
        elif self.lookahead['lexeme'] == 'para':
            self.match('para')
            return self.para()
        elif self.lookahead['lexeme'] == 'registro':
            self.match('registro')
            return self.registro()
        elif self.lookahead['lexeme'] == 'retorno':
            self.match('retorno')
            return self.retorno()
        elif self.acessovar():
            if self.lookahead['lexeme'] == '=':
                self.match('=')
                if self.expatribuicao():
                    return self.match(';')
            elif self.lookahead['lexeme'] == '(':
                if self.chamadafuncao():
                    return self.match(';')
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
            return self.match(';')
        return False
            
    def acessovar(self):
        return self.ide() and self.acessovarcont()

    def acessovarcont(self):
        if self.lookahead['lexeme'] == '.':
            self.match('.')
            return self.acessovar()
        elif self.lookahead['lexeme'] == '[':
            self.match('[')
            if self.nro() and self.match(']'):
                return self.acessovarcontb()
        return True

    def acessovarcontb(self):
        if self.lookahead['lexeme'] in [',', ')']:
            return True
        if self.lookahead['lexeme'] == '[':
            self.match('[')
            if self.nro() and self.match(']'):
                return self.acessovarcontc()
            elif self.ide() and self.match(']'):
                return self.acessovarcontc()
        return False

    def acessovarcontc(self):
        if self.lookahead['lexeme'] in [',', ')']:
            return True
        if self.lookahead['lexeme'] == '[':
            self.match('[')
            if self.nro(): 
                return self.match(']')
            elif self.ide():
                return self.match(']')
        return False

    def follow_condicional(self):
        follow = self.follow()
        i=1
        rel_log = False
        while follow['lexeme'] not in [')','{','}']:
            follow = self.follow(i)      
            if follow['type'] in ['REL','LOG']:
                rel_log=True
                break
            i += 1
            if self.i+i >= len(self.input): break
        return rel_log

    def se(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            rel_log = self.follow_condicional()
            if rel_log:
                if self.expressao():
                    if self.function_cont():
                        return self.senao()
            elif self.lookahead['lexeme'] in ['verdadeiro','falso']:
                self.bool()
                if self.function_cont():
                    return self.senao()
            elif self.lookahead['type'] == 'IDE':
                if self.acessovar():
                    if self.function_cont():
                        return self.senao()
        return False

    def senao(self):
        if self.lookahead['lexeme'] == 'senao':
            self.match('senao')
            if self.match('{'):
                if self.conteudo():
                    return self.match('}')
        return True

    def exparitmetica(self):
        if self.lookahead['lexeme'] in ['++','--']:
            self.expatribuicaocont()
            if self.acessovar():
                return self.exparitmeticacont()
        if self.nro():
            return self.exparitmeticacont()
        if self.acessovar():
            self.expatribuicaocont()
            return self.exparitmeticacont()
        elif self.lookahead['lexeme'] == '-':
            self.match('-')
            if self.negativo():
                return self.exparitmeticacont()
        elif self.lookahead['lexeme'] == '(':
            self.match('(')
            return self.exparitmeticaparen()
        return False

    def exparitmeticaparen(self):
        if self.exparitmetica():
            if self.match(')'):
                return self.exparitmeticacontb()
        return False

    def exparitmeticacont(self):
        if self.lookahead['type'] == 'ART':
            self.match(self.lookahead['lexeme'])
            return self.exparitmeticab()
        return False

    def exparitmeticab(self):
        if self.acessovar() or self.nro():
            return self.exparitmeticacontb()
        elif self.lookahead['lexeme'] == '-':
            self.match('-')
            if self.negativo():
                return self.exparitmeticacontb()
        elif self.lookahead['lexeme'] == '(':
            self.match('(')
            return self.exparitmeticabparen()
        return False

    def exparitmeticabparen(self):
        if self.exparitmetica():
            if self.match(')'):
                return self.exparitmeticacontb()
        return False

    def exparitmeticacontb(self):
        if self.lookahead['type'] == 'ART':
            self.match(self.lookahead['lexeme'])
            return self.exparitmeticab()
        return True

    def expatribuicao(self):
        if self.lookahead['lexeme'] in ['++','--']:
            self.match(self.lookahead['lexeme'])
            if self.lookahead['type'] == 'NRO':
                return self.nro()
                #return self.match(';')
            elif self.lookahead['type'] == 'IDE':
                return self.acessovar()
                #return self.match(';')
        elif self.lookahead['type'] in ['IDE', 'NRO']:
            self.valor()
            return self.expatribuicaocont()     
            #return self.match(';')
        return self.valor()
            #return self.match(';')
        #return False
        
    def expatribuicaocont(self):
        if self.lookahead['lexeme'] in ['++','--']:
            self.match(self.lookahead['lexeme'])
        return True
        
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
            self.last_ide = self.lookahead['lexeme']
            self.match(self.lookahead['lexeme'])
            return True
        return False
    
    def nro(self):
        if self.lookahead['type'] == 'NRO':
            self.match(self.lookahead['lexeme'])
            return True
        return False

    def simbolo(self):
        if self.lookahead['type'] == 'SIB':
            self.match(self.lookahead['lexeme'])
            return True
        return False

    def negativo(self):
        if self.lookahead['type'] == 'NRO':
            return self.nro()
        if self.lookahead['type'] == 'IDE':
            return self.acessovar()
        return False

    def constantes(self):
        if self.lookahead['lexeme'] == '{':
            self.match('{')
            return self.const()
        return False

    def const(self):
        if self.tipo():
            return self.constalt()
        return False

    def tipo(self):
        if self.lookahead['lexeme'] == 'inteiro':
            self.match('inteiro')
        elif self.lookahead['lexeme'] == 'real':
            self.match('real')
        elif self.lookahead['lexeme'] == 'booleano':
            self.match('booleano')
        elif self.lookahead['lexeme'] == 'cadeia':
            self.match('cadeia')
        elif self.lookahead['lexeme'] == 'char':
            self.match('char')
        elif self.lookahead['lexeme'] == 'registro':
            self.match('registro')
        else:
            return False
        return True

    def constalt(self):
        if self.ide():
            self.save_symbol("CONST")
            if self.varinit():
                return self.constcont()
        return False

    def varinit(self):
        if self.lookahead['lexeme'] in [',',';']:
            return True
        if self.lookahead['lexeme'] == '=':
            self.match('=')
            return self.valor()
        elif self.lookahead['lexeme'] == '[':
            self.match('[')
            ans = self.nro() and self.match(']')
            if ans:
                return self.varinitcont()
        return False

    def varinitcont(self): 
        if self.lookahead['lexeme'] == '=':
            self.match('=')
            if self.match('{'):
                return self.vetor()
        elif self.lookahead['lexeme'] == '[':
            self.match('[')
            ans = self.nro() and self.match(']')
            if ans:
                return self.varinitcontmatr()
        return False

    def varinitcontmatr(self):
        if self.lookahead['lexeme'] == '{':
            self.match('{')
            if self.vetor():
                if self.match(',') and self.match('{'):
                    return self.vetor()
        elif self.lookahead['lexeme'] == '[':
            self.match('[')
            if self.nro():
                ans = self.match(']') and self.match('=') and self.match('{')
                if ans and self.vetor():
                    if self.match(',') and self.match('{'):
                        if self.vetor():
                            if self.match(',') and self.match('{'):
                                return self.vetor()
        return False
            
    def vetor(self):
        if self.valor():
            return self.vetorcont()
        return False

    def vetorcont(self):
        if self.lookahead['lexeme'] == ',':
            self.match(',')
            return self.vetor()
        elif self.lookahead['lexeme'] == '}':
            self.match('}')
            return True
        return False

    def constcont(self):
        if self.lookahead['lexeme'] == ',':
            self.match(',')
            return self.constalt()
        elif self.lookahead['lexeme'] == ';':
            self.match(';')
            return self.constfim()
        return False

    def constfim(self):
        if self.lookahead['lexeme'] == '}':
            return self.match('}')
        return self.const()

    def valor(self):
        if self.lookahead['lexeme'] == '-':
            follow = self.follow(2)
            if follow['type'] in ['REL', 'LOG']:
                return self.expressao()
            elif follow['type'] == 'ART':
                return self.exparitmetica()
            else:
                self.match('-')
                return self.negativo()
        elif self.lookahead['lexeme'] == '(':
            follow = self.follow()       
            i=2
            rel_log = art = False
            while follow['lexeme'] not in [';','}']:
                follow = self.follow(i)      
                if follow['type'] in ['REL','LOG']:
                    rel_log=True
                elif follow['type'] == 'ART':
                    art=True 
                i += 1
            if rel_log:
                return self.expressao()
            elif art:
                return self.exparitmetica()
        elif self.lookahead['type'] == 'CAD':
            return self.match(self.lookahead['lexeme'])
        elif self.lookahead['type'] == 'CAR':
            return self.match(self.lookahead['lexeme'])
        elif self.lookahead['type'] == 'NRO':
            follow = self.follow()
            if follow['type'] in ['REL', 'LOG']:
                return self.expressao()
            elif follow['type'] == 'ART':
                return self.exparitmetica()
            else:
                return self.nro()
        elif self.lookahead['lexeme'] in ['verdadeiro','falso']:
            follow = self.follow()
            if follow['type'] in ['REL', 'LOG']:
                return self.expressao()
            else:
                return self.bool()
        elif self.lookahead['type'] == 'IDE':
            follow = self.follow()
            if follow['type'] in ['REL', 'LOG']:
                return self.expressao()
            elif follow['type'] == 'ART':
                return self.exparitmetica()
            elif follow['lexeme'] == '(':
                self.match(self.lookahead['lexeme'])
                return self.chamadafuncao()
            else:
                return self.acessovar()
        return False
            
    def bool(self):
        if self.lookahead['lexeme'] == 'verdadeiro' or self.lookahead['lexeme'] == 'falso':
            self.match(self.lookahead['lexeme'])
            return True
        return False

    def negativo(self):
        return self.nro() or self.acessovar()

    def variaveis(self):
        if self.lookahead['lexeme'] == '{':
            self.match('{')
            return self.var()
        return False
    
    def var(self):
        ans=False
        if self.tipo():
            if self.ide():
                self.save_symbol("VAR")
                if self.varcont():
                    ans = True
        return ans

    def varalt(self):
        if self.ide():
            self.save_symbol("VAR")
            return self.varcont()        
        return False

    def varcont(self):
        return self.varinit() and self.varfinal()

    def varfinal(self):
        if self.lookahead['lexeme'] == ',':
            self.match(',')
            return self.varalt()
        elif self.lookahead['lexeme'] == ';':
            self.match(';')
            return self.varfim()
        return False

    def varfim(self):
        if self.lookahead['lexeme'] == '}':
            return self.match('}')
        return self.var()

    def registro(self):
        if self.ide():
            if self.match('{'):
                return self.var()
        return False

    def follow_exp(self):
        follow = self.follow()       
        i=1
        rel_log = art = False
        while follow['lexeme'] not in [';','}']:
            follow = self.follow(i)      
            if follow['type'] in ['REL','LOG']:
                rel_log=True
            elif follow['type'] == 'ART':
                art=True 
            i += 1
            if self.i+i >= len(self.input): break
        return rel_log, art

    def expressao(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            rel_log, art = self.follow_exp()
            if art:
                if self.exparitmetica():
                    if self.match(')'):
                        return self.expressaocont()
            elif rel_log:
                if self.expressao():
                    if self.match(')'):
                        return self.expressaocont()
        elif self.lookahead['lexeme'] == '!':
            self.match('!')
            return self.expressaob()
        elif self.lookahead['lexeme'] == '-':
            follow = self.follow(2)
            if follow['type'] == 'ART':
                if self.exparitmetica():
                    return self.expressaocont()
            else:
                self.match('-')
                if self.negativo():
                    return self.expressaocont()
        elif self.lookahead['type'] == 'NRO':
            follow = self.follow()
            if follow['type'] == 'ART':
                if self.exparitmetica():
                    return self.expressaocont()
            else:
                self.nro()
                return self.expressaocont()
        elif self.lookahead['type'] == 'IDE':
            follow = self.follow()
            if follow['type'] == 'ART':
                if self.exparitmetica():
                    return self.expressaocont()
            else:
                if self.acessovar():
                    return self.expressaocont()
        elif self.bool():
            return self.expressaocont()
        elif self.char():
            return self.expressaocont()
        elif self.cadeia():
            return self.expressaocont()
        return False

    def expressaob(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            follow = self.follow()                
            if follow['type'] == 'ART':
                if self.exparitmetica():
                    return self.expressaocont()
            elif self.expressao():
                if self.match(')'):
                    return self.expressaocont()
        elif self.lookahead['type'] == 'IDE':
            follow = self.follow()
            if follow['type'] == 'ART':
                if self.exparitmetica():
                    return self.expressaocont()
            else:
                if self.acessovar():
                    return self.expressaocont()
        elif self.bool():
            return self.expressaocont()
        return False

    def expressaocont(self):
        if self.lookahead['type'] in ['REL', 'LOG']:
            self.match(self.lookahead['lexeme'])
            return self.expressao()
        return True
    
    def para(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            if self.acessovar():
                if self.match('='):
                    if self.expatribuicao():
                        if self.match(';'):
                            return self.paracont()
        return False

    def paracont(self):
        follow = self.follow()
        if self.lookahead['lexeme'] == 'IDE':
            if follow['lexeme'] == ';':
                self.acessovar()
                self.match(';')
                return self.parafim()
        if self.expressao():
            if self.match(';'):
                return self.parafim()
        return False

    def parafim(self):
        if self.lookahead['lexeme'] in ['++','--']:
            if self.expatribuicao():
                return self.function_cont()
        rel_log, art = self.follow_exp()
        if rel_log:
            if self.expressao():
                return self.function_cont()
        elif art:
            follow = self.follow()
            if follow['lexeme'] in ['++','--']:
                if self.expatribuicao():
                    return self.function_cont()
            elif self.exparitmetica():
                return self.function_cont()
        return False
    
    def function_cont(self):
        if self.match(')') and self.match('{'):
            if self.conteudo():
                return self.match('}')
        return False

    def enquanto(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            rel_log, art = self.follow_exp()
            if rel_log:
                if self.expressao():
                    return self.function_cont()
            elif art:
                if self.exparitmetica():
                    return self.function_cont()
            elif self.bool():
                return self.function_cont()
            elif self.acessovar():
                return self.function_cont()
        return False

    def funcao(self):
        if self.lookahead['lexeme'] == 'vazio':
            self.match('vazio')
            if self.tipocont():
                if self.ide():
                    return self.funcaoinit()
        elif self.tipo():
            if self.tipocont():
                if self.ide():
                    return self.funcaoinit()
        return False

    def funcaoinit(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            if self.paraninit():
                if self.match('{'):
                    ans=True
                    while(self.lookahead['lexeme'] != '}' and self.i < len(self.input)-1):
                        result = self.conteudo()
                        if not result:
                            self.error()
                            ans = result
                    return ans and self.match('}')
        return False

    def tipocont(self):
        if self.lookahead['lexeme'] == '[':
            self.match('[')
            if self.match(']'):
                return self.vetormais()
        return True

    def vetormais(self):
        if self.lookahead['lexeme'] == '[':
            self.match('[')
            if self.match(']'):
                return self.vetormaisum()
        return True

    def vetormaisum(self):
        if self.lookahead['lexeme'] == '[':
            self.match('[')
            return self.match(']')
        return True

    def paraninit(self):
        if self.tipo():
            if self.ide():
                return self.paraninitcont()
        elif self.lookahead['lexeme'] == ')':
            return self.match(')')
        return False

    def paraninitcont(self):
        if self.lookahead['lexeme'] == ',':
            self.match(',')
            return self.paraninit()
        return self.match(')')

    def retorno(self):
        if self.valor():
            return self.match(';')
        return False

    def chamadafuncao(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            return self.paran()
        return False
    
    def paran(self):
        if self.lookahead['lexeme'] == ')':
            return self.match(')')
        return self.parancont()

    def parancont(self):
        if self.valor():
            return self.paranfim()
        return False

    def paranfim(self):
        if self.lookahead['lexeme'] == ',':
            self.match(',')
            return self.parancont()
        elif self.lookahead['lexeme'] == ')':
            return self.match(')')