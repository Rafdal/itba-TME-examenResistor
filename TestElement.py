


class Parrot:

	# instance attributes
	def __init__(self):
		self.correctAnswer = ""

	# instance method
	def sing(self, song):
		return '{} sings {}'.format(self.name, song)

	def dance(self):
		return '{} is now dancing'.format(self.name)

