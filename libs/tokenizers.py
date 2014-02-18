import re
from libs import enum
from libs.colorizers import DefaultColors

__author__ = 'zblach'


class Tokenizer(object):
    fitness_state = enum('DEFINITELY', 'PROBABLY', 'MAYBE', 'POSSIBLY', 'NEGATORY')

    color_scheme = DefaultColors
    def set_color_scheme(self, color_scheme):
        self.color_scheme = color_scheme


    @staticmethod
    def syntax_fitness_check(line):
        raise NotImplementedError("this method requires an override")

    def tokenize(self, line):
        raise NotImplementedError("this method requires an override")

    def consume(self, line):
        raise NotImplementedError("this method requires an override")


class XXDTokenizer(Tokenizer):
    return_tokens = enum('LINE_NUMBER', 'HEX_WORD', 'CHAR_SET', 'RAW_STRING')
    parse_states = enum('UNKNOWN', 'SKIP', 'SUCCESS')

    color_scheme = DefaultColors

    @staticmethod
    def syntax_fitness_check(line):
        if re.match("^([0-9a-fA-F]+): ([0-9a-fA-F]+ )+ (.*)$", line):
            return Tokenizer.fitness_state.DEFINITELY
        else:
            return Tokenizer.fitness_state.NEGATORY


    def tokenize(self, line):
        try:
            num, line = line.split(":", 1)
            dat, line = line.split("  ", 1)
            dat = [(XXDTokenizer.return_tokens.HEX_WORD, ch) for ch in re.findall("[0-9A-Fa-f]+", dat)]
            return (XXDTokenizer.parse_states.SUCCESS,
                    [(XXDTokenizer.return_tokens.LINE_NUMBER, num), (XXDTokenizer.return_tokens.CHAR_SET, dat),
                     (XXDTokenizer.return_tokens.RAW_STRING, line)])
        except:
            return (XXDTokenizer.parse_states.UNKNOWN, line)

    def consume(self, tokens):
        (state, tokens) = tokens

        if state == XXDTokenizer.parse_states.SUCCESS:
            line = ""
            for (state, token) in tokens:
                if state == XXDTokenizer.return_tokens.LINE_NUMBER:
                    line += self.color_scheme.number(token) + ": "
                elif state == XXDTokenizer.return_tokens.CHAR_SET:
                    for (type, phrase) in token:
                        if type == XXDTokenizer.return_tokens.HEX_WORD:
                            line += self.color_scheme.hexes(phrase) + " "
                    line += " "
                elif state == XXDTokenizer.return_tokens.RAW_STRING:
                    line += self.color_scheme.raw_string(token)
                else:
                    return self.color_scheme.unknown(token)

            return line
        else:
            return self.color_scheme.unknown(tokens)


class XXDBinaryTokenizer(XXDTokenizer):
    @staticmethod
    def syntax_fitness_check(line):
        if re.match("^([0-9a-fA-F]+): ([01]+ )+ (.*)$", line):
            return Tokenizer.fitness_state.DEFINITELY
        elif re.match("^\*$", line):
            return Tokenizer.fitness_state.POSSIBLY
        else:
            return Tokenizer.fitness_state.NEGATORY


class HexdumpTokenizer(Tokenizer):
    @staticmethod
    def syntax_fitness_check(line):
        if re.match("^([0-9a-fA-F]+)( [0-9a-fA-F]+)+$", line):
            return Tokenizer.fitness_state.DEFINITELY
        elif re.match("^\*$", line):
            return Tokenizer.fitness_state.POSSIBLY
        else:
            return Tokenizer.fitness_state.NEGATORY
