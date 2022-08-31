from Scope.analyzer import *
from Semantic.analyzer import Semantic_Analysis
from Syntatical.states import *
from Lexical.key_words import *
import csv

TAB_ACTION_GOTO = list(csv.reader(open("action_table.csv","r"), delimiter = "\t"))
TOKEN_TAB_ACTION=[INTEGER, CHAR, BOOLEAN, STRING, TYPE, EQUALS, ARRAY, LEFT_SQUARE, RIGHT_SQUARE, OF, STRUCT,LEFT_BRACES,RIGHT_BRACES,SEMI_COLON,COLON,FUNCTION,LEFT_PARENTHESIS,RIGHT_PARENTHESIS,COMMA,VAR,IF,ELSE,WHILE,DO,BREAK,CONTINUE,AND,OR,LESS_THAN,GREATER_THAN,LESS_OR_EQUAL,GREATER_OR_EQUAL,EQUAL_EQUAL,NOT_EQUAL,PLUS,MINUS,TIMES,DIVIDE,PLUS_PLUS,MINUS_MINUS,NOT,DOT,ID,TRUE,FALSE,CHARACTER,STRINGVAL,NUMERAL,EOF,PLINHA,P,LDE,DE,T,DT,DC,DF,LP,B,LDV,LS,DV,LI,S,U,M,E,L,R,Y,F,LE,LV,IDD,IDU,ID,TRUE,FALSE,CHR,STR,NUM,NB,MF,MC,NF,MT,ME,MW]

def tokenTAB(a):
    return TOKEN_TAB_ACTION.index(a) + 1


class Syntatical_Analysis:
    lexical = None
    syntaticalError = False

    def __init__(self, lexical):
        self.lexical = lexical

    def parse(self):
        generated_code = open("codigo_Gerado.txt", "w")
        generated_code.close()

        if self.lexical.lexicalError:
            return

        STACK = []
        state = 0
        STACK.append(state)
        readToken = self.lexical.next_Token()
        # print(readToken)
        action = TAB_ACTION_GOTO[state+1][tokenTAB(readToken)]
        # print(action)
        
        cont=0
        while action != "acc":
            self.lexical.Lexical_error(readToken)
            if self.lexical.lexicalError == True:
                break

            if action[0] == "s":
                state = int(action[1:])
                STACK.append(state)
                readToken = self.lexical.next_Token()
                action = TAB_ACTION_GOTO[state+1][tokenTAB(readToken)]
                cont+=1
            
            elif action[0] == "r":
                rule = int(action[1:])
                for x in range(RIGHT[rule-1]):
                    STACK.pop()
                try:
                    state = int(TAB_ACTION_GOTO[STACK[-1]+1][tokenTAB(LEFT[rule-1])])
                except:
                    print("Sintaxe Error in line "+str(self.lexical.line))
                    self.syntaticalError = True
                    break
                STACK.append(state)
                action = TAB_ACTION_GOTO[state+1][tokenTAB(readToken)]
                cont+=1
                Semantic_Analysis(self.lexical, rule)
                
            else:
                self.syntaticalError = True
                print("Sintaxe Error in line " + str(self.lexical.line))
                break

