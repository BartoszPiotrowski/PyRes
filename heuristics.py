#!/usr/bin/env python3
# ----------------------------------
#
# Module heuristics.py

"""
This module implements heuristic evaluation functions for clauses.
The purpose of heuristic evaluation is selection of clauses during the
resolution process.

A heuristical evaluation function is a function h:Clauses(F,P,X)->R
(where R denotes the set of real numbers, or, in the actual
implementation, the set of floating point numbers).

A lower value of h(C) for some clause C implies that C is assumed to
be better (or more useful) in a given proof search, and should be
processed before a clause C' with larger value h(C').

Copyright 2010-2019 Stephan Schulz, schulz@eprover.org

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program ; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston,
MA  02111-1307 USA

The original copyright holder can be contacted as

Stephan Schulz
Auf der Altenburg 7
70376 Stuttgart
Germany
Email: schulz@eprover.org
"""

import unittest
from lexer import Lexer
import clauses
import numpy as np


class ClauseEvaluationFunction(object):
    """
    A class representing a clause evaluation function. This is a pure
    virtual class, and it really is just a wrapper around the given
    clause evaluation function. However, some heuristics may need
    to be able to store information, either from initialization, or
    from previous calls.
    """

    def __init__(self): # pragma: nocover
        """
        Initialize the evaluaton function.
        """
        self.name = "Virtual Base"

    def __repr__(self): # pragma: nocover
        """
        Return a string representation of the clause.
        """
        return "ClauseEvalFun(%s)"%(self.name,)

    def __call__(self, clause):
        """
        Provide this as a callable function.
        """
        return self.hEval(clause)

    def hEval(self, clause): # pragma: nocover
        """
        This needs to be overloaded...
        """
        assert False and "Virtual base class is not callable"


class FIFOEvaluation(ClauseEvaluationFunction):
    """
    Class implementing first-in-first-out evaluation - i.e. clause
    evalutations increase over time (and independent of the clause).
    """
    def __init__(self):
        """
        Initialize object.
        """
        self.name        = "FIFOEval"
        self.fifocounter = 0

    def hEval(self, clause):
        """
        Actual evaluation function.
        """
        self.fifocounter = self.fifocounter + 1
        return self.fifocounter


class SymbolCountEvaluation(ClauseEvaluationFunction):
    """
    Implement a standard symbol counting heuristic.
    """
    def __init__(self, fweight=2, vweight=1):
        """
        Initialize heuristic.
        """
        self.fweight = fweight
        self.vweight = vweight
        self.name    = "SymbolCountEval(%f,%f)"%(fweight,vweight)

    def hEval(self, clause):
        """
        Actual evaluation function.
        """
        return clause.weight(self.fweight, self.vweight)


class EvalStructure(object):
    """
    Represent a heuristic clause processing schema. The scheme
    contains several different evaluation functions, and a way to
    alternate between them. Concretely, each evaluation function is
    paired with a counter, and clauses are picked according to each
    function in a weighted round-robin scheme.
    """
    def __init__(self, eval_descriptor):
        """
        Initialize ths structure. The argument is a list of pairs,
        where each pair consists of a function and its relative weight
        count.
        """
        assert len(eval_descriptor)
        self.eval_funs = [pair[0] for pair in eval_descriptor]
        self.eval_vec  = [pair[1] for pair in eval_descriptor]
        self.current = 0
        self.current_count = self.eval_vec[0]

    def evaluate(self, clause):
        """
        Return a composite evaluation of the clause.
        """
        evals = [f(clause) for f in self.eval_funs]
        return evals

    def nextEval(self, *args):
        """
        Return the index of the next evaluation function of the scheme.
        """
        while not self.current_count:
            self.current = (self.current+1) % len(self.eval_vec)
            self.current_count = self.eval_vec[self.current]
        self.current_count = self.current_count - 1
        return self.current


class EvalStructureByPolicyModel(EvalStructure):
    """
    Chooses evaluation function using a neural net.
    """
    def __init__(self, eval_functions, policy_model_path, policy_eval_mode):
        """
        Initialize ths structure. The first argument is a list of evaluation
        functions, the second argument is a path to a neural model deciding
        which evaluation function to use in the current proof state.
        """
        from policy_model import PolicyModel
        assert len(eval_functions)
        self.eval_funs = eval_functions
        self.model = PolicyModel()
        self.model.load(policy_model_path)
        self.policy_eval_mode=policy_eval_mode

    def nextEval(self, proof_state_vector):
        """
        Return the index of the next evaluation function of the scheme.
        """
        self.current = self.model.predict(proof_state_vector,
                                          policy_mode=self.policy_eval_mode)
        #self.current = np.random.choice(len(self.eval_funs), p=probabilities)
        return self.current


class EvalStructureBySampling(EvalStructure):
    """
    Chooses evaluation function by sampling according to provided probabilities.
    """
    def __init__(self, eval_functions, probabilities):
        """
        Initialize ths structure. The first argument is a list of evaluation
        functions, the second argument is a list of probabilities for choosing
        the evaluation functions.
        """
        assert len(eval_functions)
        assert sum(probabilities) == 1
        self.eval_funs = eval_functions
        self.probabilities = probabilities

    def nextEval(self, *args):
        """
        Return the index of the next evaluation function of the scheme.
        """
        self.current = np.random.choice(len(self.eval_funs), p=self.probabilities)
        return self.current


FIFOEval        = EvalStructure([(FIFOEvaluation(),1)])
"""
Strict first-in/first out evaluation. This is obviously fair
(i.e. every clause will be picked eventuall), but not a good search
strategy.
"""

SymbolCountEval = EvalStructure([(SymbolCountEvaluation(2,1),1)])
"""
Strict symbol counting (a smaller clause is always better than a
larger clause). This is only fair if subsumption or a similar
mechanism is employed, otherwise there can e.g. be an infinite set of
clauses p(X1), p(X2), p(X3),.... that are all smaller than q(f(X)), so
that the latter is never selected.
"""

PickGiven5      = EvalStructure([(SymbolCountEvaluation(2,1),5),
                                 (FIFOEvaluation(),1)])
"""
Experiences have shown that picking always the smallest clause (by
symbol count) isn't optimal, but that it pays off to interleave smallest
and oldest clause. The ratio between the two schemes is sometimes
called the "pick-given ratio", and, according to folklore, Larry Wos
has stated that "the optimal pick-given ratio is five." Since he is a
very smart person we use this value here.
"""

PickGiven2      = EvalStructure([(SymbolCountEvaluation(2,1),2),
                                 (FIFOEvaluation(),1)])
"""
See above, but now with a pick-given ration of 2 for easier testing.
"""

PolicyModelHeuristic = lambda policy_model_path, policy_eval_mode: \
    EvalStructureByPolicyModel(
        [SymbolCountEvaluation(2,1), FIFOEvaluation()],
        policy_model_path, policy_eval_mode
    )

RandomHeuristic = lambda probabilities: EvalStructureBySampling(
                                [SymbolCountEvaluation(2,1), FIFOEvaluation()],
                                probabilities)

GivenClauseHeuristics = {
    "FIFO"       : FIFOEval,
    "SymbolCount": SymbolCountEval,
    "PickGiven5" : PickGiven5,
    "PickGiven2" : PickGiven2}
"""
Table associating name and evaluation function, so that we can select
the function by name.
"""

class TestHeuristics(unittest.TestCase):
    """
    Test heuristic evaluation functions.
    """
    def setUp(self):
        """
        Setup function for tests. Create some clauses to test
        evaluations on.
        """

        print()
        self.spec ="""
cnf(c1,axiom,(f(X1,X2)=f(X2,X1))).
cnf(c2,axiom,(f(X1,f(X2,X3))=f(f(X1,X2),X3))).
cnf(c3,axiom,(g(X1,X2)=g(X2,X1))).
cnf(c4,axiom,(f(f(X1,X2),f(X3,g(X4,X5)))!=f(f(g(X4,X5),X3),f(X2,X1))|k(X1,X1)!=k(a,b))).
cnf(c5,axiom,(b=c|X1!=X2|X3!=X4|c!=d)).
cnf(c6,axiom,(a=b|a=c)).
cnf(c7,axiom,(i(X1)=i(X2))).
cnf(c8,axiom,(c=d|h(i(a))!=h(i(e)))).
"""
        lexer = Lexer(self.spec)
        self.c1 = clauses.parseClause(lexer)
        self.c2 = clauses.parseClause(lexer)
        self.c3 = clauses.parseClause(lexer)
        self.c4 = clauses.parseClause(lexer)
        self.c5 = clauses.parseClause(lexer)
        self.c6 = clauses.parseClause(lexer)
        self.c7 = clauses.parseClause(lexer)
        self.c8 = clauses.parseClause(lexer)


    def testFIFO(self):
        """
        Test that FIFO evaluation works as expected.
        """
        eval = FIFOEvaluation()
        e1 = eval(self.c1)
        e2 = eval(self.c2)
        e3 = eval(self.c3)
        e4 = eval(self.c4)
        e5 = eval(self.c5)
        e6 = eval(self.c6)
        e7 = eval(self.c7)
        e8 = eval(self.c8)
        self.assertTrue(e1<e2)
        self.assertTrue(e2<e3)
        self.assertTrue(e3<e4)
        self.assertTrue(e4<e5)
        self.assertTrue(e5<e6)
        self.assertTrue(e6<e7)
        self.assertTrue(e7<e8)

    def testSymbolCount(self):
        """
        Test that symbol counting works as expected.
        """
        eval = SymbolCountEvaluation(2,1)
        e1 = eval(self.c1)
        e2 = eval(self.c2)
        e3 = eval(self.c3)
        e4 = eval(self.c4)
        e5 = eval(self.c5)
        e6 = eval(self.c6)
        e7 = eval(self.c7)
        e8 = eval(self.c8)
        self.assertEqual(e1, self.c1.weight(2,1))
        self.assertEqual(e2, self.c2.weight(2,1))
        self.assertEqual(e3, self.c3.weight(2,1))
        self.assertEqual(e4, self.c4.weight(2,1))
        self.assertEqual(e5, self.c5.weight(2,1))
        self.assertEqual(e6, self.c6.weight(2,1))
        self.assertEqual(e7, self.c7.weight(2,1))
        self.assertEqual(e8, self.c8.weight(2,1))

    def testEvalStructure(self):
        """
        Test composite evaluations.
        """
        eval_funs = EvalStructure([(SymbolCountEvaluation(2,1),2),
                                   (FIFOEvaluation(),1)])

        evals = eval_funs.evaluate(self.c1)
        self.assertEqual(len(evals), 2)
        self.assertEqual(eval_funs.nextEval(),0)
        self.assertEqual(eval_funs.nextEval(),0)
        self.assertEqual(eval_funs.nextEval(),1)
        self.assertEqual(eval_funs.nextEval(),0)
        self.assertEqual(eval_funs.nextEval(),0)
        self.assertEqual(eval_funs.nextEval(),1)

#    def testEvalStructureByPolicyModel(self):
#        """
#        Test composite evaluations by a policy model.
#        """
#        eval_funs = EvalStructureByPolicyModel(
#                        [SymbolCountEvaluation(2,1), FIFOEvaluation()],
#                        'tmp/policy_model.pt')
#        evals = eval_funs.evaluate(self.c1)
#        next_eval = eval_funs.nextEval([1,2,3,4])
#        self.assertEqual(len(evals), 2)
#        self.assertTrue(next_eval < 2)

    def testEvalStructureBySampling(self):
        """
        Test composite evaluations by a policy model.
        """
        eval_funs = EvalStructureBySampling(
                        [SymbolCountEvaluation(2,1), FIFOEvaluation()],
                        [0.3, 0.7])

        evals = eval_funs.evaluate(self.c1)
        next_eval = eval_funs.nextEval()
        self.assertEqual(len(evals), 2)
        self.assertTrue(next_eval < 2)


if __name__ == '__main__':
    unittest.main()
