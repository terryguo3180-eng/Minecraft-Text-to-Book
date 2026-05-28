"""
usage: text2book.py [-h] [-o OUTPUT] [-t TITLE] [-a AUTHOR] input

Convert ASCII text into a /give command that gives the player a 
written book, with the text automatically split into pages and lines

positional arguments:
  input                Input file path

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output file path (default stdout)
  -t, --title TITLE    Title of the book (default test)
  -a, --author AUTHOR  Author of the book (default test)
"""
# TerryGuo 05/27/2026


import argparse


char_widths = {
    ' ': 4, '!': 1, '"': 3, '#': 5, '$': 5, '%': 5, '&': 5, "'": 1,
    '(': 3, ')': 3, '*': 3, '+': 5, ',': 1, '-': 5, '.': 1, '/': 5,
    '0': 5, '1': 5, '2': 5, '3': 5, '4': 5, '5': 5, '6': 5, '7': 5,
    '8': 5, '9': 5, ':': 1, ';': 1, '<': 4, '=': 5, '>': 4, '?': 5,
    '@': 6, 'A': 5, 'B': 5, 'C': 5, 'D': 5, 'E': 5, 'F': 5, 'G': 5,
    'H': 5, 'I': 3, 'J': 5, 'K': 5, 'L': 5, 'M': 5, 'N': 5, 'O': 5,
    'P': 5, 'Q': 5, 'R': 5, 'S': 5, 'T': 5, 'U': 5, 'V': 5, 'W': 5,
    'X': 5, 'Y': 5, 'Z': 5, '[': 3, '\\': 5, ']': 3, '^': 5, '_': 5,
    '`': 2, 'a': 5, 'b': 5, 'c': 5, 'd': 5, 'e': 5, 'f': 4, 'g': 5,
    'h': 5, 'i': 1, 'j': 5, 'k': 4, 'l': 2, 'm': 5, 'n': 5, 'o': 5,
    'p': 5, 'q': 5, 'r': 5, 's': 5, 't': 3, 'u': 5, 'v': 5, 'w': 5,
    'x': 5, 'y': 5, 'z': 5, '{': 3, '|': 1, '}': 3, '~': 6, '§': 5,
}

def split_line(line: str) -> list[str]:
    if not line or line.isspace():
        return ['']
    
    tokens = []
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]
        if ch.isalnum():
            start = i
            while i < n and line[i].isalnum():
                i += 1
            word = line[start:i]
            tokens.append(word)
        else:
            tokens.append(ch)
            i += 1

    lines = []
    curr_line = []
    curr_width = 0

    def calc_tok_width(tok: str):
        tok_width = 0
        for ch in tok:
            tok_width += char_widths[ch]
            if ch != ' ':  # Edge case for spaces
                tok_width += 1
        return tok_width

    for tok in tokens:
        tok_width = calc_tok_width(tok)

        if tok_width > 114:
            lines.append(''.join(curr_line).rstrip())
            curr_line.clear()
            curr_width = 0
            piece = ''
            for ch in tok:
                piece += ch
                if calc_tok_width(piece) > 114:
                    lines.append(piece[:-1])
                    piece = ch
            continue

        if curr_width + tok_width <= 114:
            curr_line.append(tok)
            curr_width += tok_width
        else:
            line_str = ''.join(curr_line).rstrip()
            lines.append(line_str)

            if tok == ' ':
                curr_line.clear()
                curr_width = 0
            else:
                curr_line = [tok]
                curr_width = tok_width

    if curr_line:
        line_str = ''.join(curr_line).rstrip()
        lines.append(line_str)

    return lines


def split_str(text: str) -> list[str]:
    return [l for line in text.split('\n') for l in split_line(line)]


def get_book_cmd(text: str, title: str, author: str) -> str:
    lines = split_str(text)
    for line in lines:
        print(line)
    lineno = 0
    accum = ''
    pages = []
    
    for line in lines:
        accum += line + '\n'
        lineno += 1
        
        if lineno == 14:
            page = repr(accum)
            
            accum = ''
            lineno = 0
            pages.append(page)
    
    if accum:
        page = repr(accum)
        pages.append(page)
    
    pages = '[' + ','.join(pages) + ']'
    return f'give @p written_book[written_book_content={{pages:{pages},title:"{title}",author:"{author}"}}]'


def main():
    parser = argparse.ArgumentParser(
        description='Convert ASCII text into a /give command that gives the player a written book, with the text automatically split into pages and lines'
    )
    parser.add_argument('input', help='Input file path')
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file path (default stdout)'
    )
    parser.add_argument(
        '-t', '--title',
        type=str,
        default='test',
        help='Title of the book (default test)'
    )
    parser.add_argument(
        '-a', '--author',
        type=str,
        default='test',
        help='Author of the book (default test)'
    )
    
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf8') as f:
        text = f.read()
    
    result = get_book_cmd(text, args.title, args.author)

    if args.output:
        with open(args.output, 'w', encoding='utf8') as f:
            f.write(result)
    else:
        print(result)

if __name__ == '__main__':
    main()
