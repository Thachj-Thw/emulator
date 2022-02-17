class Node:
    def __init__(
        self, 
        parent,
        index: int = 0, 
        text: str = "", 
        resource_id: str = "", 
        _class: str = "", 
        package: str = "", 
        content_desc: str = "", 
        checkable: bool = False, 
        checked: bool = False, 
        clickable: bool = False, 
        enabled: bool = True,
        focussable: bool = False,
        focused: bool = False,
        scrollabled: bool = False,
        long_clickable: bool = False,
        password: bool = False,
        selected: bool = False,
        bounds: tuple[tuple[int, int], tuple[int, int]] = ((0, 0), (0, 0))
    ) -> None:  
        self.parent = parent
        self.index = index
        self.text = text
        self.resource_id = resource_id
        self.class_ = _class
        self.package = package
        self.content_desc = content_desc
        self.checkable = checkable
        self.checked = checked
        self.clickable = clickable
        self.enabled = enabled
        self.focussable = focussable
        self.focused = focused
        self.scrollabled = scrollabled
        self.long_clickable = long_clickable
        self.password = password
        self.selected = selected
        self.bounds = bounds
        self.width = self.bounds[1][0] - self.bounds[0][0]
        self.height = self.bounds[1][1] - self.bounds[0][1]
    
    def tap(self):
        x, y = self.bounds[0]
        self.parent.tap((x + self.width // 2, y + self.height // 2))
    
    def __str__(self):
        return f'<node index="{self.index}" text="{self.text}" resource-id="{self.resource_id}"'\
               f'class="{self.class_}" package="{self.package}" ...>'
