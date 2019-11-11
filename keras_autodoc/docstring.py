import re

from . import utils


def process_list_block(docstring,
                       starting_point,
                       section_end,
                       marker):
    ending_point = docstring.find("\n\n", starting_point)
    block = docstring[
        starting_point: (ending_point - 1 if ending_point > -1 else section_end)
    ]
    # Place marker for later reinjection.
    docstring_slice = docstring[starting_point:section_end].replace(block, marker)
    docstring = (docstring[:starting_point]
                 + docstring_slice
                 + docstring[section_end:])
    lines = block.split("\n")
    # Usually lines have at least 4 additional leading spaces.
    # These have to be removed, but first the list roots have to be detected.
    top_level_regex = r"^    ([^\s\\\(]+):(.*)"
    top_level_replacement = r"- __\1__:\2"
    lines = [re.sub(top_level_regex, top_level_replacement, line) for line in lines]
    # All the other lines get simply the 4 leading space (if present) removed
    lines = [re.sub(r"^    ", "", line) for line in lines]
    # Fix text lines after lists
    indent = 0
    text_block = False
    for i in range(len(lines)):
        line = lines[i]
        spaces = re.search(r"\S", line)
        if spaces:
            # If it is a list element
            if line[spaces.start()] == "-":
                indent = spaces.start() + 1
                if text_block:
                    text_block = False
                    lines[i] = "\n" + line
            elif spaces.start() < indent:
                text_block = True
                indent = spaces.start()
                lines[i] = "\n" + line
        else:
            text_block = False
            indent = 0
    block = "\n".join(lines)
    return docstring, block


def deindent_code(list_of_lines):
    leading_spaces = None
    for line in list_of_lines:
        if not line or line[0] == "\n":
            continue
        spaces = utils.count_leading_spaces(line)
        if leading_spaces is None:
            leading_spaces = spaces
        if spaces < leading_spaces:
            leading_spaces = spaces
    if leading_spaces:
        return [line[leading_spaces:] for line in list_of_lines]
    else:
        return list_of_lines


def get_code_blocks(docstring):
    code_blocks = {}
    tmp = docstring[:]
    while "```" in tmp:
        tmp = tmp[tmp.find("```"):]
        index = tmp[3:].find("```") + 6
        snippet = tmp[:index]
        # Place marker in docstring for later reinjection.
        token = f'$KERAS_AUTODOC_CODE_BLOCK_{len(code_blocks)}'
        docstring = docstring.replace(snippet, token)
        snippet_lines = snippet.split("\n")
        # Remove leading spaces.
        num_leading_spaces = snippet_lines[-1].find("`")
        snippet_lines = [snippet_lines[0]] + [
            line[num_leading_spaces:] for line in snippet_lines[1:]
        ]
        # Most code snippets have 3 or 4 more leading spaces
        # on inner lines, but not all. Remove them.
        snippet_lines = ([snippet_lines[0]]
                         + deindent_code(snippet_lines[1:-1])
                         + [snippet_lines[-1]])
        snippet = "\n".join(snippet_lines)
        code_blocks[token] = snippet
        tmp = tmp[index:]

    return code_blocks, docstring


def get_sections(docstring):
    # Format docstring lists.
    section_regex = r"\n# (.*)\n"
    section_idx = re.search(section_regex, docstring)
    shift = 0
    sections = {}
    while section_idx and section_idx.group(1):
        anchor = section_idx.group(1)
        shift += section_idx.end()
        next_section_idx = re.search(section_regex, docstring[shift:])
        if next_section_idx is None:
            section_end = -1
        else:
            section_end = shift + next_section_idx.start()
        marker = "$" + anchor.replace(" ", "_") + "$"
        docstring, content = process_list_block(
            docstring, shift, section_end, marker
        )
        sections[marker] = content
        # `docstring` has changed, so we can't use `next_section_idx` anymore
        # we have to recompute it
        section_idx = re.search(section_regex, docstring[shift:])
    return sections, docstring


def process_docstring(docstring):
    # First, extract code blocks and process them.
    code_blocks, docstring = get_code_blocks(docstring)

    sections, docstring = get_sections(docstring)

    # Format docstring section titles.
    docstring = re.sub(r"\n(\s+)# (.*)\n", r"\n\1__\2__\n\n", docstring)

    # Strip all remaining leading spaces.
    lines = docstring.split("\n")
    docstring = "\n".join([line.lstrip(" ") for line in lines])

    # Reinject list blocks.
    for marker, content in sections.items():
        docstring = docstring.replace(marker, content)

    # Reinject code blocks.
    for token, code_block in code_blocks.items():
        docstring = docstring.replace(token, code_block)
    return docstring
