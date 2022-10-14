from operator import truediv
from Lexical.keyWords import *
import string

KEY_WORDS = ["array", "boolean", "break", "char", "continue", "do", "else", "false", "function", "if", "integer", "of", "string", "struct", "true", "type", "var", "while"]

class LexicalAnalyser:
    _isLexical = True
    _nextChar = " "
    _line = 1
    _char = 1
    _arq = None

    _variables = []
    _identifiers = []

    _secondaryToken = None

    def __init__(self, file):
        file.seek(0)
        self._arq = file

    def SearchKeyWord(self, name): 
        try:
            index = KEY_WORDS.index(name)
            return index
        except(ValueError):
            return ID
    
    def GetVariables(self, c):
        return self._variables[c]

    def AddVariable(self, c):
        self._variables.append(c)
        return len(self._variables)-1

    def NextCharIsSymbol(self):

        if self._nextChar == "\'":
            token = CHARACTER
            self._nextChar = self._arq.read(1)
            self._char+=1
            self._secondaryToken = self.AddVariable(self._nextChar)
            self._nextChar = self._arq.read(2) 
            self._char+=2
        elif self._nextChar == ":":
            token = COLON
            self._nextChar = self._arq.read(1)
            self._char+=1
        elif self._nextChar == "+":
            self._nextChar = self._arq.read(1)
            self._char+=1
            if self._nextChar == "+":
                token = PLUS_PLUS
                self._nextChar = self._arq.read(1)
                self._char+=1
            else:
                token = PLUS

        elif self._nextChar == "-":
            self._nextChar = self._arq.read(1)
            self._char+=1
            if self._nextChar == "-":
                token = MINUS_MINUS
                self._nextChar = self._arq.read(1)
                self._char+=1
            else:
                token = MINUS

        elif self._nextChar == ";":
            token = SEMI_COLON
            self._nextChar = self._arq.read(1)
            self._char+=1

        elif self._nextChar == ",":
            token = COMMA
            self._nextChar = self._arq.read(1)
            self._char+=1

        elif self._nextChar == "=":
            self._nextChar = self._arq.read(1)
            self._char+=1
            if self._nextChar == "=":
                token = EQUAL_EQUAL
                self._nextChar = self._arq.read(1)
                self._char+=1
            else:
                token = EQUALS

        elif self._nextChar == "[":
            token = LEFT_SQUARE
            self._nextChar = self._arq.read(1)
            self._char+=1

        elif self._nextChar == "]":
            token = RIGHT_SQUARE
            self._nextChar = self._arq.read(1)
            self._char+=1

        elif self._nextChar == "{":
            token = LEFT_BRACES
            self._nextChar = self._arq.read(1)
            self._char+=1

        elif self._nextChar == "}":
            token = RIGHT_BRACES
            self._nextChar = self._arq.read(1)
            self._char+=1

        elif self._nextChar == "(":
            token = LEFT_PARENTHESIS
            self._nextChar = self._arq.read(1)
            self._char+=1

        elif self._nextChar == ")":
            token = RIGHT_PARENTHESIS
            self._nextChar = self._arq.read(1)
            self._char+=1

        elif self._nextChar == "&":
            self._nextChar = self._arq.read(1)
            self._char+=1
            if self._nextChar == "&":
                token = AND
                self._nextChar=self._arq.read(1)
                self._char+=1
            else:
                token = UNKNOWN

        elif self._nextChar == "|":
            self._nextChar = self._arq.read(1)
            self._char+=1
            if self._nextChar == "|":
                token = OR
                self._nextChar = self._arq.read(1)
                self._char+=1
            else:
                token = UNKNOWN

        elif self._nextChar == "<":
            self._nextChar=self._arq.read(1)
            self._char+=1
            if self._nextChar == "=":
                token = LESS_OR_EQUAL
                self._nextChar = self._arq.read(1)
                self._char+=1
            else:
                token=LESS_THAN

        elif self._nextChar == ">":
            self._nextChar = self._arq.read(1)
            self._char+=1
            if self._nextChar == "=":
                token = GREATER_OR_EQUAL
                self._nextChar = self._arq.read(1)
                self._char+=1
            else:
                token = GREATER_THAN

        elif self._nextChar == "!":
            self._nextChar = self._arq.read(1)
            self._char+=1
            if self._nextChar == "=":
                token = NOT_EQUAL
                self._nextChar = self._arq.read(1)
                self._char+=1
            else:
                token = NOT 

        elif self._nextChar == "*":
            token = TIMES
            self._nextChar = self._arq.read(1)
            self._char+=1

        elif self._nextChar == ".":
            self._nextChar = self._arq.read(1)
            self._char+=1
            token = DOT        
        elif self._nextChar == "/":
            token = DIVIDE
            self._nextChar = self._arq.read(1)
            self._char+=1
        else:
            token = UNKNOWN
            self._nextChar = self._arq.read(1)
            self._char+=1  

        return token

    def SearchName(self, name): 
        if name not in self._identifiers:
            self._identifiers.append(name) 
        return self._identifiers.index(name)

    def GetToken(self):
        sep = ""
        while IsSpace(self._nextChar):
            if IsLineBreak(self._nextChar):
                self._line+=1
            self._nextChar = self._arq.read(1)
            self._char+=1
        
        if self._nextChar == "":
            token = EOF
        
        elif IsDigit(self._nextChar):
            num_Aux = []
            while IsDigit(self._nextChar):
                num_Aux.append(self._nextChar)
                self._nextChar = self._arq.read(1)
                self._char+=1
            num = sep.join(num_Aux)
            token = NUMERAL
            self._secondaryToken = self.AddVariable(num)

        elif IsAlnum(self._nextChar):
            text_Aux = []
            while IsAlnum(self._nextChar) or self._nextChar == '_':
                text_Aux.append(self._nextChar)
                self._nextChar = self._arq.read(1)
                self._char+=1
            text = sep.join(text_Aux)
            token = self.SearchKeyWord(text)
            if token == ID:
                self._secondaryToken = self.SearchName(text)
        
        
        elif self._nextChar == "\"":
            string_Aux = []
            string_Aux.append(self._nextChar)
            self._nextChar = self._arq.read(1)
            self._char+=1

            while(self._nextChar != "\""):
                string_Aux.append(self._nextChar)
                self._nextChar = self._arq.read(1)
                self._char+=1

            string_Aux.append(self._nextChar)
            self._nextChar = self._arq.read(1)
            self._char+=1
            string = sep.join(string_Aux)
            token = STRING
            self._secondaryToken = self.AddVariable(string)
        
        else:
            token = self.NextCharIsSymbol()

        return token

    def IsLexicalError(self, token):
        if token == UNKNOWN:
            self._isLexical = False
            print("Character "+str(self._char+1)+" not expected, line:" + str(self._line))

    def Analyse(self):
        self._nextChar = self._arq.read(1)
        token_Aux = self.GetToken()
        while token_Aux != EOF:
            self.IsLexicalError(token_Aux)
            token_Aux = self.GetToken()
        if self._isLexical == True:
            print ("It is a lexical file")
        else:
            print ("It is not a lexical file")

## region auxiliar functions

def IsSpace(c):
    return [chr(10), chr(13), "\f", "\v", "\t"," "].count(c) != 0

def IsLineBreak(c):
    return ["\n", "\r"].count(c) != 0

def IsDigit(c):
    return "0123456789".count(c) != 0

def IsAlnum(c):
    return string.ascii_letters.count(c) != 0

## end region