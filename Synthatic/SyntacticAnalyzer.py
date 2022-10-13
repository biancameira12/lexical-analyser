from Lexical.KeyWords import *

TOKEN_TYPES = [INTEGER, CHAR, BOOLEAN, STRING, ID]


class Syntactic_Analysis:
    LEXICAL = None
    NEXT_TOKEN = None
    IS_SYNTACTICAL = True

    def __init__(self, LEXICAL):
        self.LEXICAL = LEXICAL
        NEXT_TOKEN = LEXICAL.GetToken()

    def expr(self):
        ##term()
        token = self.LEXICAL.GetToken()
        while token == PLUS or token == MINUS or token == DIVIDE or token == TIMES:
            ##term()
            print("Exit <expr>")



    def isNewVariable(self):
        NEXT_TOKEN = self.LEXICAL.GetToken()
        if (NEXT_TOKEN != ID):
            self.IS_SYNTACTICAL = False
            print("Not ID:" + str(NEXT_TOKEN))

        NEXT_TOKEN = self.LEXICAL.GetToken()
        if (NEXT_TOKEN != COLON):
            self.IS_SYNTACTICAL = False
            print("Not COLON:" + str(NEXT_TOKEN))

        NEXT_TOKEN = self.LEXICAL.GetToken()
        if (TOKEN_TYPES.count(NEXT_TOKEN) == 0):
            self.IS_SYNTACTICAL = False
            print("Not Type:" + str(NEXT_TOKEN))  

        NEXT_TOKEN = self.LEXICAL.GetToken()
        if (NEXT_TOKEN != SEMI_COLON):
            self.IS_SYNTACTICAL = False
            print("Not SEMI_COLON:" + str(NEXT_TOKEN))  

    def parse(self):

        count = -1
        while (self.IS_SYNTACTICAL and self.NEXT_TOKEN != EOF):
            count += 1
            self.NEXT_TOKEN = self.LEXICAL.GetToken()

            if (self.NEXT_TOKEN == VAR ):
                self.isNewVariable()
                continue      
                


        if (self.IS_SYNTACTICAL):
            print("It s a syntactical file")
        else:
             print("Sintaxe Error in line " + str(count))   
        

