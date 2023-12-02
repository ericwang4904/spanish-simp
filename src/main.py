from less.config import horn_simplifier

input_file_path = 'less/data/horn/lex.mturk.es.txt'
candidates_file_path = 'less/data/horn/results/less_candidates.txt'
horn_simplifier.simplify(input_file_path, candidates_file_path)#
