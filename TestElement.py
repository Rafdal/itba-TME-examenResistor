# TestElement Base Class

class TestElement:
	correctAnswer = ""
	hint = "Hint"
	title = "TestElement"
	streak = 0
	correctCount = 0
	totalCount = 0

	# instance attributes
	def __init__(self,screen):
		self.screen = screen

	def new(self):
		raise NotImplementedError("New method should be implemented by subclass")

	# instance method
	def draw(self):
		raise NotImplementedError("Draw method should be implemented by subclass")

	def flipOrder(self):
		raise NotImplementedError("Flip order method should be implemented by subclass")

