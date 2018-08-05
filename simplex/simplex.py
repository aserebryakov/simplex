# MIT License
#
# Copyright (c) 2018 Alexander Serebryakov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import collections
import re

Token = collections.namedtuple('Token', ['kind', 'value', 'line', 'column'])
TokenSpecification = collections.namedtuple('TokenSpecification', ['kind', 'regex', 'handler'])

class Tokenizer:
    def __init__(self, state=None):
        self.token_specification = []
        self.keywords = set()
        self.state = state

    def add_token(self, kind, regex, handler):
        self.token_specification.append(TokenSpecification(kind, regex, handler))

    def add_keyword(self, keyword):
        self.keywords.add(keyword)

    def handle_token(self, match_object):
        kind = match_object.lastgroup
        value = match_object.group(kind)

        for spec in self.token_specification:
            if spec.kind == kind:
                return spec.handler(match_object, kind, value, self.keywords, self.state)

        raise RuntimeError('Unexpected kind {}'.format(kind))

    def tokenize(self, code):
        tok_regex = '|'.join('(?P<{}>{})'.format(spec.kind, spec.regex)
                             for spec in self.token_specification)

        for mo in re.finditer(tok_regex, code):
            result = self.handle_token(mo)
            if result:
                yield result
