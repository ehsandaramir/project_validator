

class GraphNode:
    all_reserved = ['namespace', 'class']
    all_modifiers = ['public', 'private', 'protected', 'static']
    all_primitives = ['int', 'long', 'string', 'void']

    def __init__(self, parent, signature: str, annotations=[]):
        self.cat = None
        self.children = []
        self.content = ['{']
        self.modifiers = []

        self.parent = parent
        self.signature = signature
        self.name = ''
        self.annotations = annotations

        self._evaluate_category()
        self._evaluate_name()
        self._evaluate_modifiers()

    def add_to_content(self, line):
        tmp = self
        while tmp is not None:
            tmp.content.append(line)
            tmp = tmp.parent

    def _evaluate_category(self):
        if self.parent is None:
            self.cat = 'namespace'
        else:
            if self.parent.cat == 'namespace':
                self.cat = 'class'
            if self.parent.cat == 'class':
                if self.signature.find('(') >= 0:
                    self.cat = 'method'
                else:
                    self.cat = 'property'

            if self.parent.cat == 'property':
                self.cat = 'getter/setter'
            if self.parent.cat == 'method':
                self.cat = 'in-method'

            if self.parent.cat == 'getter/setter':
                self.cat = 'getter/setter'
            if self.parent.cat == 'in-method':
                self.cat = 'in-method'

    def _evaluate_name(self):
        if self.cat == 'namespace':
            self.name = self.signature.split(' ')[1]

        if self.cat == 'class':
            tokens = [tok
                      for tok in self.signature.split(' ')
                      if (tok not in self.all_modifiers)
                      and (tok not in self.all_reserved)
                      ]
            self.name = tokens[0]

        if self.cat == 'method':
            tokens = [tok
                      for tok in self.signature.split(' ')
                      if (tok not in self.all_modifiers)
                      and (tok not in self.all_primitives)
                      and (tok not in self.all_reserved)
                      ]
            self.name = tokens[0].split('(')[0]

    def _evaluate_modifiers(self):
        for mod in GraphNode.all_modifiers:
            if self.signature.find(mod) >= 0:
                self.modifiers.append(mod)

    def __repr__(self):
        if len(self.children) > 0:
            return '{}({}) children: {}'.format(self.cat, self.name, self.children)
        else:
            return '{}({})'.format(self.cat, self.name)
