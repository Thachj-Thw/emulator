from __future__ import annotations
from typing import Union, Optional
import subprocess
from .option import EmulatorOptions
from .args import subprocess_args
from .opencv import get_pos_img
from .node import Node, By
import time
import os
import base64
import ctypes
import re

# type
position = Union[list[int, int], tuple[int, int]]


class ObjectEmulator:
    sed = os.path.join(os.path.dirname(__file__), "sed", "sed.exe")

    def __init__(
        self,
        parent,
        index: int,
        name: str,
        top_hwnd: int = 0,
        bind_hwnd: int = 0,
        android: int = 0,
        pid: int = -1,
        pid_vbox: int = -1
    ) -> None:
        self._parent = parent
        self._controller = parent.controller
        self._index = index
        self._name = name
        self._top_hwnd = top_hwnd
        self._bind_hwnd = bind_hwnd
        self._android = android
        self._pid = pid
        self._pid_vbox = pid_vbox
        self._this = "--index " + str(self._index)
        self._error = ""
        self._dump = os.path.join(os.path.normpath(os.path.dirname(__file__)), "dump", str(self._index) + ".xml")

    @property
    def parent(self):
        return self.parent

    @property
    def index(self):
        return self._index

    @property
    def name(self):
        return self._name

    @property
    def top_hwnd(self):
        return self._top_hwnd

    @property
    def bind_hwnd(self):
        return self._bind_hwnd

    @property
    def pid(self):
        return self._pid

    @property
    def pid_vbox(self):
        return self._pid_vbox

    @property
    def error(self):
        return self._error

    def start(self, wait: bool = True):
        if not self.is_running():
            self._run_cmd(f'{self._controller} launch {self._this}')
            if wait:
                self.wait_to_started()
                self._update()
            else:
                while not self._update():
                    time.sleep(.5)
        else:
            self._update()
        return self

    def _update(self) -> bool:
        cmd = f'{self._controller} list2 | "{self.sed}" -n "/^{self._index},/p"'
        args = self._run_cmd(cmd).split("\r\n")[0].split(",")
        if args[2] != "0":
            self._top_hwnd = int(args[2])
            self._bind_hwnd = int(args[3])
            self._android = int(args[4])
            self._pid = int(args[5])
            self._pid_vbox = int(args[6])
            return True
        return False

    def wait_to_started(self, timeout: float = 60):
        timer = time.perf_counter()
        while (timeout == 0 or time.perf_counter() - timer < timeout) and not self.adb_connected():
            time.sleep(1)
        return self

    def is_running(self) -> bool:
        cmd = f'{self._controller} isrunning {self._this}'
        return self._run_cmd(cmd) == "running"

    def restart(self, wait: bool = True):
        if self.is_running():
            cmd = f'{self._controller} reboot {self._this}'
            self._run_cmd(cmd)
            if wait:
                self.wait_to_started()
            else:
                time.sleep(3)
            self._update()
            self._error = ""
        else:
            self._error = "emulator is not running"
        return self

    def rename(self, new_name: str):
        cmd = f'{self._controller} rename {self._this} --title "{new_name}"'
        self._error = self._run_cmd(cmd)
        if not self._error:
            self._name = new_name
        return self

    def install_app(self, source: str):
        if self.is_running():
            path = os.path.normpath(source)
            if os.path.isfile(path):
                cmd = f'{self._controller} installapp {self._this} --filename "{path}"'
            else:
                cmd = f'{self._controller} installapp {self._this} --packagename "{source}"'
            self._error = self._run_cmd(cmd)
        else:
            self._error = "The emulator is not started!"
        return self

    def uninstall_app(self, package_name: str):
        if self.is_running():
            cmd = f'{self._controller} uninstallapp {self._this} --packagename "{package_name}"'
            self._error = self._run_cmd(cmd)
        else:
            self._error = "The emulator is not started!"
        return self

    def run_app(self, package_name: str):
        if self.is_running():
            cmd = f'{self._controller} runapp {self._this} --packagename "{package_name}"'
            self._error = self._run_cmd(cmd)
        else:
            self._error = "The emulator is not started!"
        return self

    def kill_app(self, package_name: str):
        if self.is_running():
            cmd = f'{self._controller} killapp {self._this} --packagename "{package_name}"'
            self._error = self._run_cmd(cmd)
        else:
            self._error = "The emulator is not started!"
        return self

    def clear_app(self, package_name: str):
        cmd = f'shell pm clear "{package_name}"'
        self._error = self._run_adb(cmd)
        return self

    def list_packages(self) -> Optional[list]:
        cmd = f"shell pm list packages | sed 's/^package://'"
        return [package for package in self._run_adb(cmd).split("\r\r\n")[:-1]]

    def set_locate(self, locate: str):
        if self.is_running():
            cmd = f'{self._controller} locate {self._this} --LLI "{locate}"'
            self._error = self._run_cmd(cmd)
        else:
            self._error = "The emulator is not started!"
        return self

    def update_properties(self, prop: dict):
        for key in prop.keys():
            cmd = f'{self._controller} setprop {self._this} --key "{key}" --value "{prop[key]}"'
            self._error = self._run_cmd(cmd)
            if self._error:
                break
        return self

    def get_properties(self) -> dict:
        cmd = f"shell getprop | sed 's/[][]//g'"
        lst = self._run_adb(cmd).split("\r\r\n")[:-1]
        return {key: value for key, value in [x.split(": ") for x in lst]}

    def down_cpu(self, rate: int):
        if rate < 0:
            rate = 0
        if rate > 100:
            rate = 100
        cmd = f'{self._controller} downcpu {self._this} --rate {int(rate)}'
        self._error = self._run_cmd(cmd)
        return self

    def backup(self, file_path: str):
        path = os.path.normpath(file_path)
        cmd = f'{self._controller} backup {self._this} --file "{path}"'
        self._error = self._run_cmd(cmd)
        return self

    def restore(self, file_path: str):
        path = os.path.normpath(file_path)
        if os.path.isfile(path):
            cmd = f'{self._controller} restore {self._this} --file "{path}"'
            self._error = self._run_cmd(cmd)
        else:
            self._error = f'Path "{file_path}" invalid!'
        return self

    def action(self, actions: dict):
        for key in actions.keys():
            cmd = f'{self._controller} action {self._this} --key "{key}" --value "{actions[key]}"'
            self._error = self._run_cmd(cmd)
            if self._error:
                break
        return self

    def scan(self, file_path: str):
        if self.is_running():
            path = os.path.normpath(file_path)
            if os.path.isfile(path):
                cmd = f'{self._controller} scan {self._this} --file "{path}"'
                self._error = self._run_cmd(cmd)
            else:
                self._error = f'Path "{file_path}" invalid!'
        else:
            self._error = "emulator is not running"
        return self

    def pull(self, remote: str, local: str):
        lo_path = os.path.normpath(local)
        cmd = f'pull "{remote}" "{lo_path}"'
        out = self._run_adb(cmd)
        if "bytes" not in out:
            self._error = out
        else:
            self._error = ""
        return self

    def push(self, local: str, remote: str):
        lo_path = os.path.normpath(local)
        cmd = f'push "{lo_path}" "{remote}"'
        out = self._run_adb(cmd)
        if "bytes" not in out:
            self._error = out
        else:
            self._error = ""
        return self

    def capture(self, as_file):
        path = os.path.normpath(as_file)
        b_img = self._get_screencap_b64decode()
        if b_img:
            with open(path, mode="wb") as file:
                file.write(b_img)
            self._error = ""
        return self

    def quit(self) -> None:
        cmd = f'{self._controller} quit {self._this}'
        self._run_cmd(cmd)

    def setting(self, options: EmulatorOptions):
        opts = " ".join([f"{key} {options.options[key]}" for key in options.options.keys()])
        if opts:
            cmd = f'{self._controller} modify {self._this} {opts}'
            self._error = self._run_cmd(cmd)
        return self

    def adb_connected(self) -> bool:
        return "connected\r\r\n" == self._run_adb('shell echo "connected"')

    def tap(self, *pos: position):
        for p in pos:
            cmd = f'shell input tap {p[0]} {p[1]}'
            self._error = self._run_adb(cmd)
        return self

    def swipe(self, _from: position, to: position, duration: int = 100):
        cmd = f'shell input swipe {_from[0]} {_from[1]} {to[0]} {to[1]} {duration}'
        self._error = self._run_adb(cmd)
        return self

    def send_text(self, text: str):
        cmd = f'shell input text "{text.replace(" ", r"%s")}"'
        self._error = self._run_adb(cmd)
        return self

    def send_event(self, keycode: int):
        cmd = f'shell input keyevent {keycode}'
        self._error = self._run_adb(cmd)
        return self

    def home(self):
        return self.send_event(3)

    def back(self):
        return self.send_event(4)

    def app_switcher(self):
        return self.send_event(187)

    def tap_to_img(self, img_path: str, timeout: float = 0, threshold: float = 0.8):
        self._error = ""
        path = os.path.normpath(img_path)
        if os.path.isfile(path):
            if timeout == 0:
                screen = self._get_screencap_b64decode()
                if not screen:
                    return self
                pos = get_pos_img(path, screen, threshold=threshold)
            else:
                pos = self._wait_img_and_get_pos(path, 0 if timeout < 0 else timeout, threshold, False)
            if pos:
                self.tap(pos[0])
            else:
                self._error = "image not in screen"
        else:
            self._error = f'The path "{img_path}" invalid!'
        return self

    def tap_to_imgs(self, img_path: str, timeout: float = 0, threshold: float = 0.8):
        self._error = ""
        path = os.path.normpath(img_path)
        if os.path.isfile(path):
            if timeout == 0:
                screen = self._get_screencap_b64decode()
                if not screen:
                    return self
                pos = get_pos_img(path, screen, multi=True, threshold=threshold)
            else:
                pos = self._wait_img_and_get_pos(path, 0 if timeout < 0 else timeout, threshold, True)
            if pos:
                self.tap(*pos)
            else:
                self._error = "image not in screen"
        else:
            self._error = f'The path "{img_path}" invalid!'
        return self

    def wait_img_existed(self, img_path: str, timeout: float = 0, threshold: float = 0.8):
        self._error = ""
        path = os.path.normpath(img_path)
        if os.path.isfile(path):
            self._wait_img_and_get_pos(path, timeout, threshold, False)
        else:
            self._error = f'The path "{img_path}" invalid'
        return self

    def _get_screencap_b64decode(self) -> Optional[bytes]:
        if self.adb_connected:
            out = self._run_cmd(f'{self._controller} adb {self._this} --command "shell screencap -p | base64"')
            try:
                return base64.b64decode(out.replace("\r\r\n", "\n"))
            except Exception:
                print("output capture error:", out)
                return
        self._error = "adb is not connected"

    def _wait_img_and_get_pos(self, img_path: str, timeout: float, threshold: float, multi: bool):
        screen = self._get_screencap_b64decode()
        if screen:
            timer = time.perf_counter()
            pos = get_pos_img(obj=img_path, _in=screen, threshold=threshold, multi=multi)
            while not pos:
                screen = self._get_screencap_b64decode()
                if not screen:
                    return
                pos = get_pos_img(obj=img_path, _in=screen, threshold=threshold, multi=multi)
                if timeout != 0 and time.perf_counter() - timer > timeout:
                    self._error = "Timeout"
                    return
            return pos

    def dump_xml(self, as_file: str):
        path = os.path.normpath(as_file)
        cmd = 'shell uiautomator dump /sdcard/window_dump.xml'
        self._run_adb(cmd)
        self.pull("/sdcard/window_dump.xml", path)
        return self

    def find_node(self, by: int, value: str) -> Optional[Node]:
        self.dump_xml(self._dump)
        if self._error:
            return
        with open(self._dump, mode="r", encoding="utf-8") as file:
            xml = file.read()
        if by == By.TEXT:
            node = re.search(r'(?<=<node )index="\d+" text="%s".*?(?=/>|>)' % value, xml)
            if node:
                return self._create_node(node.group())
        elif by == By.RESOURCE_ID:
            node = re.search(r'(?<=<node )index="\d+" text=".*" resource-id="%s".*?(?=/>|>)' % value, xml)
            if node:
                return self._create_node(node.group())
        elif by == By.CLASS:
            node = re.search(r'(?<=<node )index="\d+" text=".*" resource-id=".*" class="%s".*?(?=/>|>)' % value, xml)
            if node:
                return self._create_node(node.group())
        elif by == By.PACKAGE:
            node = re.search(r'(?<=<node )index="\d+" text=".*" resource-id=".*" class=".*" package="%s".*?(?=/>|>)' % value, xml)
            if node:
                return self._create_node(node.group())

    def find_nodes(self, by: int, value: str) -> list[Node]:
        self.dump_xml(self._dump)
        if self._error:
            return
        with open(self._dump, mode="r", encoding="utf-8") as file:
            xml = file.read()
        if by == By.TEXT:
            nodes = []
            for node in re.findall(r'(?<=<node )index="\d+" text="%s".*?(?=/>|>)' % value, xml):
                nodes.append(self._create_node(node))
            return nodes
        elif by == By.RESOURCE_ID:
            nodes = []
            for node in re.findall(r'(?<=<node )index="\d+" text=".+" resource-id="%s".*?(?=/>|>)' % value, xml):
                nodes.append(self._create_node(node))
            return nodes
        elif by == By.CLASS:
            nodes = []
            for node in re.findall(r'(?<=<node )index="\d+" text=".*" resource-id=".*" class="%s".*?(?=/>|>)' % value, xml):
                nodes.append(self._create_node(node))
            return nodes
        elif by == By.PACKAGE:
            nodes = []
            for node in re.findall(r'(?<=<node )index="\d+" text=".*" resource-id=".*" class=".*" package="%s".*?(?=/>|>)' % value, xml):
                nodes.append(self._create_node(node))
            return nodes
        return []

    def _create_node(self, node: str) -> Node:
        prop = node.split("\" ")
        values = [p.split("=\"")[1] for p in prop[:-1]]
        return Node(
            parent=self,
            index=int(values[0]),
            text=values[1],
            resource_id=values[2],
            _class=values[3],
            package=values[4],
            content_desc=values[5],
            checkable=False if values[6] == "false" else True,
            checked=False if values[7] == "false" else True,
            clickable=False if values[8] == "false" else True,
            enabled=False if values[9] == "false" else True,
            focussable=False if values[10] == "false" else True,
            focused=False if values[11] == "false" else True,
            scrollable=False if values[12] == "false" else True,
            long_clickable=False if values[13] == "false" else True,
            password=False if values[14] == "false" else True,
            selected=False if values[15] == "false" else True,
            bounds=[(int(x), int(y)) for x , y in [t.split(",") for t in values[16][1:-1].split("][")]]
        )

    def wait(self, second: float):
        time.sleep(second)
        return self

    def hide(self):
        ctypes.windll.user32.ShowWindow(self._top_hwnd, 0)
        return self

    def show(self):
        ctypes.windll.user32.ShowWindow(self._top_hwnd, 1)
        return self

    def _run_adb(self, cmd: str, decode: Optional[str] = "latin-1") -> Union[str, bytes]:
        cmd = cmd.replace("\"", "\\\"")
        return self._run_cmd(f'{self._controller} adb {self._this} --command "{cmd}"', decode)

    @staticmethod
    def _run_cmd(cmd: str, decode: Optional[str] = "latin-1") -> Union[str, bytes]:
        p = subprocess.Popen(cmd, **subprocess_args(), shell=True)
        o, e = p.communicate()
        if p.wait():
            return e.decode(decode) if decode is not None else e
        return o.decode(decode) if decode is not None else e

    def __str__(self):
        return f"ObjectEmulator(index: {self._index}, name: {self._name})"

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_value, traceback):
        self.quit()
        if traceback:
            print(traceback)
