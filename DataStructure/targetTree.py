import Pyro4

from DataStructure.targetNode import TargetNode


__author__ = 'Marouane'

Pyro4.config.REQUIRE_EXPOSE = True


@Pyro4.expose
class TargetTree(object):
    def __init__(self, makefile="", root_value=None):
        self.tree_root = None
        self.targets = {}
        self.first = True
        self.root = None
        self.files = {}

        for target in makefile:
            p = None

            if not self.targets.has_key(target.value):
                p = TargetNode(value=target.value, command=target.commands, parent=None, dependencies=[])
                self.targets.update({target.value: p})
            else:
                p = self.targets.get(target.value)
                p.exist = True
                p.set_command(target.commands)
                #p.dependencies = target.dependencies
                self.targets.update({target.value: p})

            if self.first:
                if not root_value:
                    self.tree_root = self.targets.get(target.value)
                    self.tree_root.exist = True
                    self.first = False
                else:
                    self.first = False

            for dependence in target.dependencies:
                d = None
                if not self.targets.has_key(dependence):
                    d = TargetNode(value=dependence, command='', parent=p, dependencies=[])
                    p.add_dependence(d)
                    self.targets.update({dependence: d})
                else:
                    d = self.targets.get(dependence)
                    p.add_dependence(d)

        if root_value:
            self.tree_root = self.targets.get(root_value)
            self.tree_root.exist = True
            self.first = False

        self.update_file_dependencies(self.tree_root)

        self.change_to_file_list()


    def print_dico(self):
        for key in self.targets:
            print("Node : " + key + "\n")
            obj = self.targets.get(key)
            print(obj.command)
            print("\n")
            if len(obj.dependencies) > 0:
                print("Dependencies : ")
                for val in obj.dependencies:
                    print(val.value + " ")
                print("\n")

    def change_tree_root(self, target):
        node = self.targets.get(target)
        if node:
            node.exist = True
            self.tree_root = node

    def update_file_dependencies(self, node):
        if len(node.dependencies) == 0:
            if not node.exist:
                # node.parent.add_file_dependence(node)
                return node
            else:
                return None
        else:
            for dep in node.dependencies:
                v = self.update_file_dependencies(dep)
                if v:
                    var = self.files.get(node.value)
                    if not var:
                        li = set()
                        li.add(v)
                        self.files.update({node.value: li})
                    else:
                        var.add(v)

    def change_to_file_list(self):
        for val in self.files.keys():
            li = self.files.get(val)
            node = self.targets.get(val)
            for elm in li:
                node.add_file_dependence(elm)
                node.remove_dependence(elm)


    def no_child_nodes(self):
        node_list = []
        self.recursive_no_child_nodes(self.tree_root, node_list)
        return node_list

    def recursive_no_child_nodes(self, node, node_list):
        if len(node.dependencies) == 0:
            if node.state == 0:
                node_list.append(node)
                node.state = 1
        else:
            for dep in node.dependencies:
                self.recursive_no_child_nodes(dep, node_list)

    def node_satisfied(self, node_name):
        node = self.targets.get(node_name)
        if node and node != self.tree_root:
            for dep in self.targets.values():
                try:
                    dep.dependencies.remove(node)
                except:
                    pass

    def recursive_print(self, node):
        if len(node.dependencies) == 0:
            if node.command:
                print(node.value)
        else:
            for dep in node.dependencies:
                self.recursive_print(dep)
            print(node.value)

    def recursive_print_v2(self, node):
        if len(node.dependencies) == 0:
            pass
        else:
            for dep in node.dependencies:
                self.recursive_print(dep)
            print(node.value)
            # print(node.dependencies)
            print(node.file_dependencies)

    def nodes_ns_register(self, daemon, ns):
        for target in self.targets.keys():
            node = self.targets.get(target)
            uri = daemon.register(node)
            ns.register(node.value, uri)

    def update_satisfaction(self, node):
        if len(node.dependencies) == 0:
            node.update_satisfaction()
        else:
            for dep in node.dependencies:
                self.update_satisfaction(dep)
            self.update_satisfaction(node)