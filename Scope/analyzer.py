from Lexical.analyzer import *
from Scope.rules import *
from Scope.classes import *
from Scope.types import *

def IS_TYPE_KIND(eKind):
    return (eKind == ARRAY_TYPE_ or eKind == STRUCT_TYPE_ or eKind == ALIAS_TYPE_ or eKind == SCALAR_TYPE_)

global SymbolTable
SymbolTable = []
global SymbolTableLast
SymbolTableLast = []
global nCurrentLevel
nCurrentLevel = 0

global labelNo
labelNo = 0
global nFuncs
nFuncs = 0
global constPool
constPool = 0
global curFunction
curFunction = object()

int_ = object(-1, None, SCALAR_TYPE_, Type(None,1))
char_ = object(-1, None, SCALAR_TYPE_, Type(None,1))
bool_ = object(-1, None, SCALAR_TYPE_, Type(None,1))
string_ = object(-1, None, SCALAR_TYPE_, Type(None,1))
universal_ = object(-1, None, SCALAR_TYPE_, Type(None,1))

def newLabel():
    global labelNo
    labelNo+=1
    return labelNo - 1

def NewBlock():
    global nCurrentLevel
    global SymbolTable
    global SymbolTableLast
    nCurrentLevel+=1
    SymbolTable.append(None)
    SymbolTableLast.append(None)
    return nCurrentLevel

def EndBlock():
    global nCurrentLevel
    nCurrentLevel-=1
    return nCurrentLevel

def Define(aName):
    global SymbolTable
    global SymbolTableLast
    obj = object(aName,None)
    try:
        a = SymbolTable[nCurrentLevel]
    except:
        SymbolTable.append(None)
    try:
        a = SymbolTableLast[nCurrentLevel]
    except:
        SymbolTableLast.append(None)

    if SymbolTable[nCurrentLevel] == None:
        SymbolTable[nCurrentLevel] = obj
        SymbolTableLast[nCurrentLevel] = obj
    else:
        aux = SymbolTable[nCurrentLevel]
        while True:
            if aux.pNext == None:
                aux.pNext = obj
                SymbolTableLast[nCurrentLevel] = obj
                break
            else:
                aux = aux.pNext
    return obj

def Search(aName):
    global SymbolTable
    obj = SymbolTable[nCurrentLevel]
    while obj != None:
        if obj.nName == aName:
            break
        else:
            obj = obj.pNext
    return obj

def Find(aName):
    global SymbolTable
    obj = None
    for i in range(nCurrentLevel+1):
        obj = SymbolTable[i]
        while obj != None:
            if obj.nName == aName:
                break
            else:
                obj = obj.pNext
        if obj != None:
            break
    return obj

def Error(lexical, code):
    has_Err = True
    print("Line: " + str(lexical.line)+" - ")
    if code == ERR_NO_DECL:
        print("Variable not declared")
    elif code == ERR_REDCL:
        print("Variable already declared")
    elif code == ERR_TYPE_EXPECTED:
        print("Type not declared")
    elif code == ERR_BOOL_TYPE_EXPECTED:
        print("Expected Type boolean")
    elif code == ERR_INVALID_TYPE:
        print("Invalid Type for this operation")
    elif code == ERR_TYPE_MISMATCH:
        print("Invalid Type for this operation")
    elif code == ERR_KIND_NOT_STRUCT:
        print("Only Struct Types are allowed for this operation")
    elif code == ERR_FIELD_NOT_DECL:
        print("Field not declared")
    elif code == ERR_KIND_NOT_ARRAY:
        print("Only Array Types are allowed for this operation")
    elif code == ERR_INVALID_INDEX_TYPE:
        print("Invalid Index for Array")
    elif code == ERR_KIND_NOT_VAR:
        print("Only Var Types are allowed for this operation")
    elif code == ERR_KIND_NOT_FUNCTION:
        print("Only Function Types are allowed for this operation")
    elif code == ERR_TOO_FEW_ARGS:
        print("Number of parameters less than the specified value")
    elif code == ERR_TOO_MANY_ARG:
        print("Number of parameters greater than the specified value")
    elif code == ERR_PARAM_TYPE:
        print("Invalid Specified Type")
    elif code == ERR_RETURN_TYPE_MISMATCH:
        print("Return Type not compatible with the specified function return Type")

def CheckTypes(t1,t2):
    if t1 == t2:
        return True
    elif t1 == universal_ or t2 == universal_:
        return True
    elif t1.eKind == UNIVERSAL_ or t2.eKind == UNIVERSAL_:
        return True
    elif t1.eKind == ALIAS_TYPE_ and t2.eKind != ALIAS_TYPE_:
        return CheckTypes(t1._.pBaseType,t2)
    elif t1.eKind != ALIAS_TYPE_ and t2.eKind == ALIAS_TYPE_:
        return CheckTypes(t1,t2._.pBaseType)
    elif t1.eKind == t2.eKind:
        if t1.eKind == ALIAS_TYPE_:
            return CheckTypes(t1._.pBaseType,t2._.pBaseType)
        elif t1.eKind == ARRAY_TYPE_:
            if t1._.nNumElems == t2._.nNumElems:
                return CheckTypes(t1._.pElemType,t2._.pElemType)
        elif t1.eKind == STRUCT_TYPE_:
            f1 = t1._.pFields
            f2 = t2._.pFields
            while f1 != None and f2 != None:
                if not CheckTypes(f1._.pType,f2._.pType):
                    return False
            return (f1 == None and f2 == None)
    else:
        return False

def print_SymbolTable():
    global SymbolTable
    if len>0:
        obj = SymbolTable[nCurrentLevel]
        print("SymbolTable:")
        while obj != None:
            print(obj.nName)
            obj = obj.pNext

