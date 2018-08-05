from simplex import Token, Tokenizer


# Tokenizer configuration
def handler_generic(match_object, kind, value, keywords, state):
    if kind == 'ID' and value in keywords:
        kind = value
    column = match_object.start() - state['line_start']
    return Token(kind, value, state['line_num'], column)


def handler_mismatch(match_object, kind, value, keywords, state):
    raise RuntimeError('{value!r} unexpected on line {line_num}'.format(value=value, line_num=state['line_num']))


def handler_skip(match_object, kind, value, keywords, state):
    return None


def handler_newline(match_object, kind, value, keywords, state):
    state['line_start'] = match_object.end()
    state['line_num'] += 1


tokenizer = Tokenizer({
    'line_num' : 1,
    'line_start' : 0
})

tokenizer.add_token('NUMBER', r'\d+(\.\d*)?', handler_generic) # Integer or decimal number
tokenizer.add_token('ASSIGN', r':=', handler_generic) # Assignment operator
tokenizer.add_token('END', r';', handler_generic) # Statement terminator
tokenizer.add_token('ID', r'[A-Za-z]+', handler_generic) # Identifiers
tokenizer.add_token('OP', r'[+\-*/]', handler_generic) # Arithmetic operators
tokenizer.add_token('NEWLINE', r'\n', handler_newline) # Line endings
tokenizer.add_token('SKIP', r'[ \t]+', handler_skip) # Skip over spaces and tabs
tokenizer.add_token('MISMATCH', r'.', handler_mismatch) # Any other character

keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}
for kw in keywords:
    tokenizer.add_keyword(kw)

# Tokenizing
statements = '''
    IF quantity THEN
        total := total + price * quantity;
        tax := price * 0.05;
    ENDIF;
'''

for token in tokenizer.tokenize(statements):
    print(token)
