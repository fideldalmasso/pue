import re
from collections import namedtuple
pattern = re.compile(r"""(?x)
    (?P<float2>\d+\.\d+) |
    (?P<int>\d+) |
    (?P<variable>\w+) |
    (?P<string>".*")
""",re.VERBOSE)

Token = namedtuple('Token', ('kind', 'value', 'position'))
env = {'x': 'hello', 'y': 10}

for s in ['123', '123.45', 'x', 'y', '"goodbye"']:
    mo = pattern.fullmatch(s)
    match mo.lastgroup:
        case 'float2':
            tok = Token('NUM', float(s), mo.span())
        case 'int':
            tok = Token('NUM', int(s), mo.span())
        case 'variable':
            tok = Token('VAR', env[s], mo.span())
        case 'string':
            tok = Token('TEXT', s[1:-1], mo.span())
        case _:
            raise ValueError(f'Unknown pattern for {s!r}')
    print(tok)