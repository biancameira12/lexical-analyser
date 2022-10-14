from Lexical.KeyWords import *
from Synthatic.states import *
import csv

TAB_ACTION_GOTO = list(csv.reader(open("actionTableTreated.csv","r"), delimiter = ","))
LEFT = [B, CHR, DC, DC, DE, DE, DF, DT, DT, DT, DV, E, E, E, F, F, F, F, F, F, F, F, F, F, F, F, F, F, FALSE, IDD, IDU, L, L, L, L, L, L, L, LDE, LDE, LDV, LDV, LE, LE, LI, LI, LP, LP, LS, LS, LV, LV, LV, NUM, P, R, R, R, S, S, S, S, S, S, S, S, STR, T, T, T, T, T, TRUE, Y, Y, Y,]
LEN = [4,1,5,3,1,1,8,9,7,4,5,3,3,1,1,2,2,2,2,3,4,2,2,1,1,1,1,1,1,1,1,3,3,3,3,3,3,1,2,1,2,1,3,1,3,1,5,3,2,1,3,4,1,1,1,3,3,1,5,7,5,7,1,4,2,2,1,1,1,1,1,1,1,3,3,1]

class Syntactic_Analysis:
    LEXICAL = None
    NEXT_TOKEN = None
    IS_SYNTACTICAL = True
    FILO = [0]

    def __init__(self, LEXICAL):
        self.LEXICAL = LEXICAL
        for i in range (len(TAB_ACTION_GOTO)):
            for j in range (len(TAB_ACTION_GOTO[0])):
                if (TAB_ACTION_GOTO[i][j] == ''):
                    TAB_ACTION_GOTO[i][j] = 0
                else:
                    TAB_ACTION_GOTO[i][j] = int(TAB_ACTION_GOTO[i][j])
        
    def parse(self):

        q = 0
        self.NEXT_TOKEN = self.LEXICAL.GetToken()
        try:
            while (self.IS_SYNTACTICAL):
                print ("Token:")
                action = TAB_ACTION_GOTO[q][self.NEXT_TOKEN]
                
                if action > 0:
                    self.FILO.append(action)
                    self.NEXT_TOKEN = self.LEXICAL.GetToken()
                elif action < 0:
                    for i in range ((LEN[(-1)*action])):
                        self.FILO.pop()
                    self.FILO.append(TAB_ACTION_GOTO[self.FILO[-1]][LEFT[action]])
                else:
                    self.IS_SYNTACTICAL = False
                    break 

                if (len(self.FILO) == 0):
                    break   

                q = self.FILO[-1]  
        except(ValueError):
            print("ValueError")
            self.IS_SYNTACTICAL = False


        if (self.IS_SYNTACTICAL):
            print("It s a syntactical file")
        else:
             print("Sintaxe Error in line ")   
        

