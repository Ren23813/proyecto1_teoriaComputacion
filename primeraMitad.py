from collections import deque
import re

def tokenize(expression):
    # RegEx para números (enteros), operadores y paréntesis
    token_pattern = r'\d+|\^|\*|\/|\+|\-|\(|\)'
    tokens = re.findall(token_pattern, expression.replace(" ", ""))
    return tokens


def shunting_yard(input):
    stack = deque()         # stack.append() ; stack.pop()
    queue = deque()         # queue.append() ; queue.popLeft()
    tokens = tokenize(input)
    precedencia = {
        '^':4,
        '*':3,
        '/':3,
        '+':2,
        '-':2
    }
    asociatividad = {
        '^': 'r', 
        '*': 'l', 
        '/': 'l', 
        '+': 'l', 
        '-': 'l'
    }

    for i in tokens:
        if i.isdigit():
            queue.append(i)
        elif i =='(':
            stack.append(i)
        elif i == ')':
            while stack and stack[-1] != '(':
                queue.append(stack.pop())
            stack.pop()
        elif i in precedencia:
            while (stack and stack[-1] in precedencia and
                   ((asociatividad[i] == 'l' and precedencia[i] <= precedencia[stack[-1]]) or
                    (asociatividad[i] == 'r' and precedencia[i] < precedencia[stack[-1]]))):
                queue.append(stack.pop())
            stack.append(i)
    while stack:
        queue.append(stack.pop())

    print("Queue (resultado postfix):" , ' '.join(queue))
# shunting_yard("3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3")

