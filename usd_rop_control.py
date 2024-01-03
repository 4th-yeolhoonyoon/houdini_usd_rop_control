import hou


def create_node():
    root = hou.node('/stage/usd_extensions')
    children_node = root.children()

    rop_list = [c for c in children_node if c.type().name() == 'usd_rop' and c.inputConnections()]

    rop_node = rop_list.pop()
    output_path = rop_node.parm('lopoutput').eval()
    print(output_path)


def save_usd_file(rop_nodes):
    rop_nodes.pop()

    message = ('USD file with that version already exists. Do you want to overwrite? '
               '\n If you clicked \'No\' button, it sets a version number(+1)')
    dd = hou.ui.displayMessage(message, buttons=("Yes", "No", "Quit"))

    if dd == 0:
        print('hi')
    elif dd == 1:
        print('sorry')
    elif dd == 2:
        print('happy')


create_node()
