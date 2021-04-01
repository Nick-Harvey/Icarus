import random

class Horseshoe():

	def eightball():
		random_number = random.randint(1, 9)

		if random_number == 1:
			return "Yes - definitely."

		elif random_number == 2:
			return "It is decidedly so."

		elif random_number == 3:
			return "Without a doubt."

		elif random_number == 4:
			return "Reply hazy, try again."

		elif random_number == 5:
			return "Ask again later."

		elif random_number == 6:
			return "Better not tell you now."

		elif random_number == 7:
			return "My sources say no."

		elif random_number == 8:
			return "Outlook not so good."

		elif random_number == 9:
			return "Very doubtful."