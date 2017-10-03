def notvowels(string):
	a = ""
	for letter in string:
		if not (letter in "aeiouAEIOU"):
			a = a + letter
	return a
print(notvowels('Elysia'))