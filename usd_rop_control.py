import hou
import os
import re


def create_node():
    root = hou.node('/stage/usd_extensions')
    children_node = root.children()

    rop_list = [c for c in children_node if c.type().name() == 'usd_rop' and c.inputConnections()]

    rop_node = rop_list.pop()
    output_path = rop_node.parm('lopoutput').eval()
    dirname = os.path.dirname(output_path)
    basename = os.path.basename(output_path)
    print(dirname)
    print(basename)

    p = re.compile("v\d\d\d")
    m = p.search(basename)
    if m:
        # 버전 중복 체크 및 버전 업할 건지 확인하는 메소드
        pass
    else:
        # 에러 체크 함수 버전을 추가하라는 방식 or version 1로 만들기
        pass


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
