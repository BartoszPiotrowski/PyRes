#!/usr/bin/env python3
# ----------------------------------
#
# Module pyres-fof.py

"""pyres-fof.py 1.1

Usage: pyres-fof.py [options] <problem_file>

This is a straightforward implementation of a simple resolution-based
prover for full first-order logic. The problem file should be in
TPTP-3 CNF/FOF syntax. Unsupported features include double quoted
strings/distinct objects. Equality is parsed, and will by default be
dealt with by adding equality axioms for all function- and predicate
symbols.

Options:

 -h
--help
  Print this help.

 -t
--delete-tautologies
  Discard the given clause if it is a tautology.

 -f
--forward-subsumption
  Discard the given clause if it is subsumed by a processed clause.

 -b
--backward-subsumption
  Discard processed clauses if they are subsumed by the given clause.

 -H <heuristic>
--given-clause-heuristic=<heuristic>
  Use the specified heuristic for given-clause selection.

 -n
--neg-lit-selection
  Use the specified negative literal selection function.

 -S
--suppress-eq-axioms
  Do not add equality axioms. This makes the prover incomplete for
  equality problems.


Copyright 2011-2019 Stephan Schulz, schulz@eprover.org

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

import sys
import getopt
from lexer import Token,Lexer
from derivations import enableDerivationOutput,disableDerivationOutput,Derivable,flatDerivation
from clausesets import ClauseSet
from clauses import firstLit, varSizeLit, eqResVarSizeLit
from fofspec import FOFSpec
from heuristics import GivenClauseHeuristics
from saturation import SearchParams,ProofState
from litselection import LiteralSelectors


suppressEqAxioms = False
silent           = False
indexed          = False

def processOptions(opts):
    """
    Process the options given
    """
    global silent, indexed, suppressEqAxioms

    params = SearchParams()
    for opt, optarg in opts:
        if opt == "-h" or opt == "--help":
            print(__doc__)
            sys.exit()
        elif opt=="-s" or opt == "--silent":
            silent = True
        elif opt=="-i" or opt == "--index":
            indexed = True
        elif opt=="-t" or opt == "--delete-tautologies":
            params.delete_tautologies = True
        elif opt=="-f" or opt == "--forward-subsumption":
            params.forward_subsumption = True
        elif opt=="-b" or opt == "--backward_subsumption":
            params.backward_subsuption = True
        elif opt=="-H" or opt == "--given-clause-heuristic":
            try:
                params.heuristics = GivenClauseHeuristics[optarg]
            except KeyError:
                print("Unknown clause evaluation function", optarg)
                print("Supported:", GivenClauseHeuristics.keys())
                sys.exit(1)
        elif opt=="-n" or opt == "--neg-lit-selection":
            try:
                params.literal_selection = LiteralSelectors[optarg]
            except KeyError:
                print("Unknown literal selection function", optarg)
                print("Supported:", LiteralSelectors.keys())
                sys.exit(1)
        elif opt=="-S" or opt=="--suppress-eq-axioms":
            suppressEqAxioms = True

    return params

if __name__ == '__main__':
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],
                                       "hsitfbH:n:S",
                                       ["help",
                                        "silent",
                                        "index",
                                        "delete-tautologies",
                                        "forward-subsumption",
                                        "backward-subsumption"
                                        "given-clause-heuristic=",
                                        "neg-lit-selection="
                                        "supress-eq-axioms"])
    except getopt.GetoptError as err:
        print(sys.argv[0],":", err)
        sys.exit(1)

    params = processOptions(opts)

    problem = FOFSpec()
    for file in args:
        problem.parse(file)

    if not suppressEqAxioms:
        problem.addEqAxioms()
    cnf = problem.clausify()

    state = ProofState(params, cnf, silent, indexed)
    res = state.saturate()

    if res != None:
        if problem.isFof and problem.hasConj:
            print("# SZS status Theorem")
        else:
            print("# SZS status Unsatisfiable")
        proof = res.orderedDerivation()
        enableDerivationOutput()
        print("# SZS output start CNFRefutation")
        for s in proof:
            print(s)
        print("# SZS output end CNFRefutation")
        disableDerivationOutput()
    else:
        if problem.isFof and problem.hasConj:
            print("# SZS status CounterSatisfiable")
        else:
            print("# SZS status Satisfiable")
        dummy = Derivable("dummy", flatDerivation("pseudoreference", state.processed.clauses))
        sat = dummy.orderedDerivation()
        enableDerivationOutput()
        print("# SZS output start Saturation")
        for s in sat[:-1]:
            print(s)
        print("# SZS output end Saturation")
        disableDerivationOutput()
    print(state.statisticsStr())