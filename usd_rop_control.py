import hou
import os
import re


class UsdRopControl:
    def __init__(self):
        self.root = None
        self.children_node = list
        self.output_path = str
        self.version_info = str
        self.last_version = int

    def check_rop_nodes(self):
        """
        /stage 경로 내에 usd_rop 노드를 찾도록 구현할 예정

        :return: list - list about usd rop nodes
        """
        # rop 노드 찾는 부분 더 넣어야 할듯
        self.root = hou.node('/stage/usd_extensions')
        self.children_node = self.root.children()
        rop_list = [c for c in self.children_node if c.type().name() == 'usd_rop' and c.inputConnections()]
        return rop_list

    def process_rop_nodes(self, rop_nodes):
        """
        USD 버전 체크,
        경로에 버전이 없을 경우에는 1로 시작할 건지, 창을 닫을 건지 선택하도록
        경로에 버전이 있는 경우에는 이미 파일이 있으면 덮어쓸 건지, 버전 업을 할 건지 선택하도록

        :param rop_nodes: list

        """
        if len(rop_nodes) == 0:
            print('There is no USD rop node')
            return

        rop_node = rop_nodes.pop()
        self.output_path = rop_node.parm('lopoutput').eval()
        self.dirname = os.path.dirname(self.output_path)
        self.basename = os.path.basename(self.output_path)
        # 여기서 정규표현식을 사용하면, rop_node를 리스트 형식으로 받으면 안될 거 같다
        self.version_info = re.search("v\d\d\d", self.basename)

        if self.version_info:
            # 버전 중복 체크 및 버전 업할 건지 확인하는 메소드
            if os.path.isfile(self.output_path):
                message = (f'{rop_node}'
                           f'\n {self.output_path} \n'
                           '\n USD file with that version already exists. Do you want to overwrite? '
                           '\n If you clicked \'No\' button, it sets a last version +1')
                hou.ui.setStatusMessage("Select one root Alembic Archive node.")
                message_box = hou.ui.displayMessage(message, buttons=("Yes", "No", "Quit"))
                if message_box == 0:
                    rop_node.parm('execute').pressButton()
                elif message_box == 1:
                    rop_node.parm('lopoutput').set(self.set_version_up_usd())
                    rop_node.parm('execute').pressButton()
                elif message_box == 2:
                    pass
            else:
                # 최신 버전이 3인데 4로 저장하려고 할 경우에 제어가 필요할 것인가.
                message = (f'{rop_node}'
                           f'\n {self.output_path} \n'
                           'Last version is {last version info - add code}, Are you okay?')
                message_box = hou.ui.displayMessage(message, buttons=("Yes", "No", "Quit"))
                if message_box == 0:
                    rop_node.parm('execute').pressButton()
                elif message_box == 1:
                    rop_node.parm('lopoutput').set(self.set_version_up_usd())
                    rop_node.parm('execute').pressButton()
                elif message_box == 2:
                    pass
        else:
            # 에러 체크 함수 버전을 추가하는 방식 or 버전 1로 만들기
            message = (f'{rop_node}'
                       f'\n {self.output_path} \n'
                       '\n There is no version in path, Do you want to create new version?'
                       '\n If you don\'t want, add USD file version')
            message_box = hou.ui.displayMessage(message, buttons=("Yes", "Quit"))
            if message_box == 0:
                self.set_new_usd()
            elif message_box == 1:
                pass
        # 결과체크
        self.result_check()
        self.process_rop_nodes(rop_nodes)

    def set_version_up_usd(self):
        """
        중복되면 해당 버전보다 +1 해서 path를 리턴한다
        버전 업을 한 파일도 존재하면 가장 최신 버전 다음 버전 경로로 리턴한다.
        :return: next_path
        """
        print('export_version_up_usd method')
        version_num = self.version_info.group()[1:]
        next_verion = int(version_num) + 1
        filename, usd_extension = self.basename.split('.')
        version_padding = str(next_verion).rjust(3, '0')
        filename_v = filename.split(version_num)[0]
        update_filename = filename_v + version_padding + ('.' + usd_extension)
        next_path = os.path.join(self.dirname, update_filename)
        if os.path.isfile(next_path):
            version_padding = str(self.get_last_version_usd(filename_v)).rjust(3, '0')
            update_filename = filename.split(version_num)[0] + version_padding + ('.' + usd_extension)
            next_path = os.path.join(self.dirname, update_filename)

        print('next_path :', next_path)
        return next_path

    def set_new_usd(self):
        """
        version 1 로 첫 export 해주는 메소드

        :return:
        """
        print('export_new_usd method')

    def get_last_version_usd(self, start_name):
        """

        :param start_name: str
        :return:
        """
        filename, usd_extension = self.basename.split('.')
        files = os.listdir(self.dirname)
        file_list = [re.search("v\d\d\d", file).group() for file in files if file.startswith(start_name)]
        self.last_version = int(sorted(file_list).pop()[1:]) + 1
        last_ver = self.last_version
        return last_ver

    def result_check(self):
        '''
        결과 한번 더 체크해주는 메소드
        :return:
        '''
        print('result check')


rop = UsdRopControl()
node_list = rop.check_rop_nodes()
rop.process_rop_nodes(node_list)
