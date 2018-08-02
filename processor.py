'''from lexer_grammar import parser as parser
import lexer_grammar'''

from lexer_grammar import parser as parser
import lexer_grammar

import os
arg_list = {
    'file_name':"",
    'lpodPrefType':"",
    'constant':"",
    'asprin':""
}

def arg_processor(arglist):

    global arg_list
    arg_list['file_name'] =arglist[0]

    print("\nInput LPOD program:   " + arg_list['file_name'])
    

    arglist = arglist[1:]
    for item in arglist:
        if "-c lpodPrefType=" in item:
            arg_list['lpodPrefType'] = str(item[item.find("=")+1:])
            print("Preference Criterion: " + arg_list['lpodPrefType'])
        if "-constant" in item:
            arg_list['constant'] = " -c " + str(item[item.find("constant")+9:])
            print("Constant Assignment:  " + str(item[item.find("constant")+9:]))
        if "-asprin" in item:
        	arg_list['asprin'] = " " + str(item[item.find("asprin")+7:])
        	print("Asprin Options:      " + arg_list['asprin'])
    print(" ")

    

def begin_parse():

    with open(arg_list['file_name'] ,'r') as content_file:
        content = content_file.read()

    parser.parse(content)
    lpod2asprin = lexer_grammar.baseprogram + "\n\n\n" + lexer_grammar.prefstatement + "\n\n\n" + lexer_grammar.showstatement 

    with open ('parsed_temp.pl','w') as fw:
        fw.write(lpod2asprin)


def solve():

    command = "asprin " + os.getcwd()+"/lpod.lp " + os.getcwd() + "/parsed_temp.pl 0 -c lpodPrefType=" + arg_list['lpodPrefType'] + arg_list['constant'] + arg_list['asprin']
    # print(command)
    os.system(command)



def clean():
    os.remove("parsed_temp.pl")
    os.remove("parser.out")
    os.remove("parsetab.py")
    os.remove("arg_proce.pyc")
    os.remove("lexer_grammar.pyc")
    os.remove("processor.pyc")
    if os.path.isfile("parsetab.pyc"):
        os.remove("parsetab.pyc")

