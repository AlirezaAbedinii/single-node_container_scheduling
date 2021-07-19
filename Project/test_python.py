import sys
count = 0
args = sys.argv[1:]
print('Welcome to the test python app')
print(len(args))
for i in range(len(args)):
	print(args[i])