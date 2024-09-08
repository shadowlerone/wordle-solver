


import random


WORD_LIST = []

RESET = "\u001B[0m"

COLOR_STRING = {
	0: "",
	1: "\u001B[42m",
	2: "\u001B[43m",
}

with open("words_alpha.txt") as file:
	WORD_LIST = [line.rstrip() for line in file ]
"""
status legend:
0: not in word
1: in right place
2: in word
"""
class LetterData():
	def __init__(self, letter, status):
		self.letter = letter
		self.status = status
	def __str__(self):
		return f"{COLOR_STRING[self.status]}{self.letter}{RESET}"
	
	def __repr__(self) -> str:
		return self.__str__()


class WordleResponse():
	def __init__(self, status:int, message:str= "", letter_data:list[LetterData]=None):
		self.status:int = status
		self.letter_data:list[LetterData] = letter_data
		self.message:str = message
	
	def __str__(self):
		return f"status: {self.status}\nmessage: {self.message}\nletter data: {self.letter_data}"
	def get_letter_data(self):
		out = ""
		for l in self.letter_data:
			out += str(l)
		return out

"""
Statuses
-1: game over
0: invalid guess
1: correct word
2: has data

"""

class Wordle():
	def __init__(self, wordlength=5, word = None):
		self.guess_count = 0
		self.response_chain = []
		if word and word in WORD_LIST:
			self.dictionary = [words for words in WORD_LIST if len(words) == len(word)]
			self.length = len(word)
			self.word = word
		else:
			self.dictionary = [words for words in WORD_LIST if len(words) == wordlength]
			self.length = wordlength
			self.word = random.choice(self.dictionary)


	def print_chain(self):
		print("=" * self.length)
		for rp in self.response_chain:
			print(rp.get_letter_data())
		print("=" * self.length)

	def guess(self, guess:str) -> WordleResponse:
		
		if len(guess) < self.length:
			return WordleResponse(0, message="too short!")
		if len(guess) > self.length:
			return WordleResponse(0, message="too long!")
		
		if guess not in self.dictionary:
			return WordleResponse(0, message="not in word list")
		
		self.guess_count +=1
		
		# check if letters are in right place
		response_data = [None] * self.length
		for l_index in range(self.length):
			letter = guess[l_index]
			status = 0
			if letter == self.word[l_index]:
				status = 1
			elif letter in self.word:
				status = 2
			response_data[l_index] = LetterData(letter=letter, status= status)
		if guess == self.word:
			response = WordleResponse(1, message="You Won!", letter_data=response_data)
		elif self.guess_count == 6:
			response = WordleResponse(-1, message="Game Over", letter_data=response_data)

		else:			
			response = WordleResponse(2, message="Try again!", letter_data=response_data)
		self.response_chain.append(response)

		return response
	
	def play(self):
		while self.guess_count < 6:
			guess= input(f"Select a {self.length} letter word:")
			response = self.guess(guess)
			if response.status == 0:
				print(response.message)
				continue

			self.print_chain()
			print(response.message)
			if response.status == 1:
				break
		print("Game Over!")
		print(f"The word was {self.word}")		

if __name__ == "__main__":
	print("Testing Wordle")

	game = Wordle(word="owner")
	game.play()
	# game.guess("test")
	# game.print_chain()
	# game.guess("arise")
	# game.print_chain()
	# game.guess("round")
	# game.print_chain()
	# game.guess("tenor")
	# game.print_chain()
	# game.guess("owner")
	# game.print_chain()
	# game.guess("chain")
	# game.print_chain()
	# game.guess("tower")
	# game.print_chain()


