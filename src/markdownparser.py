#!/usr/local/bin/python
# coding: utf-8
# -------------------------------------------------
# @author larrymario lizhen2013 ScottFoH
# @update 2014-12-24
# -------------------------------------------------

import sys

print ''
if len(sys.argv) == 1:
    print("Using test.md as default.")
    filename = 'test03.md'
else:
    filename = sys.argv[1]
print ''

tokens = (
    'H1','H2','H3','LSQ','RSQ','LB','RB',
    'LT','RT','AS','UDL','MINUS',
    'PLUS','EXCLAM','EQ','DOT','BLANK',
    'QQ','CR','TAB','NUMBER','WORD'
    )

# Tokens
t_H1 = r'\# '
t_H2 = r'\#\# '
t_H3 = r'\#\#\# '
t_LSQ = r'\['
t_RSQ = r'\]'
t_LB = r'\('
t_RB = r'\)'
t_LT = r'<'
t_RT = r'>'
t_AS = r'\*'
t_UDL = r'_'
t_MINUS = r'-'
t_PLUS = r'\+'
t_EXCLAM = r'!'
t_EQ = r'='
t_DOT = r'\.'
t_BLANK = r'[ ]'
t_QQ = r'\`'
t_CR = r'\n'
t_TAB = r'\t'
t_NUMBER = r'[0-9]+'
t_WORD = r'[a-zA-Z,:?/\\\'\"]+'



t_ignore = ""


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import re
import ply.lex as lex
lexer = lex.lex(reflags = re.UNICODE)

# Test lexer
lexer.input(open(filename).read())
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
print ''

# ------------------------------------
# definitions of parsing rules by yacc
# ------------------------------------
precedence = (

    )
names = {}

def p_body(p):
    "body : statement"
    p[0] = '<body>\n' + p[1] + '</body>'

def p_state_null(p):
    '''statement : '''
    p[0] = ""
def p_state_expression(p):
    '''statement : statement CR expression
            | statement CR
            | expression'''
    if len(p) == 2:
        p[0] = p[1] + '\n'
    elif len(p) == 3:
        p[0] = p[1] + '\n'
    elif len(p) == 4:
        p[0] = p[1]  + '\n' + p[3] 


def p_exp_header_factor(p):
    '''expression : H1 factor
                | H2 factor
                | H3 factor'''
    if p[1] == '#':
        p[0] = '<h1>' + p[2] + '</h1>'
    elif p[1] == '##':
        p[0] = '<h2>' + p[2] + '</h2>'
    elif p[1] == '###':
        p[0] = '<h3>' + p[2] + '</h3>'

def p_exp_factor(p):
    '''expression : expression expression
                | factor
                | line
                | picture
                | ul
                | codes
                | quote
                | link'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_exp_strong(p):
    '''expression : strong'''
    p[0] = '<strong>' + p[1] + '</strong>'

def p_exp_em(p):
    '''expression : em'''
    p[0] = '<em>' + p[1] + '</em>'

def p_line(p):
    '''line : AS AS AS
                | UDL UDL UDL
                | AS BLANK AS BLANK AS
                | UDL BLANK UDL BLANK UDL
                | MINUS MINUS MINUS
                | EQ EQ EQ'''
    p[0] = '<hr/>'

def p_strong(p):
    '''strong : AS em AS
                | UDL em UDL'''
    p[0] =  p[2] 

def p_em(p):
    '''em : ASfactor AS'''
    p[0] =  p[1] 

def p_em2(p):
    '''em : UDL factor UDL'''
    p[0] =  p[2] 

def p_ASfactor(p):
    '''ASfactor : AS factor'''   
    p[0] =  p[2] 

def p_ASfactor2(p):
    '''ASfactor : ASfactor factor'''   
    p[0] =  p[1] + p[2] 

def p_quote(p):
    '''quote : RT factor '''
    p[0] = '<blockquote>' + p[2] + '</blockquote>\n'

def p_codes_code(p):
    '''codes : code QQ
                | code CR QQ'''
    p[0] = '<code style="background:AliceBlue">' + p[1] + '</code>'

def p_codes_em(p):
    '''codes : QQ UDL factor UDL QQ'''
    p[0] = '<code style="background:AliceBlue">_' + p[3] + '_</code>'

def p_codes_codes(p):
    '''codes : QQ codes QQ'''
    p[0] = p[2]

def p_code(p):
    '''code : QQ factor 
                | code factor
                | code CR
                | QQ CR factor'''
    if len(p) == 4:
        p[0] = '<br/>' + p[3]
    elif p[1] == "`":
        p[0] = p[2]
    elif p[2] == "\n":
        p[0] = p[1] + '<br/>'
    else:
        p[0] = p[1] + p[2]

def p_ol(p):
    '''ul : olis'''
    p[0] = '<ol>\n' + p[1] + '</ol>\n'

def p_ol_ul(p):
    '''ul : olis iul'''
    p[0] = '<ol>\n' + p[1] + '<ul>\n' + p[2] + '</ul>\n' + '</ol>\n'

def p_oli(p):
    '''oli : NUMBER DOT factor CR'''
    p[0] = '<li>'+p[3]+'</li>\n'

def p_olis(p):
    '''olis : olis oli
                | oli'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_ul_lis(p):
    '''ul : lis'''
    p[0] = '<ul>\n' + p[1] + '</ul>\n'

def p_iul_ili(p):
    '''iul : ilis'''
    p[0] = p[1] 

def p_iiul_iili(p):
    '''iiul : iilis'''
    p[0] = p[1]

def p_ul_iul(p):
    '''ul : lis iul'''
    p[0] = '<ul>\n' + p[1] + '<ul>\n' + p[2] + '</ul>\n' + '</ul>\n'

def p_iul_iiul(p):
    '''iul : ilis iiul'''
    p[0] =  p[1] + '<ul>\n' + p[2] + '</ul>\n' 


def p_li(p):
    '''li : ASfactor CR'''
    p[0] = '<li>'+p[1]+'</li>\n'

def p_ili(p):
    '''ili : TAB li'''
    p[0] = p[2]

def p_iili(p):
    '''iili : TAB TAB li'''
    p[0] = p[3]

def p_lis(p):
    '''lis : lis li
                | li'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_ilis(p):
    '''ilis : ilis ili
                | ili'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_iilis(p):
    '''iilis : iilis iili
                | iili'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_li2(p):
    '''li : li PLUS factor CR
                | li MINUS factor CR
                | PLUS factor CR
                | MINUS factor CR'''
    if len(p) == 4:
        p[0] = '<li>'+p[2]+'</li>\n'
    else:
        p[0] = p[1] + '<li>'+p[3]+'</li>\n'


def p_picture(p):
    "picture : EXCLAM LSQ factor RSQ LB factor RB"
    p[0] = '<img src=\"'+ p[6] + '\"  alt=\"' + p[3] + '\" />'

def p_link(p):
    '''link : LT factor RT
                | LSQ factor RSQ LB factor RB'''
    if(len(p) == 4):
        p[0] = '<a href=\"'+ p[2] +'\">'+p[2]+'</a>'
    else:
        p[0] = '<a href=\"'+ p[5] +'\">'+p[2]+'</a>'


def p_factor_subfactor(p):
    '''factor : factor subfactor
            | subfactor'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1] 


def p_subfactor(p):
    '''subfactor : WORD
            | NUMBER
            | DOT
            | BLANK 
            | TAB'''
    p[0] = p[1]

def p_error(p):
    if p:
        print("error at '%s' line '%d'" % (p.value, p.lineno))
    else:
        print("error at EOF")

import ply.yacc as yacc
yaccer = yacc.yacc(method = "SLR")

if __name__ == '__main__':
    result = yaccer.parse(open(filename).read(), debug = 0)
    print result

if len(sys.argv) == 3:
    out = file(sys.argv[2], 'w')
    out.write(result)
    print('Saved to file ' + sys.argv[2])
    out.close()

print ''
