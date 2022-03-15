def textwrapper(wrap_size,input_arg,on_spacer=True,spacer_whole_word =False,spacer =" ",text_purity = False):
	"""
	Returns Strings' array wrapping input_arg with wrap_size

	Parametrs :
		wrap_size (int)
			(cannot be 0)
		input_arg (str or list[str])
		on_spacer determines if returned substrings should stop on spacer (bool)
			(will research the longest substring w/ len<wrap_size ending on a spacer)
		spacer_whole_word dertermines if spacer should not trigger on words that contains spacer as a subword (bool)
		spacer (str)
			(cannot be the empty string '')
		text_purity removes \\n (bool)
	Returns : 
		retlist substrings of input_arg cut with wrap size (list[str])

	Note :
		1) If on_spacer is used and the length between spacers is superior to wrap_size,
			the result substring will have the full spacer-encased substring
		2) spacer_whole_word is meant for languages having " " as a natural word separator (mostly Natural languages)
			analysis could have issues with special characters (',','.','!',etc...)
			implementation of another argument native_subspacers (list[str]) is likely to happen (heavier).
	"""
	retlist = []
	textBuffer =""
	if type(input_arg) == list:
		prelist = input_arg[:]
		while len(prelist)>0:
			textBuffer+=prelist.pop(0)
	else :
		textBuffer = input_arg


	if text_purity:
		textBuffer = textBuffer.replace('\n','')
	
	if spacer_whole_word :
		spacer = " "+ spacer + " "
	
	while len(textBuffer)>0:
		if not(on_spacer) :
			retlist.append(textBuffer[:wrap_size])
			textBuffer = textBuffer[wrap_size:]
		else :	
			if spacer in textBuffer[:wrap_size]  or len(textBuffer)<wrap_size:
				retlist.append(textBuffer[:wrap_size])
			elif spacer in textBuffer[wrap_size:]:
				retlist.append(textBuffer[:wrap_size]+textBuffer[wrap_size:textBuffer[wrap_size:].index(spacer)+wrap_size+len(spacer)]) #solving Note 1
			else :
				retlist.append(textBuffer)

			textBuffer = textBuffer[len(retlist[-1]):]
			if retlist[-1][-1] != spacer and textBuffer != "":
				substring_last_spacer = retlist[-1].rsplit(spacer,1)+ [""] #solving Note 1 and preventing out of index in second next instruction.
				retlist[-1] = substring_last_spacer[0]+spacer
				textBuffer = substring_last_spacer[1]+textBuffer
			
	return retlist[:]

def non_module_exec() :
	a = "coeurs ! étoiles ! brouzoufs ! salaire "
	b = ""
	print(textwrapper(5,b))

if __name__ == '__main__':
 	non_module_exec()