import random
import string

def test(s):
    v = re.match("<SELECT.*>", s)
    print("%s  %s %d" % (('+' if v else '.'),  s, len(s)))
    return v


def remove_check_each_fragment(instr, part_len, causal):
    pre = ''
    for i in range(0, len(instr), part_len):
        stitched =  pre + instr[i+part_len:]
        if not causal(stitched):
             pre = pre + instr[i:i+part_len]
    return pre

def ddrmin(cur_str, causal_fn, pre='', post=''):
    if len(cur_str) == 1: return cur_str

    part_i = len(cur_str) // 2
    string1, string2 = cur_str[:part_i], cur_str[part_i:]
    if causal_fn(pre + string1 + post):
        return ddrmin(string1, causal_fn, pre, post)
    elif causal_fn(pre + string2 + post):
        return ddrmin(string2, causal_fn, pre, post)
    s1 = ddrmin(string1, causal_fn, pre, string2 + post)
    s2 = ddrmin(string2, causal_fn, pre + s1, post)
    return s1 + s2


def test(s):
    print("%s %d" % (s, len(s)))
    return set('()') <= set(s)

inputstring = ''.join(random.choices(string.digits +
                      string.ascii_letters +
                      string.punctuation, k=1024))
print(inputstring)

assert test(inputstring)
solution = ddrmin(inputstring, test)
print(solution)