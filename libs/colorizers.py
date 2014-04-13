__author__ = 'zblach'

import re

import colors as ansicolors

class DefaultColors(object):
    def __getattr__(self, name):
        #print name, "unknown"
        return self.default
       
    def default(self, token):
        return ansicolors.blue(token)
    
    def number(self, token):
        return ansicolors.color(token, fg=243)


class UglyRainbowHex(DefaultColors):
    def hexes(self,token):
        stream = ""
        for chr in re.findall("[0-9A-Fa-f]{2}", token):
            stream += ansicolors.color(chr, fg=int(chr, 16))

        return stream


class NicerRainbowHex(DefaultColors):
    char_ansicolors = range(124, 231)

    def hexes(self,token):
        stream = ""
        for chr in re.findall("[0-9A-Fa-f]{2}", token):
            scale = (int(chr, 16) / 256.0) * len(NicerRainbowHex.char_ansicolors)
            stream += ansicolors.color(chr, fg=NicerRainbowHex.char_ansicolors[int(scale)])

        return stream


class BracketCounter(DefaultColors):
    bracket_ansicolors = [196, 208, 220, 154, 87, 119, 52]
    default_color = 243
    bracket_index = 0

    def raw_text(self,token):
        constructed = ""
        for c in token:
            if c in "<({[":
                constructed += ansicolors.color(c, fg=BracketCounter.bracket_ansicolors[
                    BracketCounter.bracket_index % len(BracketCounter.bracket_ansicolors)])
                BracketCounter.bracket_index += 1
            elif c in ">)}]":
                BracketCounter.bracket_index -= 1
                constructed += ansicolors.color(c, fg=BracketCounter.bracket_ansicolors[
                    BracketCounter.bracket_index % len(BracketCounter.bracket_ansicolors)])
            else:
                constructed += ansicolors.color(c, fg=BracketCounter.default_color)

        return constructed


class Composite(DefaultColors):
    @staticmethod
    def raw_text(token):
        return BracketCounter().raw_text(token)

    @staticmethod
    def hexes(token):
        return NicerRainbowHex().hexes(token)
