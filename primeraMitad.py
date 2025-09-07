from collections import deque
import re

def tokenize(expression):
    token_pattern = r'[A-Za-z0-9]|\*|\+|\(|\)|\.|\||\?'
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

        if token.isalnum() or token=='?':
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

    return' '.join(queue)
# print(shunting_yard("(A.Z)+.(?|C*)"))
# shunting_yard("(?|1).1")



def regex_AFN_McYamadaSon(regexp): # regexp: ya en postfix
    efectos = {
        '*': 1,
        '+': 1,
        '.': 2,
        '|': 2,
    }
    stack = deque()
    contador = 0
    
    if isinstance(regexp, str):
        regexp = regexp.replace(" ", "")
    
    def new_state():
        nonlocal contador
        name = "q" + str(contador)
        contador += 1
        return name
    
    transiciones = []
    estados = set()
    simbolos_set = set()
    
    for token in regexp:
        if token.isalnum() or token == '?':  
            s = new_state()
            t = new_state()
            symbol = '?' if token == '?' else token  
            transiciones.append([s, symbol, t])
            estados.update([s, t])  
            simbolos_set.add(symbol)
            stack.append({'start': s, 'accept': t})
        elif token in efectos:
            if efectos[token] == 1:  # '*' o '+'
                if not stack:
                    raise ValueError(f"Expresión inválida: operador unario '{token}' sin operando")
                frag = stack.pop()
                s_new = new_state()
                t_new = new_state()
                estados.update([s_new, t_new])
                transiciones.append([s_new, '?', frag['start']])
                transiciones.append([frag['accept'], '?', frag['start']])
                transiciones.append([frag['accept'], '?', t_new])
                if token == '*':
                    transiciones.append([s_new, '?', t_new])
                stack.append({'start': s_new, 'accept': t_new})
            elif efectos[token] == 2:  # '.' o '|'
                if len(stack) < 2:
                    raise ValueError(f"Expresión inválida: operador binario '{token}' con menos de 2 operandos")
                frag_right = stack.pop()
                frag_left = stack.pop()
                if token == '.':
                    transiciones.append([frag_left['accept'], '?', frag_right['start']])
                    estados.update([frag_left['start'], frag_left['accept'], frag_right['start'], frag_right['accept']])
                    stack.append({'start': frag_left['start'], 'accept': frag_right['accept']})
                elif token == '|':
                    s_new = new_state()
                    t_new = new_state()
                    estados.update([s_new, t_new, frag_left['start'], frag_left['accept'], frag_right['start'], frag_right['accept']])
                    transiciones.append([s_new, '?', frag_left['start']])
                    transiciones.append([s_new, '?', frag_right['start']])
                    transiciones.append([frag_left['accept'], '?', t_new])
                    transiciones.append([frag_right['accept'], '?', t_new])
                    stack.append({'start': s_new, 'accept': t_new})
        else:
            raise ValueError(f"Token inesperado en la regexp postfix: '{token}'")
    
    if len(stack) != 1:
        raise ValueError("Expresión postfix inválida: quedan fragmentos sin combinar o falta operadores")
    
    final_frag = stack.pop()
    estados_list = sorted(list(estados), key=lambda x: int(x[1:]))
    simbolos = sorted(list(simbolos_set))
    
    automata = {
        "estados": estados_list,
        "simbolos": simbolos,
        "inicio": final_frag['start'],
        "aceptacion": [final_frag['accept']],
        "transiciones": transiciones
    }
    return automata

# print(shunting_yard("(0.0|1)*.1.(0|1)"))
# print(regex_AFN_McYamadaSon(shunting_yard("(0.0|1)*.1.(0|1)")))