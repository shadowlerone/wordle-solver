import enum
import random
from wordle import Wordle


WORD_LIST = []

with open("words_alpha.txt") as file:
	WORD_LIST = [line.rstrip() for line in file if len(line.rstrip()) == 5]
	
class Solver():
	def __init__(self, wordle:Wordle):
		self.wordle = wordle
		self.possible_words = WORD_LIST
		self.guess_data = [None] * 6
		self.guesses = 0
		self.state = 0

	
	def step1(self):
		# filter out words that don't match length
		self.possible_words = [
			w for w in self.possible_words if len(w) == self.wordle.length
		]

	def guess(self, word="crane"):
		response = self.wordle.guess(word)
		self.guesses = self.wordle.guess_count
		if response.status == 0 :
			return 0
		if response.status == -1:
			self.state = -1
			return -1
		if response.status == 1:
			self.state = 1
			return 1
		# ld = response.letter_data
		for idx, ld in enumerate(response.letter_data):
			# letter is in the right place
			if ld.status == 1:
				self.possible_words = [
					w for w in self.possible_words if w[idx] == ld.letter
				]
			# letter is not in the word
			elif ld.status == 0:
				self.possible_words = [
					w for w in self.possible_words if ld.letter not in w
				]
			# letter is in the word
			elif ld.status == 2:
				self.possible_words = [
					w for w in self.possible_words if ld.letter in w and ld.letter != w[idx]
				]

	def solve(self):
		self.guess()
		# self.wordle.print_chain()
		# print(len(self.possible_words))
		# print(self.wordle.word in self.possible_words)
		while self.state != -1 and self.state != 1:
			self.guess(random.choice(self.possible_words))
			# TODO: Make guess selection algorithm


			# self.wordle.print_chain()
			# print(len(self.possible_words))
		return self.state == 1
if __name__ == "__main__":
		# print("Testing Wordle")
	x = 0
	fails = 0
	guesses = []
	while x < 100000:

		game = Wordle()
		s = Solver(game)
		if s.solve():
			guesses.append(s.guesses)
		else:
			fails += 1
		# print(f"solved in: {s.guesses}")
		x+=1
	
	print(f"fails: {fails}")
	print(f"max guesses: {max(guesses)}\nmin guesses: {min(guesses)}\naverage guesses: {sum(guesses)/x}")