import pyttsx3

engine = pyttsx3.init()

commands = {
	"opening" : "I'm thinking of a person out of these 21 options. Go ahead and ask questions!",
	"yes" : "Yep, you got it!",
	"no" : "Nope, try another question!",
	"end_game" : "You guessed the right person! You won...congrats!",
	"stuck" : "Hmm...consider some things you haven't asked yet.",
	"wrong_guess" : "Good try but not there yet!"
}

engine.say(commands["end_game"])
engine.runAndWait()