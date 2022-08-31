from Lexical.LexicalAnalyzer import LexicalAnalyser

file = open('teste.ssl', 'r', encoding = 'utf-8')

lexicalFile = LexicalAnalyser(file)
lexicalFile.Analyse()

file.close()