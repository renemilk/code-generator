#!/usr/bin/python
# vim: set fileencoding=utf-8
import pprint
import sys
import os
import clang.cindex
from clang.cindex import StorageClass

import itertools
from jinja2 import Template


class Function(object):
    def __init__(self, cursor):
        self.name = cursor.spelling
        self.access = cursor.access_specifier
        self.parameters = [cursor.get_template_argument_type(i) for i in range(cursor.get_num_template_arguments())] + list(cursor.get_arguments())
        parameter_dec = [c for c in cursor.get_children() if c.kind == clang.cindex.CursorKind.PARM_DECL]
        self.parameters = [p.spelling or p.displayname for p in parameter_dec]
        self.declaration = ''
        for token in cursor.translation_unit.get_tokens(extent=cursor.extent):
            if '{' in token.spelling:
                break
            self.declaration += ' '+token.spelling


class Class(object):
    def __init__(self, cursor):
        self.name = cursor.spelling
        self.functions = []

        for c in cursor.get_children():
            if c.access_specifier != clang.cindex.AccessSpecifier.PUBLIC:
                continue
            if (c.kind == clang.cindex.CursorKind.CXX_METHOD) or \
                    (c.kind == clang.cindex.CursorKind.FUNCTION_TEMPLATE):
                self.functions.append(Function(c))


def build_classes(cursor):
    result = []
    for c in cursor.get_children():
        if (c.kind == clang.cindex.CursorKind.CLASS_DECL
            and c.location.file.name == sys.argv[1]):
            a_class = Class(c)
            result.append(a_class)
        elif c.kind == clang.cindex.CursorKind.NAMESPACE:
            child_classes = build_classes(c)
            result.extend(child_classes)

    return result


if len(sys.argv) != 2:
    print("Usage: boost_python_gen.py [header file name]")
    sys.exit()

clang.cindex.Config.set_library_file('/usr/lib/x86_64-linux-gnu/libclang-4.0.so.1')
index = clang.cindex.Index.create()
translation_unit = index.parse(sys.argv[1], ['-x', 'c++', '-std=c++11', '-D__CODE_GENERATOR__'])

classes = build_classes(translation_unit.cursor)
tpl = Template(open('wrapped.jinja', 'rt').read())
rendered = tpl.render(
             classes=classes,
             include_file=sys.argv[1])

OUTPUT_DIR = 'generated'

if not os.path.isdir(OUTPUT_DIR): os.mkdir(OUTPUT_DIR)

with open("generated/{}.bind.cc".format(sys.argv[1]), "w") as f:
    f.write(rendered)
    print(rendered)
