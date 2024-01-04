import hou
import os
import re


class UsdRopControl:
    def __init__(self):
        self.root = None
        self.children_node = None
        self.output_path = None

    def check_rop_nodes(self):
        '''
        /stage 경로 내에 usd_rop 노드를 찾도록 구현할 예정

        :return: list - list about usd rop nodes
        '''
        # rop 노드 찾는 부분 더 넣어야 할듯
        self.root = hou.node('/stage/usd_extensions')
        self.children_node = self.root.children()
        rop_list = [c for c in self.children_node if c.type().name() == 'usd_rop' and c.inputConnections()]
        return rop_list

    def process_rop_nodes(self, rop_nodes):
        '''
        USD 버전 체크,
        경로에 버전이 없을 경우에는 1로 시작할 건지, 창을 닫을 건지 선택하도록
        경로에 버전이 있는 경우에는 이미 파일이 있으면 덮어쓸 건지, 버전 업을 할 건지 선택하도록

        :param rop_nodes: list

        '''
        if len(rop_nodes) == 0:
            print('There is no USD rop node')
            return

        rop_node = rop_nodes.pop()
        self.output_path = rop_node.parm('lopoutput').eval()
        dirname = os.path.dirname(self.output_path)
        basename = os.path.basename(self.output_path)
        # 여기서 정규표현식을 사용하면, rop_node를 리스트 형식으로 받으면 안될 거 같다
        m = re.search("v\d\d\d", basename)

        if m:
            print(m.group())
            # 버전 중복 체크 및 버전 업할 건지 확인하는 메소드
            message = (f'{rop_node}'
                       f'\n {self.output_path} \n'
                       '\n USD file with that version already exists. Do you want to overwrite? '
                       '\n If you clicked \'No\' button, it sets a version number(+1)')
            dd = hou.ui.displayMessage(message, buttons=("Yes", "No", "Quit"))
            if dd == 0:
                self.export_overwrite_usd()
            elif dd == 1:
                self.export_version_up_usd()
            elif dd == 2:
                pass
            self.process_rop_nodes(rop_nodes)

        else:
            # 에러 체크 함수 버전을 추가하는 방식 or 버전 1로 만들기
            message = (f'{rop_node}'
                       f'\n {self.output_path} \n'
                       '\n There is no version in path, Do you want to create new version?'
                       '\n If you don\'t want, add USD file version')
            bb = hou.ui.displayMessage(message, buttons=("Yes", "Quit"))
            if bb == 0:
                self.export_new_usd()
            elif bb == 1:
                pass
            self.process_rop_nodes(rop_nodes)

    def export_version_up_usd(self):
        print('export_version_up_usd method')

    def export_overwrite_usd(self):
        print('export_overwrite_usd method')

    def export_new_usd(self):
        print('export_new_usd method')


rop = UsdRopControl()
node_list = rop.check_rop_nodes()
rop.process_rop_nodes(node_list)
