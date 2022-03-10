# -*- coding: utf-8 -*-
import time
import keyboard
import re


mapper = {
    '1': 'a',
    '2': 's',
    '3': 'd',
    '4': 'f',
    '5': 'g',
    '6': 'h',
    '7': 'j',
    '1+': 'q',
    '2+': 'w',
    '3+': 'e',
    '4+': 'r',
    '5+': 't',
    '6+': 'y',
    '7+': 'u',
    '1-': 'z',
    '2-': 'x',
    '3-': 'c',
    '4-': 'v',
    '5-': 'b',
    '6-': 'n',
    '7-': 'm',
    '0': None
}


class Token:
    def __init__(self, type, code):
        self.code = code
        if(type == 'single'):
            result = re.match(r'(\d[+-]?)(.*)', code).groups()
            self.key = [mapper[result[0]]]
            if len(result[1]) == 0:
                self.beat = 1
            elif result[1][0] == 'x':
                self.beat = int(result[1][1])
            else:
                self.beat = 1. / int(result[1][1])
        else:
            result = re.match(r'\(((?:\d[+-]?)+)\)(.*)', code).groups()
            self.key = [mapper[k] for k in re.findall(r'\d[+-]?', result[0])]
            if len(result[1]) == 0:
                self.beat = 1
            elif result[1][0] == 'x':
                self.beat = int(result[1][1])
            else:
                self.beat = 1. / int(result[1][1])
    
    def execute(self, beatTime=2):
        cmdStr = '+'.join([k for k in self.key if k is not None])
        print('按键: {}  编码: {}'.format(cmdStr, self.code))
        if len(cmdStr) != 0:
            keyboard.press(cmdStr)
            time.sleep(self.beat * beatTime / 4)
            keyboard.release(cmdStr)
        else: 
            time.sleep(self.beat * beatTime / 4)


class Parser:
    def __init__(self, txt=''):
        self.tokens = self.parse(''.join(txt.split()))

    def parse(self, txt):
        pattern = re.compile(
            r'(\((?:\d[+-]?)+\)(?:[x/]\d)?)|(\d[+-]?(?:[x/]\d)?)')
        tokens = pattern.findall(txt)
        result = []
        for token in tokens:
            result.append(Token('multi', token[0]) if len(
                token[0]) != 0 else Token('single', token[1]))
        return result

    def execute(self, beatTime=2):
        for token in self.tokens:
            token.execute(beatTime)



time.sleep(3)
with open('./music.txt', 'r') as f:
    data = f.read()
    par = Parser(data)
    par.execute(3.4)

