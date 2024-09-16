import os
from schedule_kspc.DirManager import Tree, Node

if __name__ == '__main__':
    # [1] Make folders by tree
    root_node = Node(name='root', path=os.getcwd())
    dir_manger = Tree(root_node=root_node)
    dir_manger.make_folders(node=root_node)

    # [2] Make folders by tree
    root_node2 = Node(name='root-2', path=os.getcwd())
    dir_manger2 = Tree(root_node=root_node2)
    dir_manger2.add_node(root=root_node2, name='child-1')
    dir_manger2.add_node(root=root_node2, name='child-2')
    dir_manger2.make_folders(node=root_node2)

    # [3] Make folders by tree
    root_node3 = Node(name='root-3', path=os.getcwd())
    dir_manger3 = Tree(root_node=root_node3)
    dir_manger3.add_node(root=root_node3, name='child-1')
    dir_manger3.root_node.children[0].add_child(name='child-1-1')
    dir_manger3.add_node(root=root_node3, name='child-2')
    dir_manger3.root_node.children[1].add_child(name='child-2-1')
    dir_manger3.make_folders(node=root_node3)

    # Show root nodes
    print(dir_manger.root_node)
    print(dir_manger2.root_node)
    print(dir_manger3.root_node)
