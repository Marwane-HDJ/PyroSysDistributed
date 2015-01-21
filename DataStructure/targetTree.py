import Pyro4

from DataStructure.targetNode import TargetNode


__author__ = 'Marouane'

Pyro4.config.REQUIRE_EXPOSE = True


@Pyro4.expose
class TargetTree(object):
    def __init__(self, makefile):
        self.tree_root = None
        self.targets = {}
        self.first = True

        for target in makefile:
            p = None

            if not self.targets.has_key(target.value):
                p = TargetNode(target.value, target.commands, None, [])
                self.targets.update({target.value: p})
            else:
                p = self.targets.get(target.value)
                p.exist = True
                p.set_command(target.commands)
                self.targets.update({target.value: p})

            if self.first:
                self.tree_root = self.targets.get(target.value)
                self.tree_root.exist = True
                self.first = False

            for dependence in target.dependencies:
                d = None
                if not self.targets.has_key(dependence):
                    d = TargetNode(dependence, '', p, [])
                    p.add_dependence(d)
                    self.targets.update({dependence: d})
                else:
                    d = self.targets.get(dependence)
                    p.add_dependence(d)

        self.update_file_dependencies(self.tree_root)

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
                node.parent.add_file_dependence(node)
        else:
            for dep in node.dependencies:
                self.update_file_dependencies(dep)
                for fd in dep.file_dependencies:
                    dep.remove_dependence(fd)

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
            try:
                node.parent.dependencies.remove(node)
            except:
                pass

    def recursive_print(self, node):
        if len(node.dependencies) == 0:
            if len(node.command) != 0:
                print(node.value)
        else:
            for dep in node.dependencies:
                self.recursive_print(dep)
            print(node.command)

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

