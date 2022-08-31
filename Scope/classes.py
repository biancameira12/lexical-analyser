# Defining Classes

class Var:
    def __init__(self, pType = None, nIndex = None, nSize = None):
        self.pType = pType
        self.nIndex = nIndex
        self.nSize = nSize

class Param:
    def __init__(self, pType = None, nIndex = None, nSize = None):
        self.pType = pType
        self.nIndex = nIndex
        self.nSize = nSize

class Field:
    def __init__(self, pType = None, nIndex = None, nSize = None):
        self.pType = pType
        self.nIndex = nIndex
        self.nSize = nSize

class Function:
    def __init__(self, pRetType = None, pParams = None, nIndex = None, nParams = None, nVars = None):
        self.pRetType = pRetType
        self.pParams = nParams
        self.nIndex = nIndex
        self.nParams = nParams
        self.nVars = nVars       

class Array:
    def __init__(self, pElemType = None, nNumElems = None, nSize = None):
        self.pElemType = pElemType
        self.nNumElems = nNumElems
        self.nSize = nSize

class Struct:
    def __init__(self, pFields = None, nSize = None):
        self.pFields = pFields
        self.nSize = nSize

class Alias:
    def __init__(self, pBaseType = None, nSize = None):
        self.pBaseType = pBaseType
        self.nSize = nSize

class Type:
    def __init__(self, pBaseType = None, nSize = None):
        self.pBaseType = pBaseType
        self.nSize = None

class object:
    def __init__(self, nName = None, pNext = None, eKind = None, _ = None):
        self.nName = nName
        self.pNext = pNext
        self.eKind = eKind
        self._ = None

class ID:
    def __init__(self, object = None, name = None):
        self.object = object
        self.name=name

class T:
    def __init__(self, type = None):
        self.type = type

class E:
    def __init__(self, type = None):
        self.type = type

class L:
    def __init__(self, type = None):
        self.type = type

class R:
    def __init__(self, type = None):
        self.type = type

class Y:
    def __init__(self, type = None):
        self.type = type

class F:
    def __init__(self, type = None):
        self.type = type

class LV:
    def __init__(self, type = None):
        self.type = type

class MC:
    def __init__(self, type = None, param = None, err = None):
        self.type = type
        self.param = param
        self.err = err

class MT:
    def __init__(self, label = None):
        self.label = label   

class ME:
    def __init__(self, label = None):
        self.label = label

class MW:
    def __init__(self, label = None):
        self.label = label

class MA:
    def __init__(self, label = None):
        self.label = label

class LE:
    def __init__(self, type = None, param = None, err = None, n = None):
        self.type = type
        self.param = param
        self.err = err
        self.n = n

class LI:
    def __init__(self, list = None):
        self.list = list

class DC:
    def __init__(self, list = None):
        self.list = list

class LP:
    def __init__(self, list = None):
        self.list = list

class TRU:
    def __init__(self, type = None, val = None):
        self.type = type
        self.val = val

class FALS:
    def __init__(self, type = None, val = None):
        self.type = type
        self.val = val

class CHR:
    def __init__(self, type = None,pos = None, val = None):
        self.type = type
        self.pos = pos
        self.val = val    

class STR:
    def __init__(self, type = None, val = None, pos = None):
        self.type = type
        self.val = val
        self.pos = pos

class NUM:
    def __init__(self, type = None, val = None, pos = None):
        self.type = type
        self.val = val
        self.pos = pos

class t_attrib:
    def __init__(self, t_nont = None, nSize = None, _ = None):
        self.t_nont = t_nont
        self.nSize = nSize
        self._ = _