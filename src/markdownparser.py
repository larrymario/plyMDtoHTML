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
    filename = 'test.md'
else:
    filename = sys.argv[1]
print ''

tokens = (
    'H1','H2','H3','H4','H5','H6',
    'SH1','SH2',
    'LINE',
    'STRONG','EM',
    'CR', 'TEXT'
    )

# Tokens
t_H1 = r'\# '
t_H2 = r'\#\# '
t_H3 = r'\#\#\# '
t_H4 = r'\#\#\#\# '
t_H5 = r'\#\#\#\#\#'
t_H6 = r'\#\#\#\#\#\#'
t_SH1 = r'=+'
t_SH2 = r'-+'
t_LINE = r'(\*[ ]{0,2}\*[ ]{0,2}\*)|(_[ ]{0,2}_[ ]{0,2}_)'
#t_LINE = r'\*[ ]{0,2}\*[ ]{0,2}\*'
t_STRONG = r'(\*\*|__)'
t_EM = r'(\*|_)'


def t_TEXT(t):
    r'[a-zA-Z0-9,.!\?\'’]+'
    t.value = str(t.value)
    return t


t_ignore = " \t"

def t_CR(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t

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

def p_state(p):
    '''statement : statement CR expression
            | statement CR
            | expression'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[1] + p[3] + '\n'

def p_exp_cr(p):
    "expression : CR"
    p[0] = '<br/>\n'

def p_exp_line(p):
    "expression : LINE"
    p[0] = '<hr/>\n'

def p_exp_header_factor(p):
    '''expression : H1 factor
                | H2 factor
                | H3 factor
                | H4 factor
                | H5 factor
                | H6 factor'''
    if p[1] == '#':
        p[0] = '<h1>' + p[2] + '</h1>\n'
    elif p[1] == '##':
        p[0] = '<h2>' + p[2] + '</h2>\n'
    elif p[1] == '###':
        p[0] = '<h3>' + p[2] + '</h3>\n'
    elif p[1] == '####':
        p[0] = '<h4>' + p[2] + '</h4>\n'
    elif p[1] == '#####':
        p[0] = '<h5>' + p[2] + '</h5>\n'
    elif p[1] == '######':
        p[0] = '<h6>' + p[2] + '</h6>\n'

def p_exp_sheader1(p):
    "expression : SH1"
    p[0] = '<h1>' + '</h1>\n'

def p_exp_sheader2(p):
    "expression : SH2"
    p[0] = '<h2>' + '</h2>\n'

def p_exp_factor(p):
    '''expression : expression factor
                | factor'''
    if len(p) == 3:
        p[0] = p[1] + ' ' + p[2]
    else:
        p[0] = p[1]
    
def p_factor_strong(p):
    "factor : STRONG factor STRONG"
    p[0] = '<strong>' + p[2] + "</strong>"

def p_factor_em(p):
    "factor : EM factor EM"
    p[0] = '<em>' + p[2] + "</em>"

def p_factor_subfactor(p):
    '''factor : factor subfactor
            | subfactor'''
    if len(p) == 3:
        p[0] = p[1] + ' ' + p[2]
    else:
        p[0] = p[1] 

def p_subfactor(p):
    "subfactor : TEXT"
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