import hou
import os
import re


def check_rop_node():
    '''

    :return:
    '''
    # rop 노드 찾는 부분 더 넣어야 할듯
    root = hou.node('/stage/usd_extensions')
    children_node = root.children()
    rop_list = [c for c in children_node if c.type().name() == 'usd_rop' and c.inputConnections()]
    return rop_list


def process_rop_nodes(rop_nodes):
    '''

    :param rop_nodes: list
    :return:
    '''
    if len(rop_nodes) == 0:
        print('There is no USD rop node')
        return

    rop_node = rop_nodes.pop()
    output_path = rop_node.parm('lopoutput').eval()
    dirname = os.path.dirname(output_path)
    basename = os.path.basename(output_path)
    print(dirname)
    print(basename)

    # 여기서 정규표현식을 사용하면, rop_node를 리스트 형식으로 받으면 안될 거 같다
    p = re.compile("v\d\d\d")
    m = p.search(basename)

    if m:
        # 버전 중복 체크 및 버전 업할 건지 확인하는 메소드
        message = ('USD file with that version already exists. Do you want to overwrite? '
                   '\n If you clicked \'No\' button, it sets a version number(+1)')

        dd = hou.ui.displayMessage(message, buttons=("Yes", "No", "Quit"))

        if dd == 0:
            print('hi')
        elif dd == 1:
            print('sorry')
        elif dd == 2:
            print('happy')

        process_rop_nodes(rop_nodes)

    else:
        # 에러 체크 함수 버전을 추가하는 방식 or 버전 1로 만들기
        message = ('There is no version in path, Do you want to create new version?'
                   '\n If you don\'t want, add USD file version')

        bb = hou.ui.displayMessage(message, buttons=("Yes", "Quit"))

        if bb == 0:
            print('hello')
        elif bb == 1:
            print('end')

        process_rop_nodes(rop_nodes)


rop = check_rop_node()
print(rop)
process_rop_nodes(rop)
