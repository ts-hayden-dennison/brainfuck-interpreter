#! usr/bin/env python
# interpreter for a simple stack-based language in Python
# copyright (C) 2012 Hayden Dennison <hayden@dennison7.com>
#This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# import system and os modules
import sys
import os

def toobig(instruction, datapointer):
    print 'Data pointer too big.'
    print 'Error occured at character: '+str(instruction)
    print 'Data pointer: '+str(datapointer)
    sys.exit()
    return

def toosmall(instruction, datapointer):
    print 'Data pointer too small.'
    print 'Error occured at character: '+str(instruction)
    print 'Data pointer: '+str(datapointer)
    sys.exit()
    return

def checkbounds(datapointer, stack):
    if datapointer >= 0 and datapointer < len(stack):
        return True
    else:
        return False
    return

# interpret the program
def interpret(code):
    # data pointer: points to the current byte in the stack
    datapointer = 0
    # points to the current character being interpreted
    instruction = 0
    # the program's "memory"
    stack = [0]*5000
    # interpret
    while instruction < len(code):
        char = code[instruction]
        if char == '>':
            #print 'increased data pointer by one'
            datapointer += 1
        elif char == '<':
            #print 'decreased data pointer by one'
            datapointer -= 1
        elif char == '+':
            if checkbounds(datapointer, stack):
                #print 'increased cell '+str(datapointer)+' by one'
                stack[datapointer] += 1
            else:
                if datapointer < 0:
                    toosmall(instruction, datapointer)
                else:
                    toobig(instruction, datapointer)
        elif char == '-':
            if checkbounds(datapointer, stack):
                #print 'decreased cell '+str(datapointer)+ ' by one'
                stack[datapointer] -= 1
            else:
                if datapointer < 0:
                    toosmall(instruction, datapointer)
                else:
                    toobig(instruction, datapointer)
        elif char == '.':
            if checkbounds(datapointer, stack):
                sys.stdout.write(chr(stack[datapointer]))
            else:
                if datapointer < 0:
                    toosmall(instruction, datapointer)
                else:
                    toobig(instruction, datapointer)
        elif char == ',':
            if checkbounds(datapointer, stack):
                byte = ''
                while len(byte) != 1:
                    byte = raw_input('Enter: ')
                stack[datapointer] = ord(byte)
            else:
                if datapointer < 0:
                    toosmall(instruction, datapointer)
                else:
                    toobig(instruction, datapointer)
        elif char == '[':
            #print 'read in a ['
            if checkbounds(datapointer, stack):
                if stack[datapointer] == 0:
                    #print str(datapointer)+' is zero, so find a matching ]'
                    try:
                        lefts = 1
                        rights = 0
                        while True:
                            instruction += 1
                            if code[instruction] == '[':
                                lefts += 1
                            if code[instruction] == ']':
                                rights += 1
                            if lefts == rights:
                                break
                        #print 'found a ] at '+str(instruction)
                    except:
                        print 'No matching "]" after "["'
                        print 'Error occured at character: '+str(instruction)
                        print 'Data pointer: '+str(datapointer)
                        sys.exit()
            else:
                if datapointer < 0:
                    toosmall(instruction, datapointer)
                else:
                    toobig(instruction, datapointer)
        elif char == ']':
            #print 'read in a ]'
            if checkbounds(datapointer, stack):
                if stack[datapointer] != 0:
                    #print str(datapointer)+' is not zero, so find a matching ['
                    try:
                        lefts = 0
                        rights = 1
                        while True:
                            instruction -= 1
                            if code[instruction] == '[':
                                lefts += 1
                            if code[instruction] == ']':
                                rights += 1
                            if lefts == rights:
                                break
                        #print 'found a [ at '+str(instruction)
                    except:
                        print 'No matching "[" before "]"'
                        print 'Error occured at character: '+str(instruction)
                        print 'Data pointer: '+str(datapointer)
                        sys.exit()
        instruction += 1
        #print 'added one to instruction at end of while'
    return

if __name__ == '__main__':
    # check to see if an input file is given
    if len(sys.argv) < 2:
        print 'run interpreter.py --help for instructions.'
        sys.exit()
    # help
    if '--help' in sys.argv:
        print '<python> interpreter.py <your bf program>'
        sys.exit()
    # see if the input file is valid
    filename = os.path.join(os.getcwd(), sys.argv[1])
    if not os.path.exists(filename):
        print 'No input file given.'
        sys.exit()
    # open the program file and extract the text
    program = open(filename, 'r')
    code = program.read()
    # don't forget to close it!
    program.close()
    # Run the code
    interpret(code)
    sys.exit()

