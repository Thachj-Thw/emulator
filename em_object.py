from __future__ import annotations
from importlib import resources
from typing import Union, Optional
import subprocess
from .option import EmulatorOption
from .args import subprocess_args
from .opencv import get_pos_img, existed
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
    dump = os.path.join(os.path.normpath(os.path.dirname(__file__)), "dump", "window_dump.xml")
    
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
        self.parent = parent
        self.controller = parent.controller
        self.index = index
        self.name = name
        self.top_hwnd = top_hwnd
        self.bind_hwnd = bind_hwnd
        self.android = android
        self.pid = pid
        self.pid_vbox = pid_vbox
        self.this = "--index " + str(self.index)
        self.error = ""
    
    def start(self, wait: bool = True):
        if not self.is_running():
            self._run_cmd(f'{self.controller} launch {self.this}')
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
        cmd = f'{self.controller} list2 | "{self.sed}" -n "/^{self.index}/p"'
        args = self._run_cmd(cmd)[:-2].split(",")
        if args[2] != "0":
            self.top_hwnd = int(args[2])
            self.bind_hwnd = int(args[3])
            self.android = int(args[4])
            self.pid = int(args[5])
            self.pid_vbox = int(args[6])
            return True
        return False
    
    def wait_to_started(self, timeout=60):
        timer = time.perf_counter()
        while time.perf_counter() - timer < timeout and not self.adb_connected():
            time.sleep(1)
        return self
    
    def is_running(self) -> bool:
        cmd = f'{self.controller} isrunning {self.this}'
        return self._run_cmd(cmd) == "running"

    def restart(self, wait=False):
        if self.is_running():
            cmd = f'{self.controller} reboot {self.this}'
            self._run_cmd(cmd)
            if wait:
                self.wait_to_started()
            else:
                time.sleep(3)
            self._update()
            return self
        self.error = "emulator is not running"
        return self
    
    def rename(self, new_name: str):
        cmd = f'{self.controller} rename {self.this} --title "{new_name}"'
        self.error = self._run_cmd(cmd)
        if not self.error:
            self.name = new_name
        return self
    
    def install_app(self, source: str):
        if self.is_running():
            path = os.path.normpath(source)
            if os.path.isfile(path):
                cmd = f'{self.controller} installapp {self.this} --filename "{path}"'
            else:
                cmd = f'{self.controller} installapp {self.this} --packagename "{source}"'
            self.error = self._run_cmd(cmd)
        else:
            self.error = "The emulator is not started!"
        return self
    
    def uninstall_app(self, package_name: str):
        if self.is_running():
            cmd = f'{self.controller} uninstallapp {self.this} --packagename "{package_name}"'
            self.error = self._run_cmd(cmd)
        else:
            self.error = "The emulator is not started!"
        return self
    
    def run_app(self, package_name: str):
        if self.is_running():
            cmd = f'{self.controller} runapp {self.this} --packagename "{package_name}"'
            self.error = self._run_cmd(cmd)
        else:
            self.error = "The emulator is not started!"
        return self
    
    def kill_app(self, package_name: str):
        if self.is_running():
            cmd = f'{self.controller} killapp {self.this} --packagename "{package_name}"'
            self.error = self._run_cmd(cmd)
        else:
            self.error = "The emulator is not started!"
        return self
    
    def list_packages(self) -> Optional[list]:
        cmd = f"shell pm list packages | sed 's/^package://'"
        return [package for package in self._run_adb(cmd).split("\r\r\n")[:-1]]

    def set_locate(self, locate: str):
        if self.is_running():
            cmd = f'{self.controller} locate {self.this} --LLI "{locate}"'
            self.error = self._run_cmd(cmd)
        else:
            self.error = "The emulator is not started!"
        return self
    
    def update_properties(self, prop: dict):
        for key in prop.keys():
            cmd = f'{self.controller} setprop {self.this} --key "{key}" --value "{prop[key]}"'
            self.error = self._run_cmd(cmd)
            if self.error:
                break
        return self
    
    def get_properties(self) -> dict:
        cmd = f"shell getprop | sed 's/[][]//g'"
        lst = self._run_adb(cmd, decode=False).decode("latin-1").split("\r\r\n")[:-1]
        return {key: value for key, value in [x.split(": ") for x in lst]}
    
    def down_cpu(self, rate: int):
        if rate < 0:
            rate = 0
        if rate > 100:
            rate = 100
        cmd = f'{self.controller} downcpu {self.this} --rate {int(rate)}'
        self.error = self._run_cmd(cmd)
        return self
    
    def backup(self, file_path: str):
        path = os.path.normpath(file_path)
        cmd = f'{self.controller} backup {self.this} --file "{path}"'
        self.error = self._run_cmd(cmd)
        return self
    
    def restore(self, file_path: str):
        path = os.path.normpath(file_path)
        if os.path.isfile(path):
            cmd = f'{self.controller} restore {self.this} --file "{path}"'
            self.error = self._run_cmd(cmd)
        else:
            self.error = f'Path "{file_path}" invalid!'
        return self
    
    def action(self, actions: dict):
        for key in actions.keys():
            cmd = f'{self.controller} action {self.this} --key "{key}" --value "{actions[key]}"'
            self.error = self._run_cmd(cmd)
            if self.error:
                break
        return self
    
    def scan(self, file_path: str):
        if self.is_running():
            path = os.path.normpath(file_path)
            if os.path.isfile(path):
                cmd = f'{self.controller} scan {self.this} --file "{path}"'
                self.error = self._run_cmd(cmd)
            else:
                self.error = f'Path "{file_path}" invalid!'
        else:
            self.error = "emulator is not running"
        return self
    
    def pull(self, remote: str, local: str):
        lo_path = os.path.normpath(local)
        cmd = f'pull "{remote}" "{lo_path}"'
        out = self._run_adb(cmd)
        if "KB/s" not in out:
            self.error = out
        return self
    
    def push(self, local: str, remote: str):
        lo_path = os.path.normpath(local)
        cmd = f'push "{lo_path}" "{remote}"'
        out = self._run_adb(cmd)
        print(out)
        if "KB/s" not in out:
            self.error = out
            print(self.error)
        return self
    
    def capture(self, as_file):
        path = os.path.normpath(as_file)
        cmd = "shell screencap -p | base64 | sed 's/\\r\\r$//'"
        with open(path, mode="wb") as file:
            file.write(base64.b64decode(self._run_adb(cmd)))
        return self
    
    def quit(self) -> None:
        cmd = f'{self.controller} quit {self.this}'
        self._run_cmd(cmd)
    
    def property_setting(self, options: EmulatorOption):
        opts = " ".join([f"{key} {options.options[key]}" for key in options.options.keys()])
        if opts:
            cmd = f'{self.controller} modify {self.this} {opts}'
            self.error = self._run_cmd(cmd)
        return self
    
    def adb_connected(self) -> bool:
        cmd = f'{self.controller} adb {self.this} --command "get-state"'
        return self._run_cmd(cmd)[:-3] == "device"
    
    def tap(self, pos: position):
        cmd = f'shell input tap {pos[0]} {pos[1]}'
        self.error = self._run_adb(cmd)
        return self
    
    def swipe(self, _from: position, to: position, duration: int = 100):
        cmd = f'shell input swipe {_from[0]} {_from[1]} {to[0]} {to[1]} {duration}'
        self.error = self._run_adb(cmd)
        return self
    
    def send_text(self, text: str):
        cmd = f'shell input text "{text.replace(" ", r"%s")}"'
        self.error = self._run_adb(cmd)
        return self
    
    def send_event(self, keycode: int):
        cmd = f'shell input keyevent {keycode}'
        self.error = self._run_adb(cmd)
        return self
    
    def home(self):
        return self.send_event(3)
    
    def back(self):
        return self.send_event(4)
    
    def app_switcher(self):
        return self.send_event(187)
    
    def tap_to_img(self, img_path: str, threshold: float = 0.8):
        path = os.path.normpath(img_path)
        if os.path.isfile(path):
            base = base64.b64decode(self._run_adb("shell screencap -p | base64 | sed 's/\\r\\r$//'"))
            if pos := get_pos_img(path, base, threshold=threshold):
                self.tap(pos[0])
            else:
                self.error = "image not in screen"
        else:
            self.error = f'The path "{img_path}" invalid!'
        return self
    
    def tap_to_imgs(self, img_path: str, threshold: float = 0.8):
        path = os.path.normpath(img_path)
        if os.path.isfile(path):
            base = base64.b64decode(self._run_adb("shell screencap -p | base64 | sed 's/\\r\\r$//'"))
            if pos := get_pos_img(path, base, multi=True, threshold=threshold):
                for p in pos:
                    self.tap(p)
            else:
                self.error = "image not in screen"
        else:
            self.error = f'The path "{img_path}" invalid!'
        return self

    def wait_img_existed(self, img_path: str, timeout: int = 0, threshold: float = 0.8):
        path = os.path.normpath(img_path)
        if os.path.isfile(path):
            timer = time.perf_counter()
            while not existed(
                path, 
                base64.b64decode(self._run_adb("shell screencap -p | base64 | sed 's/\\r\\r$//'")), 
                threshold
            ):
                if timeout != 0 and time.perf_counter() - timer > timeout:
                    self.error = "Timeout"
                    break
        else:
            self.error = f'The path "{img_path}" invalid'
        return self
    
    def dump_xml(self, as_file: str):
        path = os.path.normpath(as_file)
        cmd = 'shell uiautomator dump /sdcard/window_dump.xml'
        self._run_adb(cmd)
        self.pull("/sdcard/window_dump.xml", path)
        return self
    
    def get_node(self, by: int, value: str) -> Optional[Node]:
        self.dump_xml(self.dump)
        with open(self.dump, mode="r", encoding="utf-8") as file:
            xml = file.read()
        if by == By.TEXT:
            if node := re.search(r'(?<=<node )index="\d+" text="%s".*?(?=/>|>)' % value, xml):
                return self._create_node(node.group())
        elif by == By.RESOURCE_ID:
            if node := re.search(r'(?<=<node )index="\d+" text=".+" resource-id="%s".*?(?=>)' % value, xml):
                return self._create_node(node.group())
        elif by == By.CLASS:
            if node := re.search(r'(?<=<node )index="\d+" text=".*" resource-id=".*" class="%s".*?(?=>)' % value, xml):
                return self._create_node(node.group())
        elif by == By.PACKAGE:
            if node := re.search(r'(?<=<node )index="\d+" text=".*" resource-id=".*" class=".*" package="%s".*?(?=>)' % value, xml):
                return self._create_node(node.group())
        
    def get_nodes(self, by: int, value: str) -> list[Node]:
        self.dump_xml(self.dump)
        with open(self.dump, mode="r", encoding="utf-8") as file:
            xml = file.read()
        if by == By.TEXT:
            nodes = []
            for node in re.findall(r'(?<=<node )index="\d+" text="%s".*?(?=/>|>)' % value, xml):
                nodes.append(self._create_node(node))
            return nodes
        elif by == By.RESOURCE_ID:
            nodes = []
            for node in re.findall(r'(?<=<node )index="\d+" text=".+" resource-id="%s".*?(?=>)' % value, xml):
                nodes.append(self._create_node(node))
            return nodes
        elif by == By.CLASS:
            nodes = []
            for node in re.findall(r'(?<=<node )index="\d+" text=".*" resource-id=".*" class="%s".*?(?=>)' % value, xml):
                nodes.append(self._create_node(node))
            return nodes
        elif by == By.PACKAGE:
            nodes = []
            for node in re.findall(r'(?<=<node )index="\d+" text=".*" resource-id=".*" class=".*" package="%s".*?(?=>)' % value, xml):
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
        ctypes.windll.user32.ShowWindow(self.top_hwnd, 0)
        return self
    
    def show(self):
        ctypes.windll.user32.ShowWindow(self.top_hwnd, 1)
        return self
    
    def _run_adb(self, cmd: str, decode: bool = True) -> Union[str, bytes]:
        if self.adb_connected():
            cmd = cmd.replace("\"", "\\\"")
            return self._run_cmd(f'{self.controller} adb {self.this} --command "{cmd}"', decode)
        return "adb is not connected"

    @staticmethod
    def _run_cmd(cmd: str, decode: bool = True) -> Union[str, bytes]:
        p = subprocess.Popen(cmd, **subprocess_args(), shell=True)
        o, e = p.communicate()
        if p.wait():
            return e.decode("utf-8") if decode else e
        return o.decode("utf-8") if decode else o

    def __str__(self):
        return f"ObjectEmulator(index: {self.index}, name: {self.name})"
    
    def __enter__(self):
        return self
    
    def __exit__(self, _exc_type, _exc_value, traceback):
        self.quit()
        if traceback:
            print(traceback)
