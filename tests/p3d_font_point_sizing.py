from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, DynamicTextFont, Filename

class Font:
	def __init__(self, font_name, point_size, page_size = 256):
		self.name = font_name
		self.point_size = point_size * 1.4
		self.page_size = page_size
		self.face = DynamicTextFont(f'fonts/{font_name}.ttf')
		self.face.set_pixels_per_unit(self.point_size * 1.4)
		self.face.set_page_size(page_size, page_size)

	def save_page(self, page):
		self.face.getPage(page).write(Filename(f'{self.name}_{int(self.point_size / 1.4)}.png'))

class Text:
	def __init__(self, name, text, x, y, font_name, point_size = 15):
		self.x = x
		self.y = -abs(y)

		self.text = TextNode(name)
		self.font = Font(font_name, point_size)
		self.text.setFont(self.font.face)
		self.text.setText(f'{text}')
		self.text.setTextColor(1, 1, .9, 1)
		self.text.generate()
	
		self.panda_node = pixel2d.attach_new_node(self.text)
		self.panda_node.setPos(self.x, 0, self.y)
		self.panda_node.set_scale(self.font.point_size)

base = ShowBase()

txt1 = Text('line_1', 'The quick brown fox jumps over the lazy dog', 0, 10, 'arial', point_size = 10)
txt2 = Text('line_2', 'The quick brown fox jumps over the lazy dog', 0, 35, 'arial', point_size = 15)
txt3 = Text('line_3', 'The quick brown fox jumps over the lazy dog', 0, 65, 'arial', point_size = 20)
txt4 = Text('line_4', 'The quick brown fox jumps over the lazy dog', 0, 100, 'arial', point_size = 25)
txt5 = Text('line_5', 'The quick brown fox jumps over the lazy dog', 0, 140, 'arial', point_size = 30)

base.run()
