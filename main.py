from Lexical.LexicalAnalyzer import LexicalAnalyser
from Synthatic.SyntacticAnalyzer import Syntactic_Analysis

file = open('teste.ssl', 'r', encoding = 'utf-8')

lexicalFile = LexicalAnalyser(file)
syntatical = Syntactic_Analysis(lexicalFile)
syntatical.parse()
lexicalFile.Analyse()

file.close()