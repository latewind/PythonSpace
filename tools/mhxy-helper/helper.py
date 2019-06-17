import re
import win32gui
import win32con
from win32gui import *
import time
import autopy
from searchimg import search_img, sleep

from PIL import ImageGrab
from aip import AipOcr

from threading import Thread, Lock
from world_story import query_world_story

lock = Lock()

running = True
'''
任务窗口打开检测
'''
APP_ID = '16272528'
API_KEY = 'r2pTFSS81fsw2GouaUdZMTdY'
SECRET_KEY = 'XIkKfNpCjtLzzQ5KIdFxMkMFWWF5iicZ'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

titles = set()


def reset_point(func):
    def wrapper(*args):
        autopy.mouse.move(0, 0)
        time.sleep(2)
        func(*args)

    return wrapper


def adjust_point(point, x=50, y=50):
    return point[0] + x, point[1] + y


def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


def ocr_word(rect_area):
    ii = ImageGrab.grab(rect_area)
    ii.save('screen/ocr.bmp')
    image = get_file_content('screen/ocr.bmp')

    res = client.general(image)
    return res


def wait_finish():
    global running
    while running:
        time.sleep(5)
    print("finish")


class Helper:
    def __init__(self):
        self.simulator_name = '夜神模拟器'
        self.act_point = (353, 73)
        self.bag_point = (1239, 608)
        self.task_point = (1100, 178)
        self.task_exec_point = (975, 680)
        self.close_task_point = (1104, 83)
        self.normal_task_icon_path = "screen/normal_task.bmp"
        self.task_icon_path = "screen/map_act.bmp"
        self.world_story_act_icon = 'screen/world_story_act_icon.bmp'
        self.task_word = (440, 150, 1035, 250)
        EnumWindows(self.get_win_handler, 0)
        win_names = []
        for title in titles:
            if title:
                win_names.append(title)
        for title in win_names:
            if title.find(self.simulator_name) != -1:
                self.hwnd = win32gui.FindWindow(0, self.simulator_name)
                # win32gui.Set
                hwnd = win32gui.FindWindow(0, self.simulator_name)
                self.size = win32gui.GetWindowRect(hwnd)
                win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOP, 0, 0,
                                      self.size[2] - self.size[0],
                                      self.size[3] - self.size[1], win32con.SWP_SHOWWINDOW)
                # time.sleep(10)
        print(self.size)

    def ready(self):
        pass

    def hand_move(self):
        autopy.mouse.move(100, 100)
        autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
        autopy.mouse.smooth_move(100, 300)
        autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
        aim_point = search_img()
        self.move(aim_point)

    def drap(self, point, distance, down=True):
        autopy.mouse.move(*point)
        time.sleep(1)
        autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
        if down:
            autopy.mouse.smooth_move(point[0], point[1] - distance)
        else:
            autopy.mouse.smooth_move(point[0], point[1] + distance)
        autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)

    @staticmethod
    def point_move(point):
        autopy.mouse.move(*point)

    @staticmethod
    def move_and_click(point):
        time.sleep(1)
        autopy.mouse.move(*point)
        time.sleep(1)
        autopy.mouse.click()

    @staticmethod
    def move_and_click_quickly(point):
        autopy.mouse.move(*point)
        autopy.mouse.click()

    @staticmethod
    def click():
        autopy.mouse.click()

    @staticmethod
    def get_win_handler(hwnd, mouse):
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            titles.add(GetWindowText(hwnd))

    def get_task(self):
        ImageGrab.grab((1035, 218, 1270, 300)).save('D:\ceshi.jpg')

    @sleep(1)
    def open_bag(self):
        self.move_and_click(self.bag_point)

    @sleep(1)
    def open_act(self):
        # 打开活动界面
        self.move_and_click(self.act_point)

    @sleep(1)
    def close_act(self):
        # 关闭活动界面
        self.move_and_click((1137, 79))

    @sleep(2)
    def open_task(self):
        # 打开任务
        self.move_and_click(self.task_point)

    @sleep(1)
    def exec_task(self):
        self.move_and_click(self.task_exec_point)

    @sleep(1)
    def close_task(self):
        self.move_and_click(self.close_task_point)

    def close_task_quickly(self):
        self.move_and_click_quickly(self.close_task_point)

    def cancel_npc_chat(self):
        self.move_and_click((650, 683))
        self.click()

    def join_world_story(self):
        self.click_normal_task(self.world_story_act_icon)

    def join_map_task(self):
        self.click_normal_task(self.task_icon_path)

    def click_normal_task(self, icon_path):
        self.open_act()
        self.move_and_click((222, 157))
        aim_point = search_img(icon_path)
        if aim_point is None:
            self.close_act()
            return
        p = adjust_point(aim_point, 335, 10)
        self.move_and_click(p)


@staticmethod
def is_extend(point):
    x = point[0] + 115
    y = point[1]
    area = (x, y, x + 60, y + 70)
    p = search_img("screen/extended.bmp", area)
    return p is not None


def extend_normal_task(self):
    normal_task_point = search_img(self.normal_task_icon_path)
    if normal_task_point is not None:
        if self.is_extend(normal_task_point) is False:
            p = adjust_point(normal_task_point, 50, 50)
            self.move_and_click(p)
    return normal_task_point


def is_fighting():
    auto_fighting_point = search_img('screen/auto.bmp', (1187, 642, 1273, 735))
    return auto_fighting_point is not None


def is_not_fighting():
    return not is_fighting()


def waiting():
    time.sleep(5)
    return True


def is_shopping():
    shopping_point = search_img('screen/shopping.bmp', (580, 60, 700, 100))
    return shopping_point is not None


def is_buy_animal():
    shopping_point = search_img('screen/buy_animal.bmp', (580, 60, 710, 100))
    return shopping_point is not None


# 995 693

def buy():
    Helper.move_and_click((995, 693))
    return True


def close_shopping():
    Helper.move_and_click((1102, 101))
    return True


def submit_thing():
    submit_point = search_img('screen/submit.bmp', (930, 572, 1200, 651))
    if submit_point is None:
        return False
    p = adjust_point(submit_point, 50, 50)
    Helper.move_and_click(p)
    return True


def use_weapon_drawings():
    weapon_point = search_img('screen/use_weapon_drawings.bmp', (1015, 422, 1180, 650))
    if weapon_point is None:
        return False
    Helper.move_and_click((1100, 600))
    return True


def use_weapon_drawings_finish():
    weapon_point = search_img('screen/use_weapon_drawings.bmp', (1015, 422, 1180, 650))
    if weapon_point is None:
        return True
    return False


def is_animal_task_choose():
    p = search_img('screen/animal_task_choose.bmp', (485, 144, 795, 189))
    return p is not None


def submit_animal():
    return True


def open_act():
    Helper.move_and_click((353, 73))
    return True


def click_map_icon():
    map_icon_point = search_img('screen/map_act.bmp')
    if map_icon_point is not None:
        p = adjust_point(map_icon_point, 335, 10)
        Helper.move_and_click(p)
        return True
    return False


def close_act():
    # 关闭活动界面
    Helper.move_and_click((1137, 79))


def listen_map_task():
    listen_point = search_img('screen/listen.bmp')
    if listen_point is not None:
        p = adjust_point(listen_point, 50, 50)
        Helper.move_and_click(p)
        return True
    return False


# 送信收到
def visit_finish():
    res = ocr_word((440, 150, 1035, 250))
    print(res)
    if res['words_result_num'] > 0 and res['words_result'][0]['words'].find('信我已收到') > -1:
        return True
    return False


def close_dialog():
    Helper.move_and_click((592, 667))
    return True


# 三界奇缘问题
def ocr_world_story_question():
    res = ocr_word((530, 120, 1120, 155))
    if res['words_result_num'] > 0:
        question = res['words_result'][0]['words']
        print(question)
        return question


def ocr_world_story_answer():
    res = ocr_word((520, 390, 1156, 440))
    words_result = res['words_result']
    print(words_result)
    return words_result


# 使用地图
def use_map():
    map_point = search_img("screen/use_map.bmp")
    if map_point is not None:
        Helper.point_move((map_point[0] + 85, map_point[1] + 200))
        time.sleep(1)
        Helper.click()
        return True
    return False


def answer_world_story():
    question = ocr_world_story_question()
    answer = ocr_world_story_answer()

    # p = r'第(?P<index>\d)题:(?P<question_text>\w+)\?{0,1}\((?P<cur>\d)/(?P<total>\d)'
    p = r'第(?P<index>\d+)题:(?P<question_text>\w+)\?{0,1}'
    m = re.match(p, question)
    question_text = m.group('question_text')
    print(question_text)
    query_result = query_world_story(question_text)
    print(query_result.choices)
    choices = [choice.choice for choice in query_result.choices]
    print(choices)
    for words_result in answer:
        words = words_result['words']
        if words in choices:
            print(words)
            Helper.move_and_click((words_result['location']['left'] + 520, 390))
            break

class MapTask:
    def __init__(self):
        self.helper = Helper()
        self.act_point = (353, 73)
        self.task_icon_path = "screen/map_act.bmp"
        self.listen_path = "screen/listen.bmp"
        self.normal_task_icon_path = "screen/normal_task.bmp"
        self.map_task_list_path = "screen/map_task_list.bmp"
        # 是否做完
        self.done = False

    def accept_task(self):
        # 活动-日常活动
        self.helper.open_act()
        self.helper.move_and_click((222, 157))
        aim_point = search_img(self.task_icon_path)
        if aim_point is None:
            self.done = True
            self.helper.close_act()
            return

        p = adjust_point(aim_point, 335, 10)
        self.helper.move_and_click(p)

        # 接受任务（听听无妨）
        time.sleep(20)
        aim_point = search_img(self.listen_path)
        if aim_point is not None:
            p = adjust_point(aim_point, 50, 50)
            self.helper.move_and_click(p)
            self.helper.cancel_npc_chat()
            return
        time.sleep(2)
        self.helper.cancel_npc_chat()

    @sleep(2)
    def join(self):
        if self.done:
            return
        self.helper.open_task()
        self.helper.extend_normal_task()

        map_task_list_point = search_img(self.map_task_list_path)
        if map_task_list_point is None:
            return
        self.helper.move_and_click(adjust_point(map_task_list_point, 50, 50))
        self.helper.exec_task()
        self.helper.close_task()

        # 执行任务大约需要时间
        time.sleep(700)

    def exec(self):
        task_executor = AttackMapRobberStrategy(None)
        task_monitor = TaskMonitor(task_executor)
        task_monitor.start()


class FindMapTask(MapTask):

    def __init__(self):
        super(FindMapTask, self).__init__()
        pass

    def start_join(self):
        self.helper.open_bag()
        map_point = search_img("screen/map.bmp")
        i = 0
        while map_point is None and i < 5:
            self.helper.drap((908, 331), 88)
            time.sleep(2)
            map_point = search_img("screen/map.bmp")
            print(map_point)
            i = i + 1
        if map_point is None:
            return
        self.helper.point_move(map_point)
        self.helper.click()
        time.sleep(2)
        self.helper.point_move((507, 490))
        self.helper.click()

        task_executor = FindMapStrategy(None)
        t = TaskMonitor(task_executor)
        t.start()


class MasterTask(MapTask):

    def __init__(self):
        super(MasterTask, self).__init__()
        self.task_res = {}
        self.pattern = r'''(?P<task_type>\w+)\((?P<cur>\d+)/(?P<total>\d+)'''
        self.master_task_info_list = []
        self.current_exec_method = None

    def choose_master_task(self):
        self.helper.open_task()
        self.helper.extend_normal_task()
        p = search_img('screen/master_task_list.bmp')
        p = adjust_point(p, 50, 50)
        self.helper.move_and_click(p)

        res = ocr_word((440, 150, 1035, 250))
        self.task_res = res

    def test_ocr(self):
        res = ocr_word((440, 150, 1035, 250))
        self.task_res = res

    def parse_task(self):
        i = self.task_res['words_result_num']
        if i == 2:
            info = self.task_res['words_result'][0]['words']
            match_ret = re.search(self.pattern, info)
            cur = match_ret.group('cur')
            total = match_ret.group('total')
            task_type = match_ret.group('task_type')
            detail = self.task_res['words_result'][1]['words']
            master_task_info = MasterTaskInfo(task_type, cur, total, detail)
            self.master_task_info_list.append(master_task_info)

    def exec(self):
        if self.master_task_info_list is None:
            return
        master_task_executor = None
        master_task_info = self.master_task_info_list[-1]
        print(master_task_info)
        if master_task_info.task_type == "收集物品":
            master_task_executor = MasterTaskCollection(master_task_info)

        if master_task_info.task_type == "寻找物品":
            master_task_executor = MasterTaskFindThing(master_task_info)

        if master_task_info.task_type == "打造":
            master_task_executor = MasterTaskMakeWeapon(master_task_info)

        if master_task_info.task_type == "巡逻":
            master_task_executor = MasterTaskPatrol(master_task_info)

        if master_task_info.task_type == "送信":
            master_task_executor = MasterTaskVisitPerson(master_task_info)

        if master_task_info.task_type == "捕捉宠物":
            master_task_executor = MasterTaskCatchAnimal(master_task_info)

        # todo 执行
        self.helper.exec_task()

        self.helper.close_task_quickly()

        t = TaskMonitor(master_task_executor)
        t.start()


class TaskStrategy:
    def __init__(self, master_task_info):
        self.master_task_info = master_task_info
        self.steps = []
        self.have_thing_pattern = r'''(?P<have>\d+)/(?P<need>\d+)'''
        self._init_exec_method()

    def _init_exec_method(self):
        pass

    def next_step(self):
        if len(self.steps) == 0:
            return False
        step = self.steps[0]
        step_method = eval(step)
        if step_method():
            print(step)
            self.steps.pop(0)
        return True

    def have_thing(self):
        have_match = re.search(self.have_thing_pattern, self.master_task_info.detail)
        return have_match.group('have')


class MasterTaskFindThing(TaskStrategy):
    def __init__(self, master_task_info):
        super(MasterTaskFindThing, self).__init__(master_task_info)

    def _init_exec_method(self):
        if self.have_thing() == '1':
            self.steps = ['waiting', 'submit_animal']
        else:
            self.steps = ['waiting', 'is_shopping', 'buy', 'close_shopping', 'submit_thing']


class MasterTaskCollection(TaskStrategy):
    """
    收集
    """

    def __init__(self, master_task_info):
        super(MasterTaskCollection, self).__init__(master_task_info)

    def _init_exec_method(self):
        if self.master_task_info.detail.find("收集幽冥鬼草") != -1:
            self.steps = ['waiting', 'is_fighting', 'is_not_fighting']


class MasterTaskMakeWeapon(TaskStrategy):
    """
    打造
    """

    def __init__(self, master_task_info):
        super(MasterTaskMakeWeapon, self).__init__(master_task_info)

    def _init_exec_method(self):
        if self.master_task_info.detail.find("打造") != -1:
            self.steps = ['waiting', 'use_weapon_drawings', 'use_weapon_drawings_finish']


class MasterTaskPatrol(TaskStrategy):
    """
    巡逻
    """

    def __init__(self, master_task_info):
        super(MasterTaskPatrol, self).__init__(master_task_info)

    def _init_exec_method(self):
        if self.master_task_info.detail.find("巡逻") != -1:
            self.steps = ['waiting', 'is_fighting', 'is_not_fighting']


class MasterTaskVisitPerson(TaskStrategy):
    """
    送信
    """

    def __init__(self, master_task_info):
        super(MasterTaskVisitPerson, self).__init__(master_task_info)

    def _init_exec_method(self):
        if self.master_task_info.detail.find("送信") != -1:
            self.steps = ['waiting', 'visit_finish']


class MasterTaskCatchAnimal(TaskStrategy):
    """
    捕捉动物
    """

    def __init__(self, master_task_info):
        super(MasterTaskCatchAnimal, self).__init__(master_task_info)

    def _init_exec_method(self):
        print(self.master_task_info.detail)
        print(type(self.have_thing()))
        if self.have_thing() == '1':
            self.steps = ['waiting', 'is_animal_task_choose', 'submit_animal']
        else:
            self.steps = ['waiting', 'is_buy_animal', 'buy', 'is_animal_task_choose', 'submit_animal']


class AttackMapRobberStrategy(TaskStrategy):
    """
    打宝图强盗
    """

    def __init__(self, task_info):
        super(AttackMapRobberStrategy, self).__init__(task_info)

    def _init_exec_method(self):
        self.steps = ['open_act', 'click_map_icon',
                      'waiting', 'waiting', 'waiting', 'listen_map_task', 'close_dialog']


class FindMapStrategy(TaskStrategy):
    """
    找图策略
    """

    def __init__(self, task_info):
        super(FindMapStrategy, self).__init__(task_info)

    def _init_exec_method(self):
        self.steps = ['use_map'] * 10


class MasterTaskInfo:
    def __init__(self, task_type, cur, total, detail):
        self.task_type = task_type
        self.cur = cur
        self.total = total
        self.detail = detail


class TaskMonitor(Thread):
    def __init__(self, master_task_executor):
        Thread.__init__(self)
        self.master_task_executor = master_task_executor
        pass

    def run(self):
        global running
        while running:
            if not self.master_task_executor.next_step():
                running = False
                break
            time.sleep(5)
            print("running")
        print("running stop")


if __name__ == '__main__':
    # t = MapTask()
    # t.accept_task()
    # t.join()

    f = FindMapTask()
    f.start_join()

    # m = MasterTask()
    # m.test_ocr()
    # m.parse_task()
    # m.exec()
    # m.wait_finish()

    # t = MapTask()
    # t.exec()
    # wait_finish()
    # t.join()
    # help = Helper()
    # # help.join_map_task()
    # help.join_world_story()


