words = [w.lower().strip() for w in open('/usr/share/dict/words').read().split() if w.strip()]

def is_word(w):
    return w in words

def combinations(left, so_far=''):
    if len(w) == 1: return [left]
    return combinations(w[1:], w[0]) + combinations(w[1:])

print combinations('abc')
