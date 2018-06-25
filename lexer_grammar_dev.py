from math import exp,expm1,log
reserved = {
    'not' : 'NOT',
}

tokens = [
    'ORDEREDDISJUNCTION',
    'NUMBER','IDENTIFIER','VARIABLE','ANONYMOUS','STRING',
    'ADD','AND','EQ','AT','COLON','COMMA','CONST','COUNT','CSP','CSP_ADD',
    'CSP_SUB','CSP_MUL','CSP_LEQ','CSP_LT','CSP_GT','CSP_GEQ','CSP_EQ','CSP_NEQ','DISJOINT','DOT',
    'DOTS','EXTERNAL','FALSE','GEQ','GT','IF','INCLUDE','INFIMUM','LBRACE','LBRACK','LEQ','LPAREN',
    'LT','MAX','MAXIMIZE','MIN','MINIMIZE','MOD','MUL','NEQ','POW','QUESTION','RBRACE','RBRACK','RPAREN','SEM','SHOW',
    'EDGE','PROJECT','HEURISTIC','SHOWSIG','SLASH','SUB','SUM','SUMP','SUPREMUM','TRUE','BLOCK',
    'VBAR','WIF','XOR','COMMENT',
]
tokens += reserved.values()

t_ORDEREDDISJUNCTION = r'\>\>'

t_ANONYMOUS = r'\_'
t_STRING = r'"([^"\n]|(\\"))*"$'
t_ADD = r'\+'
t_AND = r'\&'
t_EQ = r'\='
t_AT = r'\@'
t_COLON = r'\:'
t_COMMA = r'\,'
t_CONST = r'\#const'
t_COUNT = r'\#count'
t_CSP = r'\$'
t_CSP_ADD = r'\$\+'
t_CSP_SUB = r'\$\-'
t_CSP_MUL = r'\$\*'
t_CSP_LEQ = r'\$\<\='
t_CSP_LT = r'\$\<'
t_CSP_GT = r'\$\>'
t_CSP_GEQ = r'\$\>\='
t_CSP_EQ = r'\$\='
t_CSP_NEQ = r'\$\!\='
t_DISJOINT = r'\#disjoint'
t_DOT = r'\.'
t_DOTS = r'\.\.'
t_EXTERNAL = r'\#external'
t_FALSE = r'\#false'
t_GEQ = r'\>='
t_GT = r'\>'
t_IF = r'\:\-'
t_INCLUDE = r'\#include'
t_INFIMUM = r'\#inf'
t_LBRACE = r'\{'
t_LBRACK = r'\['
t_LEQ = r'\<\='
t_LPAREN = r'\('
t_LT = r'\<'
t_MAX = r'\#max'
t_MAXIMIZE = r'\#maximize'
t_MIN = r'\#min'
t_MINIMIZE = r'\#minimize'
t_MOD = r'\\'
t_MUL = r'\*'
t_NEQ = r'\!\='
t_POW = r'\*\*'
t_QUESTION = r'\?'
t_RBRACE = r'\}'
t_RBRACK = r'\]'
t_RPAREN = r'\)'
t_SEM = r'\;'
t_SHOW = r'\#show'
t_EDGE = r'\#edge'
t_PROJECT = r'\#project'
t_HEURISTIC = r'\#heuristic'
t_SHOWSIG = r'\#showsig'
t_SLASH = r'\/'
t_SUB = r'\-'
t_SUM = r'\#sum'
t_SUMP = r'\#sum+'
t_SUPREMUM = r'\#sup'
t_TRUE = r'\#true'
t_BLOCK = r'\#program'
t_VBAR = r'\|'
t_WIF = r'\:\~'
t_XOR = r'\^'
t_COMMENT = r'\%.*'


def t_IDENTIFIER(t):
    r'_*[a-z][\'a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t

def t_VARIABLE(t):
    r'_*[A-Z][\'a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VARIABLE')  # Check for reserved words
    return t



def t_NUMBER(t):
    r'[-+]?[0-9]+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("integer value too large %d", t.value)
        t.value = 0
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex

lexer = lex.lex()
# Parsing rules

precedence = (
    ('left','DOTS'),
    ('left','XOR'),
    ('left', 'QUESTION'),
    ('left', 'AND'),
    ('left', 'ADD','SUB'),
    ('left', 'MUL','SLASH','MOD'),
    ('right', 'POW'),
)

def fill_t(t):
    filledt=""
    for item in t:
        if type(item) is str :
            filledt += str(item)
        elif type(item) is int:
            filledt += str(item)


    return filledt



# # dictionary of names
# names = {}
ruleCounter = 1
preftype = "pare"
g_parsedDic = {}
atom_list = []



# {{{1 logic program and global definitions

def p_start(t):
    'start : program'

    global checkLPOD
    if checkLPOD:
        global prefstatement
        prefstatement += "\n}. \n\n#optimize(lpod)."

    global atom_list
    global showstatement
    for item in atom_list:
    	showstatement += ("#show"+ item + ".\n")

def p_program(t):
    '''program : program statement
               | '''

# Note: skip until the next "." in case of an error and switch back to normal lexing

def p_statement(t):
    '''statement : statement_1
                | statement_2
                | statement_3
                | statement_4
                | statement_5
                | statement_6
                | statement_7
                | statement_8
                | statement_9
                | statement_10
                | statement_11
                | statement_12
                | statement_13
                | statement_14 '''


def p_identifier(t):
    'identifier : IDENTIFIER'
    t[0] = ' '+ fill_t(t)


def p_vaiable(t):
    'variable : VARIABLE'
    value = str(t[1])

    find = False
    if len(g_parsedDic) == ruleCounter:
        varList = g_parsedDic['r' + str(ruleCounter)]['var'].split(',')
        for var in varList:
            if value == var:
                find = True
        if not find:
            g_parsedDic['r' + str(ruleCounter)]['var'] += ','+ value
    else:
        g_parsedDic['r' + str(ruleCounter)] = {'weight': "",
                                               'var': value
                                               }

    t[0] = ' '+ fill_t(t)
# {{{1 terms
# {{{2 constterms are terms without variables and pooling operators

def p_constterm(t):
    '''constterm : constterm XOR constterm
                | constterm QUESTION constterm
                | constterm AND constterm
                | constterm ADD constterm
                | constterm SUB constterm
                | constterm MUL constterm
                | constterm SLASH constterm
                | constterm MOD constterm
                | constterm POW constterm
                | LPAREN RPAREN
                | LPAREN COMMA RPAREN
                | LPAREN consttermvec RPAREN
                | LPAREN consttermvec COMMA RPAREN
                | identifier LPAREN constargvec RPAREN
                | AT identifier LPAREN constargvec RPAREN
                | VBAR constterm VBAR
                | identifier
                | NUMBER
                | STRING
                | INFIMUM
                | SUPREMUM'''
    t[0] = fill_t(t)

# {{{2 arguments lists for functions in constant terms

def p_consttermvec(t):
    '''consttermvec : constterm
                    | consttermvec COMMA constterm'''
    t[0] = fill_t(t)
def p_constargvec(t):
    '''constargvec : consttermvec
                    |
                    '''
    t[0] = fill_t(t)
# {{{2 terms including variables

def p_term(t):
    '''term : term DOTS term
            | term XOR term
            | term QUESTION term
            | term AND term
            | term ADD term
            | term SUB term
            | term MUL term
            | term SLASH term
            | term MOD term
            | term POW term
            | LPAREN tuplevec RPAREN
            | identifier LPAREN argvec RPAREN
            | AT identifier LPAREN argvec RPAREN
            | VBAR unaryargvec VBAR
            | identifier
            | NUMBER
            | STRING
            | INFIMUM
            | SUPREMUM
            | variable
            | ANONYMOUS'''
    t[0] = fill_t(t)


# {{{2 argument lists for unary operations

def p_unaryargvec(t):
    '''unaryargvec : term
                    | unaryargvec SEM term'''
    t[0] = fill_t(t)
# {{{2 argument lists for functions

def p_ntermvec(t):
    '''ntermvec : term
                | ntermvec COMMA term'''
    t[0] = fill_t(t)
def p_termvec(t):
    '''termvec : ntermvec
                |'''
    t[0] = fill_t(t)
def p_tuple(t):
    '''tuple : ntermvec COMMA
            | ntermvec
            | COMMA
            | '''
    t[0] = fill_t(t)

def p_tuplevec_sem(t):
    '''tuplevec_sem : tuple SEM
                    | tuplevec_sem tuple SEM '''
    t[0] = fill_t(t)

def p_tuplevec(t):
    '''tuplevec : tuple
                | tuplevec_sem tuple '''
    t[0] = fill_t(t)

def p_argvec(t):
    '''argvec : termvec
                | argvec SEM termvec'''
    t[0] = fill_t(t)
def p_binaryargvec(t):
    '''binaryargvec : term COMMA term
                    | binaryargvec SEM term COMMA term'''
    t[0] = fill_t(t)
# TODO: I might have to create tuples differently
#       parse a tuple as a list of terms
#       each term is either a tuple or a term -> which afterwards is turned into a pool!

# {{{1 literals

def p_cmp(t):
    '''cmp : GT
            | LT
            | GEQ
            | LEQ
            | EQ
            | NEQ'''
    t[0] = fill_t(t)
def p_atom(t):
    '''atom : identifier
            | identifier LPAREN argvec RPAREN
            | SUB identifier
            | SUB identifier LPAREN argvec RPAREN'''

    t[0] = fill_t(t)

    global atom_list

    if len(t) == 2:
        term_arity = t[1] + "/0"
        if term_arity not in atom_list:
        	atom_list.append(term_arity)
        # print("#show"+ term_arity + ".\n")
    elif len(t) == 3:
        term_arity = t[1] + t[2] + "/0"
        if term_arity not in atom_list:
        	atom_list.append(term_arity)
        # print("#show"+ term_arity + ".\n")
    elif len(t) == 5:
        term_list = t[3].split(',')
        arity = len(term_list)
        term_arity = t[1] + "/" + str(arity)
        if term_arity not in atom_list:
        	atom_list.append(term_arity)
        # print("#show"+ term_arity + ".\n")
    elif len(t) == 6:
        term_list = t[4].split(',')
        arity = len(term_list)
        term_arity = t[1] + t[2] + "/" + str(arity)
        if term_arity not in atom_list:
        	atom_list.append(term_arity)
        # print("#show"+ term_arity + ".\n")
    else:
        print("Length error for atom! \n")

def p_literal(t):
    '''literal : TRUE
                | NOT TRUE
                | NOT NOT TRUE
                | FALSE
                | NOT FALSE
                | NOT NOT FALSE
                | atom
                | NOT atom
                | NOT NOT atom
                | term cmp term
                | NOT term cmp term
                | NOT NOT term cmp term
                | csp_literal'''
    t[0] = fill_t(t)
def p_csp_mul_term(t):
    '''csp_mul_term : CSP term CSP_MUL term
                    | term CSP_MUL CSP term
                    | CSP term
                    | term'''
    t[0] = fill_t(t)
def p_csp_add_term(t):
    '''csp_add_term : csp_add_term CSP_ADD csp_mul_term
                    | csp_add_term CSP_SUB csp_mul_term
                    | csp_mul_term'''
    t[0] = fill_t(t)
def p_csp_rel(t):
    '''csp_rel : CSP_GT
                | CSP_LT
                | CSP_GEQ
                | CSP_LEQ
                | CSP_EQ
                | CSP_NEQ'''
    t[0] = fill_t(t)

def p_csp_literal (t):
    '''csp_literal : csp_literal csp_rel csp_add_term
                    | csp_add_term  csp_rel csp_add_term'''
    t[0] = fill_t(t)
# {{{1 aggregates

# {{{2 auxiliary rules

def p_nlitvec(t):
    '''nlitvec : literal
                | nlitvec COMMA literal'''
    t[0] = fill_t(t)
def p_litvec(t):
    '''litvec : nlitvec
                | '''
    t[0] = fill_t(t)
def p_optcondition(t):
    '''optcondition : COLON litvec
                     | '''
    t[0] = fill_t(t)
def p_noptcondition(t):
    '''noptcondition : COLON nlitvec
                    | '''
    t[0] = fill_t(t)
def p_aggregatefunction(t):
    '''aggregatefunction : SUM
                        | SUMP
                        | MIN
                        | MAX
                        | COUNT'''
    t[0] = fill_t(t)
# {{{2 body aggregate elements

def p_bodyaggrelem(t):
    '''bodyaggrelem : COLON litvec
                    | ntermvec optcondition'''
    t[0] = fill_t(t)
def p_bodyaggrelemvec(t):
    '''bodyaggrelemvec : bodyaggrelem
                        | bodyaggrelemvec SEM bodyaggrelem'''
    t[0] = fill_t(t)
# Note: alternative syntax (without weight)

def p_altbodyaggrelem(t):
    'altbodyaggrelem : literal optcondition'
    t[0] = fill_t(t)
def p_altbodyaggrelemvec(t):
    '''altbodyaggrelemvec : altbodyaggrelem
                          | altbodyaggrelemvec SEM altbodyaggrelem'''
    t[0] = fill_t(t)
# {{{2 body aggregates

def p_bodyaggregate(t):
    '''bodyaggregate : LBRACE RBRACE
                    | LBRACE altbodyaggrelemvec RBRACE
                    | aggregatefunction LBRACE RBRACE
                    | aggregatefunction LBRACE bodyaggrelemvec RBRACE'''
    t[0] = fill_t(t)
def p_upper(t):
    '''upper : term
            | cmp term
            | '''
    t[0] = fill_t(t)
def p_lubodyaggregate(t):
    '''lubodyaggregate : term bodyaggregate upper
                        | term cmp bodyaggregate upper
                        | bodyaggregate upper '''
    t[0] = fill_t(t)
# {{{2 head aggregate elements

def p_headaggrelemvec(t):
    '''headaggrelemvec : headaggrelemvec SEM termvec COLON literal optcondition
                        | termvec COLON literal optcondition '''
    t[0] = fill_t(t)
def p_altheadaggrelemvec(t):
    '''altheadaggrelemvec : literal optcondition
                            | altheadaggrelemvec SEM literal optcondition '''
    t[0] = fill_t(t)
# {{{2 head aggregates

def p_headaggregate(t):
    '''headaggregate : aggregatefunction LBRACE RBRACE
                    | aggregatefunction LBRACE headaggrelemvec RBRACE
                    | LBRACE RBRACE
                    | LBRACE altheadaggrelemvec RBRACE '''
    t[0] = fill_t(t)
def p_luheadaggregate(t):
    '''luheadaggregate : term headaggregate upper
                        | term cmp headaggregate upper
                        | headaggregate upper '''
    t[0] = fill_t(t)
# {{{2 disjoint aggregate

def p_ncspelemvec(t):
    '''ncspelemvec :  termvec COLON csp_add_term optcondition
                    | cspelemvec SEM termvec COLON csp_add_term optcondition'''
    t[0] = fill_t(t)
def p_cspelemvec(t):
    '''cspelemvec : ncspelemvec
                    | '''
    t[0] = fill_t(t)
def p_disjoint(t):
    '''disjoint : DISJOINT LBRACE cspelemvec RBRACE
                | NOT DISJOINT LBRACE cspelemvec RBRACE
                | NOT NOT DISJOINT LBRACE cspelemvec RBRACE '''
    t[0] = fill_t(t)
#/}}}
# {{{2 conjunctions

def p_conjunction(t):
    'conjunction : literal COLON litvec'

    t[0] = fill_t(t)
# }}}
# {{{2 disjunctions

def p_dsym(t):
    '''dsym : SEM
            | VBAR '''
def p_disjunctionsep(t):
    '''disjunctionsep : disjunctionsep literal COMMA
                        | disjunctionsep literal noptcondition dsym
                        | '''
    t[0] = fill_t(t)
# Note: for simplicity appending first condlit here
def p_disjunction(t):
    '''disjunction : literal COMMA disjunctionsep literal noptcondition
                    | literal dsym disjunctionsep literal noptcondition
                    | literal  COLON nlitvec dsym disjunctionsep literal noptcondition
                    | literal COLON nlitvec '''
    t[0] = fill_t(t)
# {{{1 statements
# {{{2 rules

def p_bodycomma(t):
    '''bodycomma : bodycomma literal COMMA
                | bodycomma literal SEM
                | bodycomma lubodyaggregate COMMA
                | bodycomma lubodyaggregate SEM
                | bodycomma NOT lubodyaggregate COMMA
                | bodycomma NOT lubodyaggregate SEM
                | bodycomma NOT NOT lubodyaggregate COMMA
                | bodycomma NOT NOT lubodyaggregate SEM
                | bodycomma conjunction SEM
                | bodycomma disjoint SEM
                |'''
    t[0] = fill_t(t)
def p_bodydot(t):
    '''bodydot : bodycomma literal DOT
                | bodycomma lubodyaggregate DOT
                | bodycomma NOT lubodyaggregate DOT
                | bodycomma NOT NOT lubodyaggregate DOT
                | bodycomma conjunction DOT
                | bodycomma disjoint DOT '''
    t[0] = fill_t(t)
def p_bodyconddot(t):
    '''bodyconddot : DOT
                    | COLON DOT
                    | COLON bodydot '''
    t[0] = fill_t(t)

def p_head(t):
    '''head : literal
            | disjunction
            | luheadaggregate '''
    t[0] = fill_t(t)





lpodRuleCounter = 1
# check whether there exists an LPOD rule
checkLPOD = False
# lpodtype = "pare" # by default we use Pareto-preference
baseprogram = ""
prefstatement = ""
showstatement = ""


def p_statement_14(t):
    '''statement_14 : lpodhead DOT
                    | lpodhead IF DOT
                    | lpodhead IF bodydot '''

    t[0] = fill_t(t)

    # we first check whether this LPOD rule contains a variable
    checkVar = False

    global ruleCounter

    if len(g_parsedDic) != ruleCounter:
        g_parsedDic['r' + str(ruleCounter)] = {'var': ""}
    else:
        checkVar = True

    # let checkLPOD be True, which says that the program contains at least one LPOD rule
    global checkLPOD
    if checkLPOD == False:
        checkLPOD = True

    # base program
    global lpodRuleCounter
    line=""
    if len(t) == 3:
        bigBody = "."
    elif len(t) == 4:
        bigBody = t[3]
    else:
        print("Lenth of t is wrong in p_statement_15")

    varVec = " "

    if checkVar:
    	# add rule: body_i(X) :- Body_i,  where Body_i contains variable X
    	varVec = "(" + g_parsedDic['r' + str(ruleCounter)]['var'] + ")"

    line += ("body_" + str(lpodRuleCounter) + varVec + " :- " + bigBody + "\n")

    bigHead = t[1].split('>>')

    for i in range(len(bigHead)):
        negPart = ""
        if i > 0:
            for j in range(i):
                negPart += (", not" + bigHead[j])
        if i == (len(bigHead)-1):
            tmp = bigHead[i] + " :- body_" + str(lpodRuleCounter) + varVec + negPart + ".\n"
            line += tmp
        else:
            tmp = "{" + bigHead[i] + "} :- body_" + str(lpodRuleCounter) + varVec + negPart + ".\n"
            line += tmp

    global baseprogram
    baseprogram += line

    # preference statement
    global prefstatement
    # global lpodtype

    if prefstatement == "":
    	# prefstatement += "#preference(lpod, lpod(" + lpodtype + ")) { \n"
        prefstatement += "#preference(lpod, lpod(lpodPrefType)) { \n"
    elif lpodRuleCounter != 1:
        prefstatement += ";\n"

    prefelement = "  not body_" + str(lpodRuleCounter) + varVec
    for i in range(len(bigHead)):
        prefelement += (" >>" + bigHead[i])

    prefstatement += prefelement
    lpodRuleCounter += 1

    ruleCounter += 1

def p_lpodhead(t):
    '''lpodhead : ordisjunction ORDEREDDISJUNCTION atom'''
    t[0] = fill_t(t)

def p_ordisjunction(t):
    '''ordisjunction : atom
                    | ordisjunction ORDEREDDISJUNCTION atom'''
    t[0] = fill_t(t)









#Next is the hard rule
def p_statement_1(t):
    '''statement_1 : head DOT
                    | head IF DOT
                    | head IF bodydot
                    | IF bodydot
                    | IF DOT'''
    global ruleCounter
    if len(g_parsedDic) != ruleCounter:
    	g_parsedDic['r' + str(ruleCounter)] = {'var': ""}

    t[0] = fill_t(t)
    global baseprogram
    baseprogram += (t[0] + "\n")

    ruleCounter += 1


def p_statement_2(t):
    '''statement_2 : disjoint IF bodydot
                    | disjoint IF DOT
                    | disjoint DOT'''
    t[0] = fill_t(t)
    global baseprogram
    baseprogram += (t[0] + "\n")

# {{{2 optimization

def p_optimizetuple(t):
    '''optimizetuple : COMMA ntermvec
                     |'''
    t[0] = fill_t(t)

def p_optimizeweight(t):
    '''optimizeweight : term AT term
                      | term'''
    t[0] = fill_t(t)

def p_optimizelitvec(t):
    '''optimizelitvec : literal
                      | optimizelitvec COMMA literal'''
    t[0] = fill_t(t)

def p_optimizecond(t):
    '''optimizecond : COLON optimizelitvec
                    | COLON
                    | '''
    t[0] = fill_t(t)

def p_statement_3(t):
    '''statement_3 : WIF bodydot LBRACK optimizeweight optimizetuple RBRACK
                   | WIF DOT LBRACK optimizeweight optimizetuple RBRACK'''
    t[0] = fill_t(t)
    global baseprogram
    baseprogram += (t[0] + "\n")

def p_maxelemlist(t):
    '''maxelemlist : optimizeweight optimizetuple optimizecond
                   | maxelemlist SEM optimizeweight optimizetuple optimizecond'''
    t[0] = fill_t(t)
def p_minelemlist(t):
    '''minelemlist : optimizeweight optimizetuple optimizecond
                   | minelemlist SEM optimizeweight optimizetuple optimizecond '''
    t[0] = fill_t(t)
def p_statement_4(t):
    '''statement_4 : MINIMIZE LBRACE RBRACE DOT
                    | MAXIMIZE LBRACE RBRACE DOT
                    | MINIMIZE LBRACE minelemlist RBRACE DOT
                    | MAXIMIZE LBRACE maxelemlist RBRACE DOT'''
    t[0] = fill_t(t)
    global baseprogram
    baseprogram += (t[0] + "\n")
# {{{2 visibility

def p_statement_5(t):
    '''statement_5 : SHOWSIG identifier SLASH NUMBER DOT
                    | SHOWSIG SUB identifier SLASH NUMBER DOT
                    | SHOW DOT
                    | SHOW term COLON bodydot
                    | SHOW term DOT
                    | SHOWSIG CSP identifier SLASH NUMBER DOT
                    | SHOW CSP term COLON bodydot
                    | SHOW CSP term DOT'''
    t[0] = fill_t(t)
    global baseprogram
    baseprogram += (t[0] + "\n")
# {{{2 acyclicity

def p_statement_6(t):
    'statement_6 : EDGE LPAREN binaryargvec RPAREN bodyconddot'
    t[0] = fill_t(t)
    global baseprogram
    baseprogram += (t[0] + "\n")
# {{{2 heuristic

def p_statement_7(t):
    '''statement_7 : HEURISTIC atom bodyconddot LBRACK term AT term COMMA term RBRACK
                    | HEURISTIC atom bodyconddot LBRACK term COMMA term RBRACK'''
    t[0] = fill_t(t)
    global baseprogram
    baseprogram += (t[0] + "\n")
# {{{2 project

def p_statement_8(t):
    '''statement_8 : PROJECT identifier SLASH NUMBER DOT
                    | PROJECT SUB identifier SLASH NUMBER DOT
                    | PROJECT atom bodyconddot'''
    t[0] = fill_t(t)
    global baseprogram
    baseprogram += (t[0] + "\n")
# {{{2 constants

'''def p_define(t):
    'define : identifier EQ constterm'
    t[0] = fill_t(t)'''

def p_statement_9(t):
    'statement_9 : CONST identifier EQ constterm DOT'
    t[0] = fill_t(t)
    global baseprogram
    baseprogram += (t[0] + "\n")

def p_statement_10(t):
    '''statement_10 : INCLUDE STRING DOT
                    | INCLUDE LT identifier GT DOT'''
    t[0] = fill_t(t)
    global baseprogram
    baseprogram += (t[0] + "\n")
# {{{2 blocks

def p_nidlist (t):
    '''nidlist : nidlist COMMA identifier
               | identifier '''
    t[0] = fill_t(t)

def p_idlist (t):
    '''idlist :
              | nidlist '''
    t[0] = fill_t(t)
def p_statement_11(t):
    '''statement_11 : BLOCK identifier LPAREN idlist RPAREN DOT
                    | BLOCK identifier DOT'''
    t[0] = fill_t(t)
    global baseprogram
    baseprogram += (t[0] + "\n")
# {{{2 external

def p_statement_12(t):
    '''statement_12 : EXTERNAL atom COLON bodydot
                    | EXTERNAL atom COLON DOT
                    | EXTERNAL atom DOT'''
    t[0] = fill_t(t)
    global baseprogram
    baseprogram += (t[0] + "\n")

def p_statement_13(t):
    'statement_13 : COMMENT'
    t[0] = fill_t(t)
    global baseprogram
    baseprogram += (t[0] + "\n")



def p_error(t):
    if type(t) is 'NoneType':
        print("Syntax error")
    else:
        print("Syntax error at '%s'" % t.value)
    print("Type of t is: "+t.type)
    print("At rule line number: " + str(ruleCounter))
    print("next token: " + str(parser.token()))


import ply.yacc as yacc
parser = yacc.yacc(start='start')
