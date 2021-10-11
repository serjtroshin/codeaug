from tree_sitter import Language, Parser, Tree


def traverse_tree(tree: Tree):
    cursor = tree.walk()

    reached_root = False
    while reached_root == False:
        yield cursor.node

        if cursor.goto_first_child():
            continue

        if cursor.goto_next_sibling():
            continue

        retracing = True
        while retracing:
            if not cursor.goto_parent():
                retracing = False
                reached_root = True

            if cursor.goto_next_sibling():
                retracing = False


class TreeSitterCode:
    """
    stores 1) the source code in bytes
           2) the tree
        allows to traverse nodes in the AST tree, replace values.
        updates both with `replace` method
        (tool to change identifiers)
    """
    def __init__(self, code: str, parser: Parser):
        self.code_bytes = bytes(
            code, "utf-8"
        )
        self.parser = parser
        self.tree = self.parser.parse(self.code_bytes)
        
    @property
    def code(self):
        return self.code_bytes.decode()
    
    def traverse(self):
        for item in traverse_tree(self.tree):
            yield item
            
    def identifiers(self):
        def is_identifier(node): return node.type=='identifier'
        for node in self.traverse():
            if is_identifier(node):
                yield node
                
    def get_value(self, node):
        return self.code_bytes[node.start_byte: node.end_byte]
    
    def inspect(self):
        print("="*80)
        for it in code_tree.traverse():
            print(it.type, '\t', code_tree.get_value(it), '\t', it.start_point, '\t', it.end_point, '\t', it.start_byte, '\t', it.end_byte)
            
    def replace(self, node: Tree, new_value: bytes):
        assert not b'\n' in new_value
        start_byte_old, end_byte_old = node.start_byte, node.end_byte
        length = len(new_value)
        self.code_bytes = self.code_bytes[:node.start_byte] + \
                new_value + \
                self.code_bytes[node.end_byte:]
        assert node.end_point[0] == node.start_point[0], "we should edit one line"
        # print(start_byte_old, end_byte_old, start_byte_old + length, node.start_point, node.end_point, (node.start_point[0], node.start_point[1] + length))
        self.tree.edit(
            start_byte=start_byte_old,
            old_end_byte=end_byte_old,
            new_end_byte=start_byte_old + length,
            start_point=node.start_point,
            old_end_point=node.end_point,
            new_end_point=(node.start_point[0], node.start_point[1] + length),
        )
        self.tree = self.parser.parse(self.code_bytes, self.tree)
        # self.tree = self.parser.parse(self.code_bytes)


if __name__=="__main__":
    code_example ="""
    my_file = "input.txt"
    with open(my_file, "r") as f:
        print(f.readlines())
    """
    parser = Parser()
    parser.set_language(PY_LANGUAGE)
    code_tree = TreeSitterCode(code_example, parser)

    print("<No bug>")
    print(colored(code_tree.code))

    for identifier in code_tree.identifiers():
        value = code_tree.get_value(identifier)
        if value == b'f':
            code_tree.replace(identifier, b'my_file') # insert bug
            break

    print("<With bug>")
    print(colored(code_tree.code))
            
    # code_tree.inspect()
        
    for identifier in code_tree.identifiers():
        value = code_tree.get_value(identifier)
        if value == b'f':
            code_tree.replace(identifier, b'my_file') # insert bug
            break
            
    print("<With second bug>")
    print(colored(code_tree.code))

    # code_tree.inspect()

