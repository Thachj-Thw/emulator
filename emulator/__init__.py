from __future__ import annotations
import os
import subprocess
from .args import subprocess_args
from .em_object import ObjectEmulator
from typing import Iterator, Optional, Union


__version__ = "0.0.6"


class LDPlayer:
    """
    Main cotroll all player of LDPlayer
    """
    def __init__(self, ldplayer_dir: str) -> None:
        self.error = ""
        ld_dir = os.path.normpath(ldplayer_dir)
        if not os.path.exists(ld_dir):
            raise Exception(f'The path: "{ldplayer_dir}" invalid!')
        ldconsole = os.path.join(ld_dir, "ldconsole.exe")
        dnconsole = os.path.join(ld_dir, "dnconsole.exe")
        if os.path.exists(ldconsole):
            self.controller = f'"{ldconsole}"'
        elif os.path.exists(dnconsole):
            self.controller = f'"{dnconsole}"'
        else:
            raise Exception("ldconsole.exe or dnconsole.exe not found")
        self.emulators = EmulatorContainer()
        for info in self.list_index_name():
            e = ObjectEmulator(self, info["index"], info["name"])
            self.emulators.update({info["index"]: e, info["name"]: e})
        self.adb = os.path.join(ld_dir, "adb.exe")
        if not os.path.isfile(self.adb):
            raise Exception("ADB not found!")
        os.system(f'"{self.adb}" start-server')

    def new(self, name: str = None) -> ObjectEmulator:
        exists = self.list_index()
        i = 0
        for _ in range(len(exists)):
            if i not in exists:
                break
            i += 1
        if not name:
            name = "LDPlayer-" + str(i)
        cmd = f'{self.controller} add --name "{name}"'
        self._run_cmd(cmd)
        em = ObjectEmulator(self, i, name)
        self.emulators.update({i: em, name: em})
        return em

    def copy(self, emulator: ObjectEmulator, as_name: str):
        cmd = f'{self.controller} copy --name "{as_name}" --from {emulator.index}'
        self.error = self._run_cmd(cmd)
        exists = self.list_index()
        i = 0
        for _ in range(len(exists)):
            if i not in exists:
                break
            i += 1
        em = ObjectEmulator(self, i, as_name)
        self.emulators.update({i: em, as_name: em})
        return em

    def remove(self, e: ObjectEmulator) -> bool:
        cmd = f'{self.controller} remove {e.this}'
        self.error = self._run_cmd(cmd)
        if self.error:
            return False
        self.emulators.clear()
        for info in self.list_index_name():
            obj = ObjectEmulator(self, info["index"], info["name"])
            self.emulators.update({info["index"]: obj, info["name"]: obj})
        return True

    def list_name(self) -> list[str]:
        return self._run_cmd(f'{self.controller} list').replace("À×µçÄ£ÄâÆ÷", "LDPlayer").split("\r\n")[:-1]

    def list_index(self) -> list[int]:
        return [int(args.split(",")[0]) for args in self._run_cmd(f'{self.controller} list2').split("\r\n")[:-1]]

    def list_index_name(self) -> list[dict]:
        lst = []
        for string in self._run_cmd(f'{self.controller} list2').split("\r\n")[:-1]:
            args = string.split(",")
            lst.append({"index": int(args[0]), "name": args[1].replace("À×µçÄ£ÄâÆ÷", "LDPlayer")})
        return lst

    def list_running(self) -> list[str]:
        return self._run_cmd(f'{self.controller} runninglist').split("\r\n")[:-1]

    def sort_window(self) -> bool:
        cmd = f'{self.controller} sortWnd'
        self.error = self._run_cmd(cmd)
        return False if self.error else True

    def setting(
        self,
        fps: int = None,
        audio: bool = None,
        fastplay: bool = None,
        cleanmode: bool = None
    ) -> bool:
        cmd = f'{self.controller} globalsetting'
        if fps is not None:
            if fps > 60:
                fps = 60
            elif fps < 1:
                fps = 1
            cmd += ' --fps ' + str(fps)
        if audio is not None:
            cmd += ' --audio ' + str(int(audio))
        if fastplay is not None:
            cmd += ' --fastplay ' + str(int(fastplay))
        if cleanmode is not None:
            cmd += ' --cleanmode ' + str(int(cleanmode))
        self.error = self._run_cmd(cmd)
        return False if self.error else True

    def quit_all(self) -> bool:
        cmd = f'{self.controller} quitall'
        self.error = self._run_cmd(cmd)
        return False if self.error else True

    def exit(self) -> bool:
        return os.system(f'"{self.adb}" kill-server')

    def _run_cmd(self, cmd: str, decode: Optional[str] = 'latin-1') -> Union[str, bytes]:
        p = subprocess.Popen(cmd, **subprocess_args())
        o, e = p.communicate()
        if p.wait():
            return e.decode(decode) if decode is not None else e
        return o.decode(decode) if decode is not None else o

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_value, traceback):
        self.quit_all()
        self.kill()
        if traceback:
            print(traceback)


class EmulatorContainer(dict):

    def __getitem__(self, __k) -> ObjectEmulator:
        return super().__getitem__(__k)

    def __iter__(self) -> Iterator[ObjectEmulator]:
        return iter([self[k] for k in self.keys() if type(k) is int])

    def __len__(self) -> int:
        return len([x for x in self.keys() if type(x) is int])

    def __str__(self) -> str:
        return "Emulators(" + ", ".join([self[k].__str__() for k in self.keys() if type(k) is int]) + ")"
