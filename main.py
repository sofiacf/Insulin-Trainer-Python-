import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.label import Label

class InsulinTrainer(App):
	def build(self):
		return Label(text='Test')

if __name__ == '__main__':
	InsulinTrainer().run()

