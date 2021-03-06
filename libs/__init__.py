__author__ = 'zblach'


def enum(*sequential, **named):
    return type('Enum', (), dict(zip(sequential, sequential), **named))

from libs.tokenizers import Tokenizer

def list_languages():
    languages = {}
    for (k, v) in tokenizers.__dict__.items():
        try:
            if issubclass(v, tokenizers.Tokenizer):
                languages[v] = (len(v.mro()[:-1]), Tokenizer.fitness_state.POSSIBLY)
        except:
            pass

    languages.pop(tokenizers.Tokenizer) # abstract class
    return languages

def determine_language(stream):
    languages = list_languages()
    precache = []
    while True:
        line = stream.readline()
        precache += [line]
        states = []
        for l, (d, s) in languages.copy().items():
            state = l.syntax_fitness_check(line[:-1])
            if state != Tokenizer.fitness_state.NEGATORY:
                states += [state]
                languages[l] = (d, state)
            else:
                languages.pop(l)
        
        if (states == []):
            
            raise(SyntaxError("Couldn't determine language."))
        
        if len(languages) == 1 or (
                    len(set(states)) == 1 and states[0] == Tokenizer.fitness_state.DEFINITELY):
            break

    max_d = -1
    candidate_language = None

    for l, (d, s) in languages.items():
        if d > max_d:
            d = max_d
            candidate_language = l
        
    return (candidate_language, precache)
