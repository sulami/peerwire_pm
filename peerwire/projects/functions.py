# coding: utf-8

import markdown

# Get the full project path in the project tree
def get_project_path(p, b=''):
    b = p.name + b
    if p.parent:
        b = '/' + b
        return get_project_path(p.parent, b)
    else:
        return b

# This function makes a list of lists, containing a projects object and some
# HTML-code for the tree-style display, using unicode and an unhealthy amount of
# values passed in loops.
def get_project_tree(p, padding, tree, c, initial):
    if p.project_set:
        tree.append([ [p, padding] ])
        if p.parent and initial > 1:
            if c != p.parent.project_set.all().count():
                padding = padding[:-1] + u'│'
            else:
                padding = padding[:-1] + '&nbsp;'
        count = 0
        for sub in p.project_set.all().order_by('-value'):
            count += 1
            if count == p.project_set.all().count():
                get_project_tree(sub, padding + u'└', tree, count, initial + 1)
            else:
                get_project_tree(sub, padding + u'├', tree, count, initial + 1)
    else:
        tree.append([ [p, padding] ])
        return tree
    return tree

def get_project_root(p, tree):
    if p.parent:
        tree.insert(0, p.parent)
        get_project_root(p.parent, tree)
    return tree

def markdown(text):
    return markdown.markdown(
        text,
        safe_mode='escape',
        output_format='html5',
        extensions=['codehilite(noclasses=true,pygments_style=friendly)']
        )


