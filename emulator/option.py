from typing import Union


class EmulatorOptions:
    """
    options:
    - resolution: width, height, DPI
    - cpu: 1|2|3|4
    - memory: M256|M521|M768|M1024|M1536|M2048|M3078|M4096|M6144
    - manufacturer: samsung, asus, ...
    - model: SM-G970N, ASUS_Z00DUO, ...
    - number: phone number
    - imei: auto
    - imsi: auto
    - simserial: auto
    - android id: auto
    - mac: auto
    - autorotate: True|False
    - lockwindow: True|False
    """
    M256 = 256
    M521 = 521
    M768 = 768
    M1024 = 1024
    M1536 = 1536
    M2048 = 2048
    M3072 = 3072
    M4096 = 4096
    M6144 = 6144
    MEMORY_OPTIONS = [M256, M521, M768, M1024, M1536, M2048, M3072, M4096, M6144]

    def __init__(self) -> None:
        self._options = {}
        self._resolution = (None, None, None)
        self._cpu = None
        self._memory = None
        self._manufacturer = None
        self._model = None
        self._phone_number = None
        self._imei = None
        self._imsi = None
        self._android_id = None
        self._mac = None
        self._auto_rotate = None
        self._lock_window = None

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, new_resolution: Union[list[int, int, int], tuple[int, int, int]]):
        if not isinstance(new_resolution, (list, tuple)):
            raise ValueError("Resolution must be list or tuple")
        if len(new_resolution) < 3:
            raise ValueError("Resolution need 3 arguments: width, height, dpi")
        self.set_resolution(*new_resolution[:3])

    def set_resolution(self, width: int, height: int, dpi: int):
        if width < 64:
            width = 64
        elif width > 4096:
            width = 4096
        if height < 64:
            height = 64
        elif height > 4096:
            height = 4096
        if dpi < 10:
            dpi = 10
        elif dpi > 640:
            dpi = 640
        self._resolution = (width, height, dpi)
        self._options["--resolution"] = f"{width},{height},{dpi}"

    @property
    def cpu(self):
        return self._cpu

    @cpu.setter
    def cpu(self, new_cpu: int):
        self.set_cpu(new_cpu)

    def set_cpu(self, core: int) -> None:
        if not isinstance(core, int):
            raise ValueError("CPU must be an integer between 1 and 4")
        if core < 1:
            core = 1
        elif core > 4:
            core = 4
        self._cpu = core
        self._options["--cpu"] = self._cpu

    @property
    def memory(self):
        return self._memory

    @memory.setter
    def memory(self, new_memory: int):
        self.set_memory(new_memory)

    def set_memory(self, byte: int) -> None:
        if byte not in self.MEMORY_OPTIONS:
            raise ValueError("byte must be one in " + str(self.MEMORY_OPTIONS))
        self._memory = byte
        self._options["--memory"] = self._memory

    @property
    def manufacturer(self):
        return self._manufacturer

    @manufacturer.setter
    def manufacturer(self, new_manufacturer: str):
        self.set_manufacturer(new_manufacturer)

    def set_manufacturer(self, manufacturer: str) -> None:
        if not isinstance(manufacturer, str):
            raise ValueError("Manufacturer must be a string")
        self._manufacturer = manufacturer
        self._options["--manufacturer"] = self._manufacturer

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, new_model: str):
        self.set_model(new_model)

    def set_model(self, model: str) -> None:
        if not isinstance(model, str):
            raise ValueError("Model must be a string")
        self._model = model
        self._options["--model"] = self._model

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, new_phone_number: str):
        self.set_phone_number(new_phone_number)

    def set_phone_number(self, phone_number: str) -> None:
        if not isinstance(phone_number, str):
            raise ValueError("PhoneNumber must be a string")
        self._phone_number = phone_number
        self._options["--pnumber"] = self._phone_number

    @property
    def imei(self):
        return self._imei

    @imei.setter
    def imei(self, new_imei: str):
        self.set_imei(new_imei)

    def set_imei(self, imei: str) -> None:
        if not isinstance(imei, str):
            raise ValueError("IMEI must be a string")
        self._imei = imei
        self._options["--imei"] = self._imei

    @property
    def imsi(self):
        return self._imsi

    @imsi.setter
    def imsi(self, new_imsi: str):
        self.set_imsi(new_imsi)

    def set_imsi(self, imsi: str) -> None:
        if not isinstance(imsi, str):
            raise TypeError("IMSI must be a string")
        self._imsi = imsi
        self._options["--imsi"] = self._imsi

    @property
    def android_id(self):
        return self._android_id

    @android_id.setter
    def android_id(self, new_android_id: str):
        self.set_android_id(new_android_id)

    def set_android_id(self, android_id: str) -> None:
        if not isinstance(android_id, str):
            raise TypeError("Android ID must be a string")
        self._android_id = android_id
        self._options["--androidid"] = self._android_id

    @property
    def mac(self):
        return self._mac

    @mac.setter
    def mac(self, new_mac: str):
        self.set_mac(new_mac)

    def set_mac(self, mac: str) -> None:
        if not isinstance(mac, str):
            raise TypeError("Mac ID must be a string")
        self._mac = mac
        self._options["--mac"] = self._mac

    @property
    def auto_rotate(self):
        return self._auto_rotate

    @auto_rotate.setter
    def auto_rotate(self, new_auto_rotate: bool):
        self.set_auto_rotate(new_auto_rotate)

    def set_auto_rotate(self, b: bool = True) -> None:
        if not isinstance(b, bool):
            raise ValueError("Auto-rotate must be a boolean")
        self._auto_rotate = b
        self._options["--autorotate"] = int(self._auto_rotate)

    @property
    def lock_window(self):
        return self._lock_window

    @lock_window.setter
    def lock_window(self, new_lock_window: bool):
        self.set_lock_window(new_lock_window)

    def set_lock_window(self, b: bool = True) -> None:
        if not isinstance(b, bool):
            raise ValueError("Lock Window must be a boolean")
        self._lock_window = b
        self._options["--lockwindow"] = int(self._lock_window)

    @property
    def options(self):
        return self._options
