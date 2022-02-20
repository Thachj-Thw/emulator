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
        self.options = {}
    
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
        self.options["--resolution"] = f"{width},{height},{dpi}"
    
    def set_cpu(self, core: int) -> None:
        if core < 1:
            core = 1
        elif core > 4:
            core = 4
        self.options["--cpu"] = int(core)
    
    def set_memory(self, byte: int) -> None:
        if byte not in self.MEMORY_OPTIONS:
            raise Exception("byte must be one in " + str(self.MEMORY_OPTIONS))
        self.options["--memory"] = byte
    
    def set_manufacturer(self, manufacturer: str) -> None:
        self.options["--manufacturer"] = manufacturer
    
    def set_model(self, model: str) -> None:
        self.options["--model"] = model
    
    def set_number(self, phone_number: str) -> None:
        self.options["--pnumber"] = phone_number
    
    def set_imei(self, imei: str) -> None:
        self.options["--imei"] = imei
    
    def set_imsi(self, imsi: str) -> None:
        self.options["--imsi"] = imsi

    def set_android_id(self, id: str) -> None:
        self.options["--androidid"] = id
    
    def set_mac(self, mac: str) -> None:
        self.options["--mac"] = mac
    
    def set_auto_rotate(self, b: bool = True) -> None:
        self.options["--autorotate"] = int(b)
    
    def set_lock_window(self, b: bool = True) -> None:
        self.options["--lockwindow"] = int(b)
