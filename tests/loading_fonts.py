from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, DynamicTextFont, Filename

class Fonts:
	def __init__(self):
		self.cache = {}

	def get(self, font_name, point_size, new = False):
		if font_name not in self.cache.keys():
			new = Font(font_name, point_size)
			self.cache.update({font_name: {point_size: new}})
		else:
			if point_size not in self.cache[font_name].keys():
				new = Font(font_name, point_size)
				self.cache[font_name].update({point_size: new})
		return self.cache[font_name][point_size]
			
class Font:
	def __init__(self, font, point_size, page_size = 256):
		self.name = font
		self.point_size = point_size * 1.4
		self.page_size = page_size

		self.face = DynamicTextFont(f'fonts/{font}.ttf')
		self.face.set_pixels_per_unit(self.point_size*1.4)
		self.face.set_page_size(page_size, page_size)

	def save_page(self, page):
		self.face.getPage(page).write(Filename(f'{self.name}_{int(self.point_size/1.4)}.png'))

class Text:
	def __init__(self, name, text, x, y, font, point_size = 15):
		self.x = x
		self.y = -abs(y)

		self.font = fonts.get(font, point_size)

		self.text = TextNode(name)
		self.text.setFont(self.font.face)
		self.text.setText(f'{text}')
		self.text.setTextColor(0, 0, .8, 1)
		self.text.generate()
	
		self.panda_node = pixel2d.attach_new_node(self.text)
		self.panda_node.setPos(self.x, 0, -abs(self.y))
		self.panda_node.set_scale(self.font.point_size)

base = ShowBase()

fonts = Fonts()

Text('line_1', 'The quick brown fox jumped over the lazy dog', 0, 150, 'arial', point_size = 10)
Text('line_2', 'The quick brown fox jumped over the lazy dog', 0, 180, 'arial', point_size = 15)
Text('line_3', 'The quick brown fox jumped over the lazy dog', 0, 215, 'arial', point_size = 20)
Text('line_4', 'The quick brown fox jumped over the lazy dog', 0, 255, 'arial', point_size = 25)
Text('line_5', 'The quick brown fox jumped over the lazy dog', 0, 300, 'arial', point_size = 30)

for font in fonts.cache:
	for size in fonts.cache[font]:
		fonts.cache[font][size].save_page(0)

#pixel2d.ls()

print(fonts.cache)

base.run()
