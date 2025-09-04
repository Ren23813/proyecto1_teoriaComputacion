from collections import deque
import re

def tokenize(expression):
    token_pattern = r'[A-Za-z0-9]|\*|\+|\(|\)|\.|\|'
    tokens = re.findall(token_pattern, expression.replace(" ", ""))
    return tokens

def shunting_yard(input):
    stack = deque()         # stack.append() ; stack.pop()
    queue = deque()         # queue.append() ; queue.popLeft()
    tokens = tokenize(input)
    precedencia = {
        '*':3,
        '+':3,
        '.':2,
        '|':1,
    }
    asociatividad = {
        '*': 'r',
        '+': 'r',
        '.': 'l', 
        '|': 'l', 
    }

    for i in range(len(tokens)):
        token = tokens[i]

        if token.isalnum():
            queue.append(token)
        elif token =='(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                queue.append(stack.pop())
            stack.pop()
        elif token in precedencia:
            while (stack and stack[-1] in precedencia and
                   ((asociatividad[token] == 'l' and precedencia[token] <= precedencia[stack[-1]]) or
                    (asociatividad[token] == 'r' and precedencia[token] < precedencia[stack[-1]]))):
                queue.append(stack.pop())
            stack.append(token)
        if i + 1 < len(tokens) and tokens[i].isalnum() and tokens[i+1].isalnum():
            stack.append('.') 
    while stack:    
        queue.append(stack.pop())

    print("Queue (resultado postfix):" , ' '.join(queue))
# shunting_yard("(A.Z)+.(B|C*)")

