from Synthatic.states import *
from ScopeType.ScopeAnalyzer import *
from ScopeType.rules import *
from ScopeType.classes import *
from ScopeType.types import *

##region global variables
_stack = []
_token = ""
_numSize = ""
_rLabel = ""
_nFuncs = 0
_constPool = 0
##endregion

def SemanticAnalyser(lexical, rule):

    generated_code = open("codeGenerated.txt","w")
    
    global _token,_numSize,_rLabel,_nFuncs,_constPool
    global t,f
    global curFunction
    global SymbolTable
    global IDD_,IDU_,ID_,T_,LI_,LI0_,LI1_,TRU_,FALS_,STR_,CHR_,NUM_,DC_,DC0_,DC1_,LP_,LP0_,LP1_,E_,E0_,E1_,L_,L0_,L1_,R_,R0_,R1_,Y_,Y0_,Y1_,F_,F0_,F1_,LV_,LV0_,LV1_,MC_,LE_,LE0_,LE1_,MT_,ME_,MW_

    p = None

    if rule == IDD_RULE:
        _token = lexical._secondaryToken
        try:
            p = Search(_token)
        except:
            pass
        if p != None:
            Error(lexical, ERR_REDCL)
        else:
            p = Define(_token)
        p.eKind = NO_KIND_DEF_
        IDD_.t_nont = IDD
        IDD_._ = ID(p,_token)
        _stack.append(IDD_)
        return

    if rule == ID_RULE:
        _token = lexical._secondaryToken
        ID_.t_nont=ID
        ID_._=ID(None,_token)
        _stack.append(ID_)
        return

    if rule == IDU_RULE:
        _token = lexical._secondaryToken
        p = Find(_token)
        if p == None:
            Error(lexical, ERR_NO_DECL)
            p = Define(_token)
        IDU_.t_nont = IDU
        IDU_._ = ID(p,_token)
        _stack.append(IDU_)
        return

    if rule == T_IDU_RULE:
        IDU_ = _stack.pop()
        p = IDU_._.object
        if IS_TYPE_KIND(p.eKind) or p.eKind==UNIVERSAL_:
            T_ = t_attrib(T,p._.nSize,T(p))
        else:
            T_ = t_attrib(T,0,T(universal_))
            Error(lexical, ERR_TYPE_EXPECTED)
        _stack.append(T_)
        return

    if rule == T_CHAR_RULE:
        T_ = t_attrib(T,1,T(char_))
        _stack.append(T_)
        return

    if rule == T_INTEGER_RULE:
        T_ = t_attrib(T,1,T(int_))
        _stack.append(T_)
        return

    if rule == T_BOOL_RULE:
        T_ = t_attrib(T,1,T(bool_))
        _stack.append(T_)
        return

    if rule == T_STRING_RULE:
        T_ = t_attrib(T,1,T(string_))
        _stack.append(T_)
        return

    if rule == LI_IDD_RULE:
        IDD_ = _stack.pop()
        LI_ = t_attrib(LI,None,LI(IDD_._.object))
        _stack.append(LI_)
        return

    if rule == LI_COMMA_RULE:
        IDD_ = _stack.pop()
        LI1_ = _stack.pop()
        LI0_ = t_attrib(LI,None,LI(LI1_._.list))
        _stack.append(LI0_)
        return

    if rule == TRUE_RULE:
        TRU_ = t_attrib(TRU, None, TRU(bool_,True))
        _stack.append(TRU_)
        return

    if rule == FALSE_RULE:
        FALS_ = t_attrib(FALS,None,FALS(bool_,False))
        _stack.append(FALS_)
        return

    if rule == CHR_RULE:
        CHR_ = t_attrib(CHR,None,CHR(char_, lexical.GetVariables(lexical._secondaryToken)))
        _stack.append(CHR_)
        return

    if rule == STR_RULE:
        STR_ = t_attrib(STR,None,STR(string_, lexical.GetVariables(lexical._secondaryToken), lexical._secondaryToken))
        _stack.append(STR_)
        return

    if rule == NUM_RULE:
        NUM_ = t_attrib(NUM,None,NUM(int_, lexical.GetVariables(lexical._secondaryToken), lexical._secondaryToken))
        _stack.append(NUM_)
        return

    if rule == DT_ARRAY_RULE:
        T_ = _stack.pop()
        NUM_ = _stack.pop()
        IDD_ = _stack.pop()
        p = IDD_._.object
        _numSize = NUM_._.val
        t = T_._.type
        p.eKind = ARRAY_TYPE_
        p._ = Array(t,_numSize,_numSize*T_.nSize)
        return

    if rule == DT_ALIAS_RULE:
        T_ = _stack.pop()
        IDD_ = _stack.pop()
        p = IDD_._.object
        t = T_._.type
        p.eKind = ALIAS_TYPE_
        p._ = Alias(t,T_.nSize)
        return

    if rule == DC_LI_RULE:
        T_ = _stack.pop()
        LI_ = _stack.pop()
        p = LI_._.list
        t = T_._.type
        _numSize = 0
        while p != None and p.eKind == NO_KIND_DEF_:
            p.eKind = FIELD_
            p._ = Field(t,_numSize,T_.nSize)
            _numSize = _numSize+T_.nSize
            p = p.pNext
        DC_ = t_attrib(DC,_numSize,DC(LI_._.list))
        _stack.append(DC_)
        return

    if rule == DC_DC_RULE:
        T_ = _stack.pop()
        LI_ = _stack.pop()
        DC1_ = _stack.pop()
        p = LI_._.list
        t = T_._.type
        _numSize = DC1_.nSize
        while p != None and p.eKind == NO_KIND_DEF_:
            p.eKind = FIELD_
            p._ = Field(t,_numSize,T_.nSize)
            _numSize = _numSize+T_.nSize
            p = p.pNext
        DC0_ = t_attrib(DC,_numSize,DC(DC1_._.list))
        _stack.append(DC0_)
        return

    if rule == NB_RULE:
        NewBlock()
        return

    if rule == DT_STRUCT_RULE:
        DC_ = _stack.pop()
        IDD_ = _stack.pop()
        p = IDD_._.object
        p.eKind = STRUCT_TYPE_
        p._ = Struct(DC_._.list,DC_.nSize)
        EndBlock()
        return

    if rule == LP_IDD_RULE:
        T_ = _stack.pop()
        IDD_ = _stack.pop()
        p = IDD_._.object
        p.eKind = PARAM_
        p._ = Param(t,0,T_.nSize)
        LP_ = t_attrib(LP,T_.nSize,LP(p))
        _stack.append(LP_)
        return

    if rule == LP_LP_RULE:
        T_ = _stack.pop()
        IDD_ = _stack.pop()
        LP1_ = _stack.pop()
        p = IDD_._.object
        t = T_._.type
        _numSize = LP1_.nSize
        p.eKind = PARAM_
        p._ = Param(t,_numSize,T_.nSize)
        LP0_ = t_attrib(LP,_numSize+T_.nSize,LP(LP1_._.list))
        return

    if rule == NF_RULE:
        IDD_ = _stack[-1]
        f = IDD_._.object
        f.eKind = FUNCTION_
        f._ = Function(None,None,_nFuncs,0,0)
        _nFuncs+=1
        NewBlock()
        return

    if rule == MF_RULE:
        T_ = _stack.pop()
        LP_ = _stack.pop()
        IDD_ = _stack.pop()
        f = IDD_._.object
        f.eKind = FUNCTION_
        f._ = Function(T_._.type,LP_._.list,f._.nIndex,LP_.nSize,LP_.nSize)
        curFunction = f
        generated_code.write("BEGIN_FUNC "+str(f._.nIndex)+" "+str(f._.nParams)+"\n")
        return

    if rule == DF_RULE:
        EndBlock()
        generated_code.write("END_FUNC"+"\n")
        return

    if rule == U_IF_RULE:
        MT_ = _stack.pop()
        E_ = _stack.pop()
        t = E_._.type
        if not CheckTypes(t,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
            generated_code.write("L"+str(MT_._.label)+"\n")
        
    elif rule == U_IF_ELSE_U_RULE:
        ME_ = _stack.pop()
        MT_ = _stack.pop()
        E_ = _stack.pop()
        t = E_._.type
        if not CheckTypes(t,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        generated_code.write("L"+str(ME_._.label)+"\n")
        return

    if rule == M_IF_ELSE_M_RULE:
        ME_ = _stack.pop()
        MT_ = _stack.pop()
        E_ = _stack.pop()
        t = E_._.type
        if not CheckTypes(t,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        generated_code.write("L"+str(ME_._.label)+"\n")
        return

    if rule == M_WHILE_RULE:
        MT_ = _stack.pop()
        E_ = _stack.pop()
        MW_ = _stack.pop()
        print(E_)
        print(E_._)
        t = E_._.type
        if not CheckTypes(t,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        generated_code.write("\tJMP_BW L"+'0'+"\nL"+str(MT_._.label)+"\n")        
        return

    if rule == M_DO_WHILE_RULE:
        E_ = _stack.pop()
        MW_ = _stack.pop()
        t = E_._.type
        if not CheckTypes(t,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        generated_code.write("\tNOT\n\tTJMP_BW L"+str(MW_._.label)+"\n")  
        return

    if rule == E_AND_RULE:
        L_ = _stack.pop()
        E1_ = _stack.pop()
        if not CheckTypes(E1_._.type,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        if not CheckTypes(L_._.type,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        E0_ = t_attrib(E,None,E(bool_))
        _stack.append(E0_)
        generated_code.write("\tAND"+"\n")
        return

    if rule == E_OR_RULE:
        L_ = _stack.pop()
        E1_ = _stack.pop()
        if not CheckTypes(E1_._.type,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        if not CheckTypes(L_._.type,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        E0_ = t_attrib(E,None,E(bool_))
        _stack.append(E0_)
        generated_code.write("\tOR"+"\n")
        return

    if rule == E_L_RULE:
        L_ = _stack.pop()
        E_ = t_attrib(E,None,E(L_._.type))
        _stack.append(E_)
        return

    if rule == L_LESS_THAN_RULE:
        R_ = _stack.pop()
        L1_ = _stack.pop()
        if not CheckTypes(L1_._.type,R_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        L0_ = t_attrib(L,None,L(bool_))
        _stack.append(L0_)
        generated_code.write("\tLT"+"\n")
        return

    if rule == L_GREATER_THAN_RULE:
        R_ = _stack.pop()
        L1_ = _stack.pop()
        if not CheckTypes(L1_._.type,R_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        L0_ = t_attrib(L,None,bool_)
        _stack.append(L0_)
        generated_code.write("\tGT"+"\n")
        return

    if rule == L_LESS_EQUAL_RULE:
        R_ = _stack.pop()
        L1_ = _stack.pop()
        if not CheckTypes(L1_._.type,R_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        L0_ = t_attrib(L,None,bool_)
        _stack.append(L0_)
        generated_code.write("\tLE"+"\n")
        return

    if rule == L_GREATER_EQUAL_RULE:
        R_ = _stack.pop()
        L1_ = _stack.pop()
        if not CheckTypes(L1_._.type,R_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        L0_ = t_attrib(L,None,bool_)
        _stack.append(L0_)
        generated_code.write("\tGE"+"\n")
        return

    if rule == L_EQUAL_EQUAL_RULE:
        R_ = _stack.pop()
        L1_ = _stack.pop()
        if not CheckTypes(L1_._.type,R_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        L0_ = t_attrib(L,None,bool_)
        _stack.append(L0_)
        generated_code.write("\tEQ"+"\n")
        return

    if rule == L_NOT_EQUAL_RULE:
        R_ = _stack.pop()
        L1_ = _stack.pop()
        if not CheckTypes(L1_._.type,R_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        L0_ = t_attrib(L,None,bool_)
        _stack.append(L0_)
        generated_code.write("\tNE"+"\n")
        return

    if rule == L_R_RULE:
        R_ = _stack.pop()
        L_ = t_attrib(L,None,L(R_._.type))
        _stack.append(L_)
        return

    if rule == R_PLUS_RULE:
        Y_ = _stack.pop()
        R1_ = _stack.pop()
        if not CheckTypes(R1_._.type,Y_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        if not CheckTypes(R1_._.type,int_) and not CheckTypes(R1_._.type,string_):
            Error(lexical, ERR_INVALID_TYPE)
        R0_ = t_attrib(R,None,R(R1_._.type))
        _stack.append(R0_)
        generated_code.write("\tADD"+"\n")
        return

    if rule == R_MINUS_RULE:
        Y_ = _stack.pop()
        R1_ = _stack.pop()
        if not CheckTypes(R1_._.type,Y_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        if not CheckTypes(R1_._.type,int_):
            Error(lexical, ERR_INVALID_TYPE)
        R0_ = t_attrib(R,None,R(R1_._.type))
        _stack.append(R0_)
        generated_code.write("\tSUB"+"\n")
        return

    if rule == R_Y_RULE:
        Y_ = _stack.pop()
        R_ = t_attrib(R,None,R(Y_._.type))
        _stack.append(R_)
        return

    if rule == Y_TIMES_RULE:
        F_ = _stack.pop()
        Y1_ = _stack.pop()
        if not CheckTypes(Y1_._.type,F_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        if not CheckTypes(Y1_._.type,int_):
            Error(lexical, ERR_INVALID_TYPE)
        Y0_ = t_attrib(Y,None,Y(Y1_._.type))
        _stack.append(Y0_)
        generated_code.write("\tMUL"+"\n")
        return

    if rule == Y_DIVIDE_RULE:
        F_ = _stack.pop()
        Y1_ = _stack.pop()
        if not CheckTypes(Y1_._.type,F_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        if not CheckTypes(Y1_._.type,int_):
            Error(lexical, ERR_INVALID_TYPE)
        Y0_ = t_attrib(Y,None,Y(Y1_._.type))
        _stack.append(Y0_)
        generated_code.write("\tDIV"+"\n")
        return

    if rule == Y_F_RULE:
        F_ = _stack.pop()
        Y_ = t_attrib(Y,None,Y(F_._.type))
        _stack.append(Y_)
        return

    if rule == F_LV_RULE:
        LV_ = _stack.pop()
        # print(LV_._.type._.nSize)
        # n = LV_._.type._.nSize 
        _numSize = 0
        F_ = t_attrib(F,None,F(LV_._.type))
        _stack.append(F_)
        generated_code.write("\tDE_REF "+str(_numSize)+"\n")
        return

    if rule == F_LEFT_PLUS_PLUS_RULE:
        LV_ = _stack.pop()
        t = LV_._.type
        if not CheckTypes(t,int_):
            Error(lexical, ERR_INVALID_TYPE)
        F_ = t_attrib(F,None,F(int_))
        generated_code.write("\tDUP\n\tDUP\n\tDE_REF 1"+"\n")
        generated_code.write("\tINC\n\tSTORE REF 1\n\tDE_REF 1"+"\n")
        return

    if rule == F_LEFT_MINUS_MINUS_RULE:
        LV_ = _stack.pop()
        t = LV_._.type
        if not CheckTypes(t,int_):
            Error(lexical, ERR_INVALID_TYPE)
        F_ = t_attrib(F,None,F(LV_._.type))
        _stack.append(F_)
        generated_code.write("\tDUP\n\tDUP\n\tDE_REF 1"+"\n")
        generated_code.write("\tDEC\n\tSTORE_REF 1\n\tDE_REF 1"+"\n")
        return

    if rule==F_RIGHT_PLUS_PLUS_RULE:
        LV_ = _stack.pop()
        t = LV_._.type
        if not CheckTypes(t,int_):
            Error(lexical, ERR_INVALID_TYPE)
        F_ = t_attrib(F,None,F(LV_._.type))
        _stack.append(F_)
        generated_code.write("\tDUP\n\tDUP\n\tDE_REF 1"+"\n")
        generated_code.write("\tINC\n\tSTORE_REF 1\n\tDE_REF 1"+"\n")
        generated_code.write("\tDEC"+"\n")
        return

    if rule == F_RIGHT_MINUS_MINUS_RULE:
        LV_ = _stack.pop()
        t = LV_._.type
        if not CheckTypes(t,int_):
            Error(lexical, ERR_INVALID_TYPE)
        F_ = t_attrib(F,None,F(t))
        _stack.append(F_)
        generated_code.write("\tDUP\n\tDUP\n\tDE_REF 1"+"\n")
        generated_code.write("\tDEC\n\tSTORE_REF 1\n\tDE_REF 1"+"\n")
        generated_code.write("\tINC"+"\n")
        return

    if rule == F_PARENTHESIS_E_RULE:
        E_ = _stack.pop()
        F_ = t_attrib(F,None,F(E_._.type))
        _stack.append(F_)
        return

    if rule == F_MINUS_F_RULE:
        F1_ = _stack.pop()
        t = F1_._.type
        if not CheckTypes(t,int_):
            Error(lexical, ERR_INVALID_TYPE)
        F0_ = t_attrib(F,None,F(t))
        _stack.append(F0_)
        generated_code.write("\tNEG"+"\n")
        return

    if rule == F_NOT_F_RULE:
        F1_ = _stack.pop()
        t = F1_._.type
        if not CheckTypes(t,bool_):
            Error(lexical, ERR_INVALID_TYPE)
        F0_ = t_attrib(F,None,F(t))
        _stack.append(F0_)
        generated_code.write("\tNOT"+"\n")
        return

    if rule == F_TRUE_RULE:
        TRU_ = _stack.pop()
        F_ = t_attrib(F,None,F(bool_))
        _stack.append(F_)
        generated_code.write("\tLOAD_TRUE"+"\n")
        return

    if rule == F_FALSE_RULE:
        FALS_ = _stack.pop()
        F_ = t_attrib(F,None,F(bool_))
        _stack.append(F_)
        generated_code.write("\tLOAD_FALSE"+"\n")
        return

    if rule == F_CHR_RULE:
        CHR_ = _stack.pop()
        F_ = t_attrib(F,None,F(char_))
        _stack.append(F_)
        _numSize = lexical._secondaryToken
        generated_code.write("\tLOAD_CONST "+str(constPool)+"\n")
        constPool+=1
        return

    if rule == F_STR_RULE:
        STR_ = _stack.pop()
        F_ = t_attrib(F,None,F(string_))
        _stack.append(F_)
        _numSize = lexical._secondaryToken
        generated_code.write("\tLOAD_CONST "+str(constPool)+"\n")
        constPool+=1
        return

    if rule == F_NUM_RULE:
        NUM_ = _stack.pop()
        F_ = t_attrib(F,None,F(int_))
        _stack.append(F_)
        _numSize = lexical._secondaryToken
        generated_code.write("\tLOAD_CONST "+str(constPool)+"\n")
        constPool+=1
        return

    if rule == LV_DOT_RULE:
        ID_ = _stack.pop()
        LV1_ = _stack.pop()
        t = LV1_._.type
        if t.eKind != STRUCT_TYPE_:
            if t.eKind != UNIVERSAL_:
                Error(lexical, ERR_KIND_NOT_STRUCT)
            LV0_ = t_attrib(LV,None,LV(universal_))
        else:
            p = t._.pFields
            while p != None:
                if p.aName == ID_._.name:
                    break
                p = p.pNext
            if p == None:
                Error(lexical, ERR_FIELD_NOT_DECL)
                LV0_ = t_attrib(LV,None,LV(universal_))
            else:
                LV0_ = t_attrib(LV,None,LV(p._.pType))
                LV0_._.type._ = Type(None,p._.nSize)
        _stack.append(LV0_)
        generated_code.write("\tADD "+str(p._.nIndex)+"\n")
        return

    if rule == LV_SQUARE_RULE:
        E_ = _stack.pop()
        LV1_ = _stack.pop()
        t = LV1_._.type
        if CheckTypes(t,string_):
            LV0_ = t_attrib(LV,None,LV(char_))
        elif t.eKind!=ARRAY_TYPE_:
            if t.eKind != UNIVERSAL_:
                Error(lexical, ERR_KIND_NOT_ARRAY)
            LV0_ = t_attrib(LV,None,LV(universal_))
        else:
            LV0_ = t_attrib(LV,None,LV(t._.tipoElemento))
            _numSize = t._tipoElemento._.nSize
            generated_code.write("\tMUL "+str(_numSize)+"\n")
            generated_code.write("\tADD"+"\n")
        if not CheckTypes(E_._.type,int_):
            Error(lexical, ERR_INVALID_INDEX_TYPE)
        _stack.append(LV0_)
        return

    if rule == LV_IDU_RULE:
        IDU_ = _stack.pop()
        p = IDU_._.object
        if p.eKind != VAR_ and p.eKind!=PARAM_:
            if p.eKind != UNIVERSAL_:
                Error(lexical, ERR_KIND_NOT_VAR)
            LV_ = t_attrib(LV,None,LV(universal_))
        else:
            LV_ = t_attrib(LV,None,LV(p._.tipo))
            LV_._.type._ = Type(None,p._.nSize)
            generated_code.write("\tLOAD_REF "+str(p._.nIndex)+"\n")
        _stack.append(LV_)
        return

    if rule == MC_RULE:
        IDU_ = _stack[-1]
        f = IDU_._.object
        if f.eKind != FUNCTION_:
            MC_ = t_attrib(MC,None,MC(universal_,None,True))
        else:
            MC_ = t_attrib(MC,None,MC(f._.pRetType,f._.pParams,False))
        _stack.append(MC_)
        return

    if rule == LE_E_RULE:
        E_ = _stack.pop()
        MC_ = _stack[-1]
        LE_ = t_attrib(LE,None,LE(None,None,MC_._.err,1))
        if not MC_._.err:
            p=MC_._.param 
            if p == None:
                Error(lexical, ERR_TOO_MANY_ARG)
                LE_._.err = True
            else:
                if not CheckTypes(p._.tipo,E_._.type):
                    Error(lexical, ERR_PARAM_TYPE)
                LE_._.param = p.pNext
                LE_._.n = _numSize + 1
        _stack.append(LE_)
        return

    if rule == LE_LE_RULE:
        E_ = _stack.pop()
        LE1_ = _stack.pop()
        LE0_ = t_attrib(LE,None,LE(None,None,L1_._.err,LE1_._.n))
        if not LE1_._.err:
            p = LE1_._.param
            if p == None:
                Error(lexical, ERR_TOO_MANY_ARG)
                LE0_._.err = True
            else:
                if not CheckTypes(p._.tipo,E_._.type):
                    Error(lexical, ERR_PARAM_TYPE)
                LE0_._.param = p.pNext
                LE0_._.n = _numSize+1
        _stack.append(LE0_)
        return

    if rule == F_IDU_MC_RULE:
        LE_ = _stack.pop()
        MC_ = _stack.pop()
        IDU_ = _stack.pop()
        f = IDU_._.object
        F_ = t_attrib(F,None,F(MC_._.type))
        if not LE_._.err:
            if LE_._.n-1 < f._nParams and LE_._.n != 0:
                Error(lexical, ERR_TOO_FEW_ARGS)
            elif LE_._.n-1 > f._.nParams:
                Error(lexical, ERR_TOO_MANY_ARG)
        _stack.append(F_)
        generated_code.write("\tCALL "+str(f._.nIndex)+"\n")
        return

    if rule == MT_RULE:
        _rLabel = newLabel()
        MT_ = t_attrib(MT,None,MT(_rLabel))
        _stack.append(MT_)
        generated_code.write("\tTJMP_FW L"+str(_rLabel)+"\n")
        return

    if rule == ME_RULE:
        MT_ = _stack[-1]
        _rLabel = newLabel()
        ME_._.label = _rLabel
        ME_.t_nont = ME
        _stack.append(ME_)
        generated_code.write("\tTJMP_FW L"+str(_rLabel)+"\n")
        generated_code.write("L"+str(MT_._.label)+"\n")
        return

    if rule == MW_RULE:
        _rLabel = newLabel()
        print(MW_)
        MW_ = _stack.pop() ##
        print(MW_._)
        MW_._.label = _rLabel
        _stack.append(MW_)
        generated_code.write("L"+str(_rLabel)+"\n")
        return

    if rule==M_BREAK_RULE:
        MT_ = _stack[-1]
        return
        return

    if rule == M_CONTINUE_RULE:
        pass
        return

    if rule == M_E_SEMICOLON:
        E_ = _stack.pop()
        LV_ = _stack.pop()
        if not CheckTypes(LV_._.type,E_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        t = LV_._.type
        E0_._ = F(E_._.type)
        _stack.append(E0_)
        if t._ == None or t._.nSize == None:
            generated_code.write("\tSTORE_REF 1\n")
        else:
            generated_code.write("\tSTORE_REF "+str(t._.nSize)+"\n")

    generated_code.close()