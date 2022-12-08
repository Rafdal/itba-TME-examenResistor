
class TestElement:

	# instance attributes
	def __init__(self, screen):
		self.correctAnswer = ""
		self.screen = screen
		self.drawNewElement = False

	def new(self):
		raise NotImplementedError("New method should be implemented by subclass")

	# instance method
	def draw(self):
		raise NotImplementedError("Draw method should be implemented by subclass")

	def flipOrder(self):
		raise NotImplementedError("Flip order method should be implemented by subclass")

