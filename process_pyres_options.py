import getopt
from saturation import SearchParams
from litselection import LiteralSelectors


def processPyresOptions(options):

    version          = "1.2"
    suppressEqAxioms = False
    silent           = False
    indexed          = False
    proofObject      = False

    def processOptions(opts):
        """
        Process the options given
        """
        global silent, indexed, suppressEqAxioms, proofObject

        params = SearchParams()
        for opt, optarg in opts:
            if opt == "-h" or opt == "--help":
                print(__doc__)
                sys.exit()
            elif opt=="-s" or opt == "--silent":
                silent = True
            elif opt=="-V" or opt == "--version":
                print("# Version: ", version)
            elif opt=="-p" or opt == "--proof":
                proofObject = True
            elif opt=="-i" or opt == "--index":
                indexed = True
            elif opt=="-t" or opt == "--delete-tautologies":
                params.delete_tautologies = True
            elif opt=="-f" or opt == "--forward-subsumption":
                params.forward_subsumption = True
            elif opt=="-b" or opt == "--backward_subsumption":
                params.backward_subsumption = True
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
            elif opt=="-P" or opt == "--policy-model":
                params.heuristics = PolicyModelHeuristic(optarg)
            elif opt=="-S" or opt=="--suppress-eq-axioms":
                suppressEqAxioms = True

        return params


    try:
        opts, args = getopt.gnu_getopt(options.split(),
                                       "hsVpitfbH:P:n:S",
                                       ["help",
                                        "silent",
                                        "version",
                                        "proof",
                                        "index",
                                        "delete-tautologies",
                                        "forward-subsumption",
                                        "backward-subsumption"
                                        "given-clause-heuristic=",
                                        "policy-model=",
                                        "neg-lit-selection="
                                        "supress-eq-axioms"])
    except getopt.GetoptError as err:
        print(sys.argv[0],":", err)
        sys.exit(1)

    params = processOptions(opts)

    return {'main':params,
            'indexed':indexed,
            'suppressEqAxioms':suppressEqAxioms}
