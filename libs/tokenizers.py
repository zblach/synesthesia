import re
from libs import enum
from libs.colorizers import DefaultColors

__author__ = 'zblach'


class Tokenizer(object):
    fitness_state = enum('DEFINITELY', 'PROBABLY', 'MAYBE', 'POSSIBLY', 'NEGATORY')
    color_scheme = DefaultColors

    def __init__(self, colorscheme=DefaultColors):
        self.color_scheme = colorscheme()

    @staticmethod
    def syntax_fitness_check(line):
        raise NotImplementedError("this method requires an override")

    def tokenize(self, line):
        raise NotImplementedError("this method requires an override")

    def consume(self, line):
        raise NotImplementedError("this method requires an override")

class XXDTokenizer(Tokenizer):
    return_tokens = enum('LINE_NUMBER', 'WORD', 'ENCODED_DATA', 'RAW_STRING')
    parse_states = enum('UNKNOWN', 'SKIP', 'SUCCESS')

    color_scheme = DefaultColors()

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
            dat = [(XXDTokenizer.return_tokens.WORD, ch) for ch in re.findall("[0-9A-Fa-f]+", dat)]
            return (XXDTokenizer.parse_states.SUCCESS,
                    [(XXDTokenizer.return_tokens.LINE_NUMBER, num), (XXDTokenizer.return_tokens.ENCODED_DATA, dat),
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
                elif state == XXDTokenizer.return_tokens.ENCODED_DATA:
                    for (type, phrase) in token:
                        if type == XXDTokenizer.return_tokens.WORD:
                            line += self.color_scheme.hexes(phrase) + " "
                    line += " "
                elif state == XXDTokenizer.return_tokens.RAW_STRING:
                    line += self.color_scheme.raw_text(token)
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
        
    def tokenize(self, line):
        try:
            num, line = line.split(":", 1)
            dat, line = line.split("  ", 1)
            dat = [(XXDTokenizer.return_tokens.WORD, ch) for ch in re.findall("[01]+", dat)]
            return (XXDTokenizer.parse_states.SUCCESS,
                    [(XXDTokenizer.return_tokens.LINE_NUMBER, num), (XXDTokenizer.return_tokens.ENCODED_DATA, dat),
                     (XXDTokenizer.return_tokens.RAW_STRING, line)])
        except:
            return (XXDTokenizer.parse_states.UNKNOWN, line)
class HexdumpTokenizer(Tokenizer):
    @staticmethod
    def syntax_fitness_check(line):
        if re.match("^([0-9a-fA-F]+)( [0-9a-fA-F]+)+$", line):
            return Tokenizer.fitness_state.DEFINITELY
        elif re.match("^\*$", line):
            return Tokenizer.fitness_state.POSSIBLY
        else:
            return Tokenizer.fitness_state.NEGATORY
class KeyPrinter(Tokenizer):
    #return_tokens = enum('HEADER', 'OPTION', 'B64TEXT')
    tokens = {
        'HEADER': "^-{5}(BEGIN|END) .* KEY BLOCK-{5}$",
        'OPTION': "^([a-zA-Z]+): (.*)$",
        'B64TEXT' :"^[a-zA-Z0-9/+=]{64}$"
    }
    return_states = enum(
        'HEADER', 
        'OPTION', 
        'VALUE', 
        'B64TEXT', 
        'UNKNOWN')
   
    @staticmethod
    def interpretB64(string):
        (a,b,c) = string.decode("base64")
        
    
    @staticmethod
    def syntax_fitness_check(line):
        if re.match(KeyPrinter.tokens['HEADER'], line):
            return Tokenizer.fitness_state.DEFINITELY
        elif re.match(KeyPrinter.tokens['OPTION'], line):
            return Tokenizer.fitness_state.POSSIBLY
        elif re.match(KeyPrinter.tokens['B64TEXT'], line):
            return Tokenizer.fitness_state.POSSIBLY
        else:
            return Tokenizer.fitness_state.NEGATORY
        
    def tokenize(self, line):
        if re.match(self.tokens['HEADER'], line):
            return (KeyPrinter.return_states.HEADER, line)
        elif re.match(self.tokens['OPTION'], line):
            (_, opt, val, _) = re.split(self.tokens['OPTION'], line)
            return (KeyPrinter.return_states.OPTION,
                (
                    (KeyPrinter.return_states.OPTION, opt),
                    (KeyPrinter.return_states.VALUE, val)
                ))
        elif re.match(self.tokens['B64TEXT'], line):
            return (KeyPrinter.return_states.B64TEXT, line)
        else:
            return (KeyPrinter.return_states.UNKNOWN, line)
            
    def consume(self, tokens):
        (state, token) = tokens
        if state == KeyPrinter.return_states.OPTION:
            return self.color_scheme.number(token[0][1]) + ": " + self.color_scheme.default(token[1][1])
        elif state == KeyPrinter.return_states.HEADER:
            return self.color_scheme.number(token)
        elif state == KeyPrinter.return_states.UNKNOWN:
            return self.color_scheme.default(token)
        elif state == KeyPrinter.return_states.B64TEXT:
            consume = ""
            for quad in re.findall(".{4}", token):
                consume += self.color_scheme.default(quad[:-1]) + ' '
            return consume