a1_contents = 'wood'
a1_quantity = '10'

a2_contents = 'stone'
a2_quantity = '7'

a3_contents = 'copper'
a3_quantity = '1'
											
dictionary = {'a1':('rect',[a1_contents,a1_quantity]),
				'a2':('rect',[a2_contents,a2_quantity]),
				'a3':('rect',[a3_contents,a3_quantity])}
				
keys = list(dictionary.keys())

print(keys[0])					# Output: 'a1'
print(dictionary['a1'][0])		# Output: 'rect'																									
print(dictionary['a1'][1][0])  # Output: wood
print(dictionary['a1'][1][1])	# Output: 10


				