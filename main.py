from Lexical.analyzer import LexicalAnalyser
from Syntatical.analyzer import Syntatical_Analysis

file = open('codigo-teste-1.ssl', 'r', encoding = 'utf-8')

lexical = LexicalAnalyser(file)
lexical.run()

file.close()