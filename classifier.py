import cast
import parser
import sys
import word2vec

if len(sys.argv) < 2:
    print('Please specify a movie to parse.')
    sys.exit(1)

word2vec.load()

user_input = input("String: ")

casts = []

for i in range(1, len(sys.argv)):
    arg = sys.argv[i]
    filename = arg + '.txt'

    script_data = parser.parse_script(filename)
    script_cast = cast.make_cast(script_data).filter(min_lines=20)

    casts.append(script_cast)

full_cast = cast.combine(casts)

wmdistances = []

for j, c in enumerate(full_cast):
    wmdistances.extend([(c.name, line, word2vec.wmdistance(parser.line_to_words(user_input), parser.line_to_words(line))) for line in c.lines])

wmdistances.sort(key=lambda x: x[2])
best_distances = wmdistances[:10]
for distance in best_distances:
  print(distance)
