from xml.dom.minidom import parse, parseString

class Layout:
    def get_element_by_name(self, name, element = None):
        if hasattr(self, 'name'):
            if self.name == name:
                return self
        if hasattr(self, 'children'):
            for child in self.children:
                if (element := child.get_element_by_name(name)):
                    return element

    def update_positions(self):
        if not isinstance(self, Canvas):
            if isinstance(self.parent, Canvas):
                self.x = self.rx
                self.y = self.ry
            else:
                self.x = self.parent.x + self.rx
                self.y = self.parent.y + self.ry
        if hasattr(self, 'children'):
            for child in self.children:
                child.update_positions()

    def structure(self, indent = 0):
        yield (indent, self)
        if hasattr(self, 'children'):
            for child in self.children:
                yield from child.structure(indent = (indent + 1))

class CanHaveChildren(Layout):
    def __init__(self):
        self.children = []

    def add_child(self, child):
        if child not in self.children:
            child.parent = self
            if isinstance(self, Canvas):
                child.x = child.rx
                child.y = child.ry
            else:
                child.x = self.x + child.rx 
                child.y = self.y + child.ry
            self.children.append(child)

class Canvas(CanHaveChildren):
    def __init__(self, width, height):
        self.name = 'canvas'
        self.width = int(width)
        self.height = int(height)
        super().__init__()

class Element(Layout):
    def __init__(self, rx, ry, name = None):
        self.name = name
        self.parent = None
        self.visible = True
        self.x = 0
        self.y = 0
        self.rx = int(rx)
        self.ry = int(ry)

class Group(Element, CanHaveChildren):
    def __init__(self, rx, ry, name = None):
        Element.__init__(self, rx, ry, name)
        CanHaveChildren.__init__(self)  

class Image(Element):
    def __init__(self, rx, ry, file='dummy_path.png'):
        super().__init__(rx, ry)
        self.file = file

class Text(Element):
    def __init__(self, rx, ry, text='--PLACEHOLDER--'):
        super().__init__(rx, ry)
        self.text = text

def import_layout(xml):
    layout = parseString(xml)
    if layout.firstChild.nodeName == "canvas":
        attributes = {key:value for key, value in layout.firstChild.attributes.items()}
        width, height = int(attributes['width']), int(attributes['height'])
        canvas = Canvas(width = width, height = height)
        get_children(canvas, layout.firstChild.childNodes)
        return canvas

def get_children(parent, layout):
    for child in layout:
        if child.nodeName in ['group','image','text']:
            if child.attributes.items():
                attributes = {key:value for key, value in child.attributes.items()}
                match child.nodeName:
                    case 'group':
                        new_child = Group(attributes['x'], attributes['y'])
                    case 'image':
                        new_child = Image(attributes['x'], attributes['y'])
                        new_child.file = attributes['file']
                    case 'text':
                        new_child = Text(attributes['x'], attributes['y'])
                        new_child.text = attributes['text']
                if 'name' in attributes.keys():
                    new_child.name = attributes['name']
                parent.add_child(new_child)
                if child.nodeName == 'group':
                    get_children(new_child, child.childNodes)

def show_structure(active_object, indent_by = 4):
    for indent_level, element in active_object.structure():
        indent = ' ' * (indent_level * indent_by)
        print(f'{indent}{custom_vars(element)}')

def custom_vars(obj):
    if isinstance(obj, (Canvas, Element)):
        d = {'element':obj.__class__.__name__}
        d.update({key:value for key, value in vars(obj).items()})
        return d

xml_file = """
    <canvas width="1920" height="1080">
        <group name="group_1" x="50" y="50">
            <group x="0" y="0">
                <image x="0" y="0" file="dummy_image.png" />
            </group>
        </group>
        <group name="group_2" x="50" y="150">
            <group x="0" y="0">
                <text x="10" y="10" text="SOME TEXT" />
                <text x="10" y="50" text="MORE TEXT" />
            </group>
        </group>
    </canvas>
"""

canvas = import_layout(xml_file)

if (active_object := canvas.get_element_by_name('group_2')):
    active_object.rx = 50
    active_object.ry = 200
    active_object.update_positions()

show_structure(canvas)

