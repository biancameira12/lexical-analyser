from Syntatical.states import *
from Scope.analyzer import *
from Scope.rules import *
from Scope.classes import *
from Scope.types import *

name = ""
n = ""
rLabel = ""

hasErr = False
StackSem = []

def Semantic_Analysis(lexical, rule):

    generated_code = open("codigo_Gerado.txt","a+")
    
    global name,n,rLabel
    global t,f
    global IDD_,IDU_,ID_,T_,LI_,LI0_,LI1_,TRU_,FALS_,STR_,CHR_,NUM_,DC_,DC0_,DC1_,LP_,LP0_,LP1_,E_,E0_,E1_,L_,L0_,L1_,R_,R0_,R1_,Y_,Y0_,Y1_,F_,F0_,F1_,LV_,LV0_,LV1_,MC_,LE_,LE0_,LE1_,MT_,ME_,MW_
    global nFuncs
    global curFunction
    global constPool
    global SymbolTable
    p = None

    if rule == IDD_RULE:
        name = lexical.secondary_Token
        try:
            p = Search(name)
        except:
            pass
        if p != None:
            Error(lexical, ERR_REDCL)
        else:
            p = Define(name)
        p.eKind = NO_KIND_DEF_
        IDD_.t_nont = IDD
        IDD_._ = ID(p,name)
        StackSem.append(IDD_)

    elif rule == IDU_RULE:
        name = lexical.secondary_Token
        p = Find(name)
        if p == None:
            Error(lexical, ERR_NO_DECL)
            p = Define(name)
        IDU_.t_nont = IDU
        IDU_._ = ID(p,name)
        StackSem.append(IDU_)

    elif rule == ID_RULE:
        name = lexical.secondary_Token
        ID_.t_nont=ID
        ID_._=ID(None,name)
        StackSem.append(ID_)

    elif rule == T_IDU_RULE:
        IDU_ = StackSem.pop()
        p = IDU_._.object
        if IS_TYPE_KIND(p.eKind) or p.eKind==UNIVERSAL_:
            T_ = t_attrib(T,p._.nSize,T(p))
        else:
            T_ = t_attrib(T,0,T(universal_))
            Error(lexical, ERR_TYPE_EXPECTED)
        StackSem.append(T_)

    elif rule == T_INTEGER_RULE:
        T_ = t_attrib(T,1,T(int_))
        StackSem.append(T_)

    elif rule == T_CHAR_RULE:
        T_ = t_attrib(T,1,T(char_))
        StackSem.append(T_)

    elif rule == T_BOOL_RULE:
        T_ = t_attrib(T,1,T(bool_))
        StackSem.append(T_)

    elif rule == T_STRING_RULE:
        T_ = t_attrib(T,1,T(string_))
        StackSem.append(T_)

    elif rule == LI_IDD_RULE:
        IDD_ = StackSem.pop()
        LI_ = t_attrib(LI,None,LI(IDD_._.object))
        StackSem.append(LI_)
    
    elif rule == LI_COMMA_RULE:
        IDD_ = StackSem.pop()
        LI1_ = StackSem.pop()
        LI0_ = t_attrib(LI,None,LI(LI1_._.list))
        StackSem.append(LI0_)
    
    #elif rule == DV_VAR_RULE:
    #    T_ = StackSem.pop()
    #    t = T_._.type
    #    LI_ = StackSem.pop()
    #    p = LI_._.list
    #    n = curFunction._.nVars
    #    while p != None and p.eKind == NO_KIND_DEF_:
    #        p.eKind = VAR_
    #        p._ = Var(t,n,T_.nSize)
    #        n+=T_.nSize
    #        p = p.pNext
    #    curFunction._.nVars=n

    elif rule == TRUE_RULE:
        TRU_ = t_attrib(TRU, None, TRU(bool_,True))
        StackSem.append(TRU_)

    elif rule == FALSE_RULE:
        FALS_ = t_attrib(FALS,None,FALS(bool_,False))
        StackSem.append(FALS_)

    elif rule == CHR_RULE:
        CHR_ = t_attrib(CHR,None,CHR(char_, lexical.get_Cte(lexical.secondary_Token)))
        StackSem.append(CHR_)
    
    elif rule == STR_RULE:
        STR_ = t_attrib(STR,None,STR(string_, lexical.get_Cte(lexical.secondary_Token), lexical.secondary_Token))
        StackSem.append(STR_)
    
    elif rule == NUM_RULE:
        NUM_ = t_attrib(NUM,None,NUM(int_, lexical.get_Cte(lexical.secondary_Token), lexical.secondary_Token))
        StackSem.append(NUM_)

    elif rule == DT_ARRAY_RULE:
        T_ = StackSem.pop()
        NUM_ = StackSem.pop()
        IDD_ = StackSem.pop()
        p = IDD_._.object
        n = NUM_._.val
        t = T_._.type
        p.eKind = ARRAY_TYPE_
        p._ = Array(t,n,n*T_.nSize)

    elif rule == DT_ALIAS_RULE:
        T_ = StackSem.pop()
        IDD_ = StackSem.pop()
        p = IDD_._.object
        t = T_._.type
        p.eKind = ALIAS_TYPE_
        p._ = Alias(t,T_.nSize)

    elif rule == DC_LI_RULE:
        T_ = StackSem.pop()
        LI_ = StackSem.pop()
        p = LI_._.list
        t = T_._.type
        n = 0
        while p != None and p.eKind == NO_KIND_DEF_:
            p.eKind = FIELD_
            p._ = Field(t,n,T_.nSize)
            n = n+T_.nSize
            p = p.pNext
        DC_ = t_attrib(DC,n,DC(LI_._.list))
        StackSem.append(DC_)
    
    elif rule == DC_DC_RULE:
        T_ = StackSem.pop()
        LI_ = StackSem.pop()
        DC1_ = StackSem.pop()
        p = LI_._.list
        t = T_._.type
        n = DC1_.nSize
        while p != None and p.eKind == NO_KIND_DEF_:
            p.eKind = FIELD_
            p._ = Field(t,n,T_.nSize)
            n = n+T_.nSize
            p = p.pNext
        DC0_ = t_attrib(DC,n,DC(DC1_._.list))
        StackSem.append(DC0_)
    
    elif rule == NB_RULE:
        NewBlock()

    elif rule == DT_STRUCT_RULE:
        DC_ = StackSem.pop()
        IDD_ = StackSem.pop()
        p = IDD_._.object
        p.eKind = STRUCT_TYPE_
        p._ = Struct(DC_._.list,DC_.nSize)
        EndBlock()

    elif rule == LP_IDD_RULE:
        T_ = StackSem.pop()
        IDD_ = StackSem.pop()
        p = IDD_._.object
        p.eKind = PARAM_
        p._ = Param(t,0,T_.nSize)
        LP_ = t_attrib(LP,T_.nSize,LP(p))
        StackSem.append(LP_)
    
    elif rule == LP_LP_RULE:
        T_ = StackSem.pop()
        IDD_ = StackSem.pop()
        LP1_ = StackSem.pop()
        p = IDD_._.object
        t = T_._.type
        n = LP1_.nSize
        p.eKind = PARAM_
        p._ = Param(t,n,T_.nSize)
        LP0_ = t_attrib(LP,n+T_.nSize,LP(LP1_._.list))
    
    elif rule == NF_RULE:
        IDD_ = StackSem[-1]
        f = IDD_._.object
        f.eKind = FUNCTION_
        f._ = Function(None,None,nFuncs,0,0)
        nFuncs+=1
        NewBlock()

    elif rule == MF_RULE:
        T_ = StackSem.pop()
        LP_ = StackSem.pop()
        IDD_ = StackSem.pop()
        f = IDD_._.object
        f.eKind = FUNCTION_
        f._ = Function(T_._.type,LP_._.list,f._.nIndex,LP_.nSize,LP_.nSize)
        curFunction = f
        generated_code.write("BEGIN_FUNC "+str(f._.nIndex)+" "+str(f._.nParams)+"\n")

    elif rule == DF_RULE:
        EndBlock()
        generated_code.write("END_FUNC"+"\n")

    elif rule == U_IF_RULE:
        MT_ = StackSem.pop()
        E_ = StackSem.pop()
        t = E_._.type
        if not CheckTypes(t,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
            generated_code.write("L"+str(MT_._.label)+"\n")
        
    elif rule == U_IF_ELSE_U_RULE:
        ME_ = StackSem.pop()
        MT_ = StackSem.pop()
        E_ = StackSem.pop()
        t = E_._.type
        if not CheckTypes(t,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        generated_code.write("L"+str(ME_._.label)+"\n")

    elif rule == M_IF_ELSE_M_RULE:
        ME_ = StackSem.pop()
        MT_ = StackSem.pop()
        E_ = StackSem.pop()
        t = E_._.type
        if not CheckTypes(t,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        generated_code.write("L"+str(ME_._.label)+"\n")

    elif rule == M_WHILE_RULE:
        MT_ = StackSem.pop()
        E_ = StackSem.pop()
        MW_ = StackSem.pop()
        print(E_)
        print(E_._)
        t = E_._.type
        if not CheckTypes(t,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        generated_code.write("\tJMP_BW L"+'0'+"\nL"+str(MT_._.label)+"\n")        

    elif rule == M_DO_WHILE_RULE:
        E_ = StackSem.pop()
        MW_ = StackSem.pop()
        t = E_._.type
        if not CheckTypes(t,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        generated_code.write("\tNOT\n\tTJMP_BW L"+str(MW_._.label)+"\n")  

    elif rule == E_AND_RULE:
        L_ = StackSem.pop()
        E1_ = StackSem.pop()
        if not CheckTypes(E1_._.type,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        if not CheckTypes(L_._.type,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        E0_ = t_attrib(E,None,E(bool_))
        StackSem.append(E0_)
        generated_code.write("\tAND"+"\n")
    
    elif rule == E_OR_RULE:
        L_ = StackSem.pop()
        E1_ = StackSem.pop()
        if not CheckTypes(E1_._.type,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        if not CheckTypes(L_._.type,bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        E0_ = t_attrib(E,None,E(bool_))
        StackSem.append(E0_)
        generated_code.write("\tOR"+"\n")

    elif rule == E_L_RULE:
        L_ = StackSem.pop()
        E_ = t_attrib(E,None,E(L_._.type))
        StackSem.append(E_)
    
    elif rule == L_LESS_THAN_RULE:
        R_ = StackSem.pop()
        L1_ = StackSem.pop()
        if not CheckTypes(L1_._.type,R_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        L0_ = t_attrib(L,None,L(bool_))
        StackSem.append(L0_)
        generated_code.write("\tLT"+"\n")

    elif rule == L_GREATER_THAN_RULE:
        R_ = StackSem.pop()
        L1_ = StackSem.pop()
        if not CheckTypes(L1_._.type,R_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        L0_ = t_attrib(L,None,bool_)
        StackSem.append(L0_)
        generated_code.write("\tGT"+"\n")

    elif rule == L_LESS_EQUAL_RULE:
        R_ = StackSem.pop()
        L1_ = StackSem.pop()
        if not CheckTypes(L1_._.type,R_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        L0_ = t_attrib(L,None,bool_)
        StackSem.append(L0_)
        generated_code.write("\tLE"+"\n")

    elif rule == L_GREATER_EQUAL_RULE:
        R_ = StackSem.pop()
        L1_ = StackSem.pop()
        if not CheckTypes(L1_._.type,R_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        L0_ = t_attrib(L,None,bool_)
        StackSem.append(L0_)
        generated_code.write("\tGE"+"\n")

    elif rule == L_EQUAL_EQUAL_RULE:
        R_ = StackSem.pop()
        L1_ = StackSem.pop()
        if not CheckTypes(L1_._.type,R_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        L0_ = t_attrib(L,None,bool_)
        StackSem.append(L0_)
        generated_code.write("\tEQ"+"\n")

    elif rule == L_NOT_EQUAL_RULE:
        R_ = StackSem.pop()
        L1_ = StackSem.pop()
        if not CheckTypes(L1_._.type,R_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        L0_ = t_attrib(L,None,bool_)
        StackSem.append(L0_)
        generated_code.write("\tNE"+"\n")

    elif rule == L_R_RULE:
        R_ = StackSem.pop()
        L_ = t_attrib(L,None,L(R_._.type))
        StackSem.append(L_)
    
    elif rule == R_PLUS_RULE:
        Y_ = StackSem.pop()
        R1_ = StackSem.pop()
        if not CheckTypes(R1_._.type,Y_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        if not CheckTypes(R1_._.type,int_) and not CheckTypes(R1_._.type,string_):
            Error(lexical, ERR_INVALID_TYPE)
        R0_ = t_attrib(R,None,R(R1_._.type))
        StackSem.append(R0_)
        generated_code.write("\tADD"+"\n")

    elif rule == R_MINUS_RULE:
        Y_ = StackSem.pop()
        R1_ = StackSem.pop()
        if not CheckTypes(R1_._.type,Y_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        if not CheckTypes(R1_._.type,int_):
            Error(lexical, ERR_INVALID_TYPE)
        R0_ = t_attrib(R,None,R(R1_._.type))
        StackSem.append(R0_)
        generated_code.write("\tSUB"+"\n")

    elif rule == R_Y_RULE:
        Y_ = StackSem.pop()
        R_ = t_attrib(R,None,R(Y_._.type))
        StackSem.append(R_)
    
    elif rule == Y_TIMES_RULE:
        F_ = StackSem.pop()
        Y1_ = StackSem.pop()
        if not CheckTypes(Y1_._.type,F_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        if not CheckTypes(Y1_._.type,int_):
            Error(lexical, ERR_INVALID_TYPE)
        Y0_ = t_attrib(Y,None,Y(Y1_._.type))
        StackSem.append(Y0_)
        generated_code.write("\tMUL"+"\n")

    elif rule == Y_DIVIDE_RULE:
        F_ = StackSem.pop()
        Y1_ = StackSem.pop()
        if not CheckTypes(Y1_._.type,F_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        if not CheckTypes(Y1_._.type,int_):
            Error(lexical, ERR_INVALID_TYPE)
        Y0_ = t_attrib(Y,None,Y(Y1_._.type))
        StackSem.append(Y0_)
        generated_code.write("\tDIV"+"\n")

    elif rule == Y_F_RULE:
        F_ = StackSem.pop()
        Y_ = t_attrib(Y,None,Y(F_._.type))
        StackSem.append(Y_)
    
    elif rule == F_LV_RULE:
        LV_ = StackSem.pop()
        # print(LV_._.type._.nSize)
        # n = LV_._.type._.nSize 
        n = 0
        F_ = t_attrib(F,None,F(LV_._.type))
        StackSem.append(F_)
        generated_code.write("\tDE_REF "+str(n)+"\n")
    
    elif rule == F_LEFT_PLUS_PLUS_RULE:
        LV_ = StackSem.pop()
        t = LV_._.type
        if not CheckTypes(t,int_):
            Error(lexical, ERR_INVALID_TYPE)
        F_ = t_attrib(F,None,F(int_))
        generated_code.write("\tDUP\n\tDUP\n\tDE_REF 1"+"\n")
        generated_code.write("\tINC\n\tSTORE REF 1\n\tDE_REF 1"+"\n")

    elif rule == F_LEFT_MINUS_MINUS_RULE:
        LV_ = StackSem.pop()
        t = LV_._.type
        if not CheckTypes(t,int_):
            Error(lexical, ERR_INVALID_TYPE)
        F_ = t_attrib(F,None,F(LV_._.type))
        StackSem.append(F_)
        generated_code.write("\tDUP\n\tDUP\n\tDE_REF 1"+"\n")
        generated_code.write("\tDEC\n\tSTORE_REF 1\n\tDE_REF 1"+"\n")

    elif rule==F_RIGHT_PLUS_PLUS_RULE:
        LV_ = StackSem.pop()
        t = LV_._.type
        if not CheckTypes(t,int_):
            Error(lexical, ERR_INVALID_TYPE)
        F_ = t_attrib(F,None,F(LV_._.type))
        StackSem.append(F_)
        generated_code.write("\tDUP\n\tDUP\n\tDE_REF 1"+"\n")
        generated_code.write("\tINC\n\tSTORE_REF 1\n\tDE_REF 1"+"\n")
        generated_code.write("\tDEC"+"\n")

    elif rule == F_RIGHT_MINUS_MINUS_RULE:
        LV_ = StackSem.pop()
        t = LV_._.type
        if not CheckTypes(t,int_):
            Error(lexical, ERR_INVALID_TYPE)
        F_ = t_attrib(F,None,F(t))
        StackSem.append(F_)
        generated_code.write("\tDUP\n\tDUP\n\tDE_REF 1"+"\n")
        generated_code.write("\tDEC\n\tSTORE_REF 1\n\tDE_REF 1"+"\n")
        generated_code.write("\tINC"+"\n")

    elif rule == F_PARENTHESIS_E_RULE:
        E_ = StackSem.pop()
        F_ = t_attrib(F,None,F(E_._.type))
        StackSem.append(F_)

    elif rule == F_MINUS_F_RULE:
        F1_ = StackSem.pop()
        t = F1_._.type
        if not CheckTypes(t,int_):
            Error(lexical, ERR_INVALID_TYPE)
        F0_ = t_attrib(F,None,F(t))
        StackSem.append(F0_)
        generated_code.write("\tNEG"+"\n")

    elif rule == F_NOT_F_RULE:
        F1_ = StackSem.pop()
        t = F1_._.type
        if not CheckTypes(t,bool_):
            Error(lexical, ERR_INVALID_TYPE)
        F0_ = t_attrib(F,None,F(t))
        StackSem.append(F0_)
        generated_code.write("\tNOT"+"\n")

    elif rule == F_TRUE_RULE:
        TRU_ = StackSem.pop()
        F_ = t_attrib(F,None,F(bool_))
        StackSem.append(F_)
        generated_code.write("\tLOAD_TRUE"+"\n")

    elif rule == F_FALSE_RULE:
        FALS_ = StackSem.pop()
        F_ = t_attrib(F,None,F(bool_))
        StackSem.append(F_)
        generated_code.write("\tLOAD_FALSE"+"\n")

    elif rule == F_CHR_RULE:
        CHR_ = StackSem.pop()
        F_ = t_attrib(F,None,F(char_))
        StackSem.append(F_)
        n = lexical.secondary_Token
        generated_code.write("\tLOAD_CONST "+str(constPool)+"\n")
        constPool+=1

    elif rule == F_STR_RULE:
        STR_ = StackSem.pop()
        F_ = t_attrib(F,None,F(string_))
        StackSem.append(F_)
        n = lexical.secondary_Token
        generated_code.write("\tLOAD_CONST "+str(constPool)+"\n")
        constPool+=1

    elif rule == F_NUM_RULE:
        NUM_ = StackSem.pop()
        F_ = t_attrib(F,None,F(int_))
        StackSem.append(F_)
        n = lexical.secondary_Token
        generated_code.write("\tLOAD_CONST "+str(constPool)+"\n")
        constPool+=1

    elif rule == LV_DOT_RULE:
        ID_ = StackSem.pop()
        LV1_ = StackSem.pop()
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
        StackSem.append(LV0_)
        generated_code.write("\tADD "+str(p._.nIndex)+"\n")

    elif rule == LV_SQUARE_RULE:
        E_ = StackSem.pop()
        LV1_ = StackSem.pop()
        t = LV1_._.type
        if CheckTypes(t,string_):
            LV0_ = t_attrib(LV,None,LV(char_))
        elif t.eKind!=ARRAY_TYPE_:
            if t.eKind != UNIVERSAL_:
                Error(lexical, ERR_KIND_NOT_ARRAY)
            LV0_ = t_attrib(LV,None,LV(universal_))
        else:
            LV0_ = t_attrib(LV,None,LV(t._.tipoElemento))
            n = t._tipoElemento._.nSize
            generated_code.write("\tMUL "+str(n)+"\n")
            generated_code.write("\tADD"+"\n")
        if not CheckTypes(E_._.type,int_):
            Error(lexical, ERR_INVALID_INDEX_TYPE)
        StackSem.append(LV0_)

    elif rule == LV_IDU_RULE:
        IDU_ = StackSem.pop()
        p = IDU_._.object
        if p.eKind != VAR_ and p.eKind!=PARAM_:
            if p.eKind != UNIVERSAL_:
                Error(lexical, ERR_KIND_NOT_VAR)
            LV_ = t_attrib(LV,None,LV(universal_))
        else:
            LV_ = t_attrib(LV,None,LV(p._.tipo))
            LV_._.type._ = Type(None,p._.nSize)
            generated_code.write("\tLOAD_REF "+str(p._.nIndex)+"\n")
        StackSem.append(LV_)
        
    elif rule == MC_RULE:
        IDU_ = StackSem[-1]
        f = IDU_._.object
        if f.eKind != FUNCTION_:
            MC_ = t_attrib(MC,None,MC(universal_,None,True))
        else:
            MC_ = t_attrib(MC,None,MC(f._.pRetType,f._.pParams,False))
        StackSem.append(MC_)
    
    elif rule == LE_E_RULE:
        E_ = StackSem.pop()
        MC_ = StackSem[-1]
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
                LE_._.n = n + 1
        StackSem.append(LE_)
    
    elif rule == LE_LE_RULE:
        E_ = StackSem.pop()
        LE1_ = StackSem.pop()
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
                LE0_._.n = n+1
        StackSem.append(LE0_)
    
    elif rule == F_IDU_MC_RULE:
        LE_ = StackSem.pop()
        MC_ = StackSem.pop()
        IDU_ = StackSem.pop()
        f = IDU_._.object
        F_ = t_attrib(F,None,F(MC_._.type))
        if not LE_._.err:
            if LE_._.n-1 < f._nParams and LE_._.n != 0:
                Error(lexical, ERR_TOO_FEW_ARGS)
            elif LE_._.n-1 > f._.nParams:
                Error(lexical, ERR_TOO_MANY_ARG)
        StackSem.append(F_)
        generated_code.write("\tCALL "+str(f._.nIndex)+"\n")

    elif rule == MT_RULE:
        rLabel = newLabel()
        MT_ = t_attrib(MT,None,MT(rLabel))
        StackSem.append(MT_)
        generated_code.write("\tTJMP_FW L"+str(rLabel)+"\n")

    elif rule == ME_RULE:
        MT_ = StackSem[-1]
        rLabel = newLabel()
        ME_._.label = rLabel
        ME_.t_nont = ME
        StackSem.append(ME_)
        generated_code.write("\tTJMP_FW L"+str(rLabel)+"\n")
        generated_code.write("L"+str(MT_._.label)+"\n")

    elif rule == MW_RULE:
        rLabel = newLabel()
        print(MW_)
        MW_ = StackSem.pop() ##
        print(MW_._)
        MW_._.label = rLabel
        StackSem.append(MW_)
        generated_code.write("L"+str(rLabel)+"\n")

    elif rule==M_BREAK_RULE:
        MT_ = StackSem[-1]

    elif rule == M_CONTINUE_RULE:
        pass
    
    elif rule == M_E_SEMICOLON:
        E_ = StackSem.pop()
        LV_ = StackSem.pop()
        if not CheckTypes(LV_._.type,E_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        t = LV_._.type
        E0_._ = F(E_._.type)
        StackSem.append(E0_)
        if t._ == None or t._.nSize == None:
            generated_code.write("\tSTORE_REF 1\n")
        else:
            generated_code.write("\tSTORE_REF "+str(t._.nSize)+"\n")

    generated_code.close()