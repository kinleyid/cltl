
# Ideas: t + a should add all tasks to today's list
# t + n should create a new item and add it to today's list
# t + n n should do this with 2 items
# t 1 should display the first thing you have to do today
# t 1 = n should create a new item and make it the second thing you have to do today
# p should get the previous day's to-dos
# n should be an alias for a + n
# re t 1 3 2 4 should re-order today's tasks
# d should alias t - 1
# a - 1 should delete the first item
# t + a 1 3 5 should add the 1st, 3rd, & 5th items to today's to-do list
# t 1 should display the first thing to do today
# re as short for replace
# d as done or delete

# a # display all
# t + a 1 10 11 # add the 1st, 10th, & 11th items to today's to do list
# d # delete the items from the to do list
# n # add a new item for later

# Easiest if order of command and args doesn't matter
# Functions:
# +: add to list
# d: remove from list (delete/done)
# r: 

import pickle

# Global variables
keys = ['Title', 'Description', 'Importance', 'Urgency', 'Duration', 'Fun']
defaults = ['', '', 0, 0, 0, 0]
savefilename = 'saved.dat'
try:
	all_lists = pickle.load(open(savefilename, 'rb'))
except: # First time running program
	print('\nWelcome to the command line to-do list!\nThe master repository is at github.com/kinleyid/cltl\n')
	open(savefilename, 'wb').close() # Initialize save file
	# Initialize global variables
	all_lists = {
		'a': [], # All tasks
		't': [], # Today's tasks
		'h': [], # History of tasks
		'ans': []} # Most recently printed set of tasks

def new_task():
	out_dict = {}
	for idx in range(len(keys)):
		key = keys[idx]
		out_dict[key] = input(key + ': ')
		if out_dict[key] == '':
			out_dict[key] = defaults[idx]
	print('')
	return [out_dict]

def get_indices(ls, idx):
	if idx == []:
		idx = list(range(len(ls)))
	out = []
	for i in idx:
		out += [ls[i]]
	return(out)

def delete_indices(key, idx): # Delete permanently
	if idx == []:
		idx = list(range(len(all_lists[key])))
	idx.sort()
	for i in range(len(idx)):
		del all_lists[key][idx[i] - i]
		
def recycle_indices(key, idx): # Move to history
	if idx == []:
		idx = list(range(len(all_lists[key])))
	idx.sort()
	for i in range(len(idx)):
		all_lists['h'] += all_lists[key].pop(idx[i] - i)

def move_indices(key1, key2, idx):
	if idx == []:
		idx = list(range(len(all_lists[key2])))
	all_lists[key1] += get_indices(all_lists[key2], idx)
	delete_indices(key2, idx)

def get_printable(item):
	return('%s | %s\n\t%s' % (item['Title'],
		''.join(['*' for i in range(int(item['Importance']))]),
		item['Description']))

def print_list(items):
	print('')
	for idx in range(len(items)):
		print('[%d]: %s' % (idx + 1, get_printable(items[idx])))
	all_lists['ans'] = items
	print('')

def parse_in(cmd):
	raw = cmd.split()
	if raw != []:
		subj = None
		verb = None
		obj = []
		idx = []
		
		# Parse tree
		for curr in raw:
			if curr in ['n', 'a', 't', 'h']:
				if subj == None:
					subj = curr
				else:
					obj += [curr]
			elif curr in ['+', 're', 'd']:
				verb = curr
			elif curr.isdigit():
				idx += [int(curr)]
			elif cmd == 'x': # exit program
				with open(savefilename, 'wb') as save_file:
					pickle.dump(all_lists, save_file)
				exit()
		
		# idx from human to python
		idx = list(map(lambda x: x - 1, idx))
		
		# Evaluate command
		if subj == None: # No first arg
			if verb == 'd':
				del all_lists['t'][0] # Delete current task
			elif verb == '+':
				all_lists['a'] += new_task() # Add new task to all
		
		elif obj == []: # First arg, no second arg
			if verb == None: # Only first arg
				if subj == 'n':
					all_lists['a'] += new_task() # Create new task
				elif subj in ['a', 't', 'h',]:
					print_list(get_indices(all_lists[subj], idx)) # Display tasks
			else: # Only first arg and function
				if verb == 're': # Re-order subj
					if sorted(idx) != list(range(len(all_lists[subj]))): # Error
						print('Index error')
					else:
						all_lists[subj] = get_indices(all_lists[subj], idx)
				elif verb == 'd': # Remove
					if subj == 'h': # Delete permanently
						delete_indices(subj, idx)
					else:
						recycle_indices(subj, idx)
				elif verb == '+': # Add new task
					all_lists[subj] += new_task()
		
		else: # First arg and second arg
			if verb == '+':
				for curr_obj in obj:
					if curr_obj == 'n':
						all_lists[subj] += new_task()
					else:
						move_indices(subj, curr_obj, idx)

def main_loop():
	while True: # Main loop
		with open(savefilename, 'wb') as save_file:
			pickle.dump(all_lists, save_file)
		if all_lists['t'] == []:
			print('No current task!')
		else:
			print('Current task: %s' % get_printable(all_lists['t'][0]))
		parse_in(input('>| '))

main_loop()

