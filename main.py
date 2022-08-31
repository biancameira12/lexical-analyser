from Lexical.analyzer import LexicalAnalyser

file = open('codigo-teste.ssl', 'r', encoding = 'utf-8')

lexicalFile = LexicalAnalyser(file)
lexicalFile.analyse()

file.close()