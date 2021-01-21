from lexer import Token,Lexer
from derivations import Derivable,Derivation
from signature import Signature
from clauses import parseClause

from terms import *
import substitutions
from literals import Literal, parseLiteral, parseLiteralList,\
     literalList2String, litInLitList, oppositeInLitList
from litselection import firstLit, varSizeLit, eqResVarSizeLit

def distance(c1, c2):
    sig1 = c1.collectSig()
    sig2 = c2.collectSig()
    funs1 = set(sig1.funs)
    preds1 = set(sig1.preds)
    funs2 = set(sig2.funs)
    preds2 = set(sig2.preds)
    symb1 = funs1 | preds1
    symb2 = funs2 | preds2
    jacc = len(symb1 & symb2) / len(symb1 | symb2)
    return jacc

def distanceFromSet(set, c):
    dists = [distance(c, ci) for ci in set]
    avg_dist = sum(dists) / len(dists)
    set_weights = [c.weight(2,1) for c in set]
    avg_weight = sum(set_weights) / len(set_weights)
    prop_weight = avg_weight / max(c.weight(2,1), 1)
    norm_prop_weight = (1 - min(1, prop_weight))
    return (avg_dist + norm_prop_weight) / 2


if __name__ == '__main__':

    clauses = """
cnf(test,axiom,p(a)|r(f(X))).
cnf(test,axiom,(p(a)|p(f(X)))).
cnf(test3,lemma,(p(a)|~p(f(X)))).
cnf(taut,axiom,p(a)|q(a)|~p(a)).
cnf(dup,axiom,p(a)|q(a)|p(a)).
"""

    lex = Lexer(clauses)
    c1 = parseClause(lex)
    c2 = parseClause(lex)
    c3 = parseClause(lex)
    c4 = parseClause(lex)
    c5 = parseClause(lex)

    print(c1); print(c1)
    print(distance(c1, c1))

    print(c1); print(c3)
    print(distance(c1, c3))

    print(c1); print(c5)
    print(distance(c1, c5))

    s = [c1, c2, c3, c4]
    print(s)
    print(c5)
    print(distanceFromSet(s, c5))
