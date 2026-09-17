# json_parser.py

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"


def tokenize(text):
    tokens = []
    i = 0
    n = len(text)

    while i < n:
        ch = text[i]

        # Whitespace
        if ch in ' \t\n\r':
            i += 1
            continue

        # Structural characters
        if ch in '{}[],:':
            tokens.append(Token(ch, ch))
            i += 1
            continue

        # String
        if ch == '"':
            i += 1
            start = i
            while i < n and text[i] != '"':
                if text[i] == '\\':
                    i += 2
                    continue
                i += 1
            tokens.append(Token('STRING', text[start:i]))
            i += 1
            continue

        # Number
        if ch == '-' or ch.isdigit():
            start = i
            while i < n and (text[i].isdigit() or text[i] in '-+.eE'):
                i += 1
            tokens.append(Token('NUMBER', text[start:i]))
            continue

        # Literals: true, false, null
        if text[i:i+4] == 'true':
            tokens.append(Token('TRUE', True))
            i += 4
            continue
        if text[i:i+5] == 'false':
            tokens.append(Token('FALSE', False))
            i += 5
            continue
        if text[i:i+4] == 'null':
            tokens.append(Token('NULL', None))
            i += 4
            continue

        raise ValueError(f"Unexpected character: {ch!r} at position {i}")

    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected_type=None):
        token = self.peek()
        if token is None:
            raise ValueError("Unexpected end of input")
        if expected_type and token.type != expected_type:
            raise ValueError(f"Expected {expected_type}, got {token.type}")
        self.pos += 1
        return token

    def parse(self):
        return self.parse_value()

    def parse_value(self):
        token = self.peek()
        if token is None:
            raise ValueError("Unexpected end of input")

        if token.type == '{':
            return self.parse_object()
        if token.type == '[':
            return self.parse_array()
        if token.type == 'STRING':
            return self.consume().value
        if token.type == 'NUMBER':
            raw = self.consume().value
            return float(raw) if '.' in raw or 'e' in raw.lower() else int(raw)
        if token.type == 'TRUE':
            self.consume()
            return True
        if token.type == 'FALSE':
            self.consume()
            return False
        if token.type == 'NULL':
            self.consume()
            return None

        raise ValueError(f"Unexpected token: {token}")

    def parse_object(self):
        self.consume('{')
        obj = {}

        if self.peek() and self.peek().type == '}':
            self.consume('}')
            return obj

        while True:
            key_token = self.consume('STRING')
            self.consume(':')
            value = self.parse_value()
            obj[key_token.value] = value

            next_token = self.peek()
            if next_token.type == ',':
                self.consume(',')
                continue
            if next_token.type == '}':
                self.consume('}')
                break
            raise ValueError(f"Expected ',' or '}}', got {next_token.type}")

        return obj

    def parse_array(self):
        self.consume('[')
        arr = []

        if self.peek() and self.peek().type == ']':
            self.consume(']')
            return arr

        while True:
            arr.append(self.parse_value())

            next_token = self.peek()
            if next_token.type == ',':
                self.consume(',')
                continue
            if next_token.type == ']':
                self.consume(']')
                break
            raise ValueError(f"Expected ',' or ']', got {next_token.type}")

        return arr

def loads(text):
    """Parse a JSON string into a Python object."""
    tokens = tokenize(text)
    parser = Parser(tokens)
    return parser.parse()


def dumps(obj, indent=0):
    """Convert a Python object to a JSON string."""
    sp = '  ' * indent

    if obj is None:
        return 'null'
    if obj is True:
        return 'true'
    if obj is False:
        return 'false'
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        return '"' + obj.replace('"', '\\"') + '"'
    if isinstance(obj, list):
        if not obj:
            return '[]'
        items = [sp + '  ' + dumps(item, indent + 1) for item in obj]
        return '[\n' + ',\n'.join(items) + '\n' + sp + ']'
    if isinstance(obj, dict):
        if not obj:
            return '{}'
        items = [
            sp + '  ' + dumps(str(k)) + ': ' + dumps(v, indent + 1)
            for k, v in obj.items()
        ]
        return '{\n' + ',\n'.join(items) + '\n' + sp + '}'

    raise TypeError(f"Cannot serialize {type(obj)}")