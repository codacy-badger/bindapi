import re

def multi_replace_regex(string, replacements, ignore_case=False):
    for pattern, repl in replacements.items():
        string = re.sub(pattern, repl, string, flags=re.I if ignore_case else 0)
    return string