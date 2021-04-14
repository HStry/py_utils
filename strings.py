from collections import OrderedDict

class NULL:
    pass

NULL = NULL()

SUPERSCRIPT = OrderedDict((('0', '\u2070'), ('1', '\u00B9'), ('2', '\u00B2'),
                           ('3', '\u00B3'), ('4', '\u2074'), ('5', '\u2075'),
                           ('6', '\u2076'), ('7', '\u2077'), ('8', '\u2078'),
                           ('9', '\u2079'), ('+', '\u207A'), ('-', '\u207B'),
                           ('=', '\u207C'), ('(', '\u207D'), (')', '\u207E'),
                           ('i', '\u2071'), ('n', '\u207F')))
SUBSCRIPT =   OrderedDict((('0', '\u2080'), ('1', '\u2081'), ('2', '\u2082'),
                           ('3', '\u2083'), ('4', '\u2084'), ('5', '\u2085'),
                           ('6', '\u2086'), ('7', '\u2087'), ('8', '\u2088'),
                           ('9', '\u2089'), ('+', '\u208A'), ('-', '\u208B'),
                           ('=', '\u208C'), ('(', '\u208D'), (')', '\u208E'),
                           ('a', '\u2090'), ('e', '\u2091'), ('h', '\u2095'),
                           ('k', '\u2096'), ('l', '\u2097'), ('m', '\u2098'),
                           ('n', '\u2099'), ('o', '\u2092'), ('p', '\u209A'),
                           ('s', '\u209B'), ('t', '\u209C'), ('x', '\u2093')))

def sup(chars=None, onKeyError=None):
    """Converts characters to subscript.
    
    :param chars:      String to convert to superscript.
    :param onKeyError: Action directive if the requested superscript character
                       isn't available. Passing a zero length string ('') will
                       result in the unavailable characters being silently
                       dropped. Passing a single character will result in
                       missing superscript characters being replaced by that
                       character. Passing a string of equal length to chars
                       will cause any unavailable character to be replaced by
                       the corresponding character in onKeyError.
                       The default value of None will raise KeyError.
    """
    if chars is None:
        print(''.join(SUPERSCRIPT.keys()))
    
    elif onKeyError is None:
        return ''.join(SUPERSCRIPT.get(c) for c in chars)
    
    elif len(onKeyError) <= 1:
        return ''.join(SUPERSCRIPT.get(c, onKeyError) for c in chars)
    
    elif len(onKeyError) == len(chars):
        return ''.join(SUPERSCRIPT.get(*c) for c in zip(chars, onKeyError))
    
    else:
        raise ValueError('Illegal value for onKeyError')

def sub(chars=None, onKeyError=None):
    """Converts characters to subscript.
    
    :param chars:      String to convert to subscript.
    :param onKeyError: Action directive if the requested subscript character
                       isn't available. Passing a zero length string ('') will
                       result in the unavailable characters being silently
                       dropped. Passing a single character will result in
                       missing subscript characters being replaced by that
                       character. Passing a string of equal length to chars
                       will cause any unavailable character to be replaced by
                       the corresponding character in onKeyError.
                       The default value of None will raise KeyError.
    """
    if chars is None:
        print(''.join(SUBSCRIPT.keys()))
    
    elif onKeyError is None:
        return ''.join(SUBSCRIPT.get(c) for c in chars)
    
    elif len(onKeyError) <= 1:
        return ''.join(SUBSCRIPT.get(c, onKeyError) for c in chars)
    
    elif len(onKeyError) == len(chars):
        return ''.join(SUBSCRIPT.get(*c) for c in zip(chars, onKeyError))
    
    else:
        raise ValueError('Illegal value for onKeyError')

def find(string, substring, overlap=True, casesensitive=True):
    """Finds all indices for substrings within a string, with or without
    overlap.
    
    :param string:        String to find substrings in.
    :param substring:     Substring to find
    :param overlap:       Return overlapping matches
    :param casesensitive: Require matching case.
    """
    
    if not casesensitive:
        string = string.lower()
        substring = substring.lower()
    
    if len(string) < len(substring):
        raise ValueError('Substring must be shorter than string')
    
    i = 0
    if overlap:
        n = 1
    else:
        n = max(1, len(substring))
    
    while i < len(string):
        if string[i:].startswith(substring):
            yield i
            i += n
        else:
            i += 1

def refind(string, pattern, overlap=True, casesensitive=True):
    """Finds all matches for regex pattern within a string, with or without
    overlap.
    
    :param string:        String to find pattern in.
    :param pattern:       Regex pattern to match. If re.Pattern type, will be
                          used without further processing. If string, and
                          pattern starts with '^(', it will be compiled as is.
                          Otherwise it will be wrapped with f'^({pattern})'
    :param overlap:       Return overlapping matches
    :param casesensitive: Require matching case.
    """
    
    def _match(s):
        match = pattern.match(s)
        match = match.group(0) if match else ''
        return max(1, 1 * (overlap or len(match))), match
    
    if not isinstance(pattern, re.Pattern):
        if not pattern.startswith('^('):
            pattern = f'^({pattern})'
        pattern = re.compile(pattern, (not casesensitive) * re.IGNORECASE)
    
    i = 0
    while i < len(string):
        n, match = _match(string[i:])
        
        if match:
            yield i, match
        i += n
