# Paarth Lakhani
# u0936913

import sys

pcfg_data_file = sys.argv[1]
sentences_data_file = sys.argv[2]
probabilistic_cky = False

if len(sys.argv) > 3:
    if sys.argv[3] == "-prob":
        probabilistic_cky = True


cfg_data = open('./data/' + pcfg_data_file, 'r')
sentences_data = open('./data/' + sentences_data_file, 'r')

cfg_grammar = cfg_data.readlines()
sentences = sentences_data.readlines()
cfg_grammar_dict = {}

if not probabilistic_cky:
    for rule in cfg_grammar:
        rule = rule.strip()
        symbols = rule.split("->")
        value = symbols[0].strip()
        key = symbols[1:]
        key = key[0].split(".")[0].strip()
        if key in cfg_grammar_dict:
            cfg_grammar_dict[key].append(value)
        else:
            cfg_grammar_dict[key] = [value]
else:
    for rule in cfg_grammar:
        rule = rule.strip()
        symbols = rule.split("->")
        value = symbols[0].strip()
        keyProb = symbols[1:][0].split(".")
        key = keyProb[0].strip()
        prob = "." + keyProb[1]
        if key in cfg_grammar_dict:
            cfg_grammar_dict[key].append(value + " " + prob)
        else:
            cfg_grammar_dict[key] = [value + " " + prob]


def cky_parsing(words):
    cky_parsing_array = [[[] for x in range(len(words))] for y in range(len(words))]

    for col in range(len(cky_parsing_array[0])):
        if words[col] in cfg_grammar_dict:
            cky_parsing_array[col][col] = cfg_grammar_dict.get(words[col])

        # Iterate over rows, from bottom to top
        for row in range(col - 1, -1, -1):
            list_terminals = []
            for partition in range(row + 1, col + 1):  # col+1 to capture the last col as well
                former_terminals = cky_parsing_array[row][partition - 1]
                latter_terminals = cky_parsing_array[partition][col]
                for former_terminal in former_terminals:
                    if len(latter_terminals) != 0:
                        for latter_terminal in latter_terminals:
                            potential_terminal_present = former_terminal + " " + latter_terminal
                            if potential_terminal_present in cfg_grammar_dict:
                                for terminal in cfg_grammar_dict.get(potential_terminal_present):
                                    list_terminals.append(terminal)
                                list_terminals.sort(reverse=True)
                                list_terminals.sort()
            cky_parsing_array[row][col] = list_terminals
    return cky_parsing_array


def probabilistic_cky_parsing(words):
    cky_parsing_array = [[[] for x in range(len(words))] for y in range(len(words))]

    for col in range(len(cky_parsing_array[0])):
        if words[col] in cfg_grammar_dict:
            cky_parsing_array[col][col] = cfg_grammar_dict.get(words[col])

        # Iterate over rows, from bottom to top
        for row in range(col - 1, -1, -1):
            list_terminals = []
            for partition in range(row + 1, col + 1):  # col+1 to capture the last col as well
                former_terminals = cky_parsing_array[row][partition - 1]
                latter_terminals = cky_parsing_array[partition][col]
                for former_terminal in former_terminals:
                    if len(latter_terminals) != 0:
                        for latter_terminal in latter_terminals:
                            potential_terminal_present = former_terminal.split(".")[0].strip() + " " + latter_terminal.split(".")[0].strip()
                            if potential_terminal_present in cfg_grammar_dict:
                                for terminal in cfg_grammar_dict.get(potential_terminal_present):
                                    former_prob = float("." + former_terminal.split(".")[1])
                                    latter_prob = float("." + latter_terminal.split(".")[1])
                                    terminal_prob = float("." + terminal.split(".")[1])
                                    final_terminal_prob = former_prob * latter_prob * terminal_prob
                                    terminal_add_to_list = terminal.split(".")[0] + str(" " + str(final_terminal_prob))
                                    if len(list_terminals) > 0:
                                        for terminalCheck in list_terminals:
                                            original_terminal = terminalCheck.split(".")[0]
                                            if original_terminal == terminal.split(".")[0]:
                                                if final_terminal_prob > float("." + terminalCheck.split(".")[1]):
                                                    list_terminals.append(terminal_add_to_list)
                                    else:
                                        list_terminals.append(terminal_add_to_list)
            cky_parsing_array[row][col] = list_terminals
    return cky_parsing_array


for sentence in sentences:
    words = sentence.strip().split()
    if not probabilistic_cky:
        parsed_grammar = cky_parsing(words)
        number_of_parsers = parsed_grammar[0][len(words) - 1].count("S")
        print("PARSING SENTENCE: " + sentence.strip())
        print("NUMBER OF PARSES FOUND: " + str(number_of_parsers))
        print("TABLE:")
        for row in range(len(parsed_grammar)):
            for col in range(len(parsed_grammar[0])):
                if row <= col:
                    if parsed_grammar[row][col]:
                        parsed_grammar[row][col].sort()
                        value = " ".join(parsed_grammar[row][col])
                        print("cell[" + str(row + 1) + "," + str(col + 1) + "]: " + value)
                    else:
                        print("cell[" + str(row + 1) + "," + str(col + 1) + "]: -")
        print("\n"),
    else:
        parsed_grammar = probabilistic_cky_parsing(words)
        print(parsed_grammar)
