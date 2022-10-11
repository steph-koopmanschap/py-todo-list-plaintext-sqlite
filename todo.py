'''
Authors: Stephanus Koopmanschap
'''
#===========IMPORTS=======================

import random
import sqlite3
from sqlite3 import Error

#===========GLOBALS=======================

databaseFile = 'todo.db'
db = None #database instance for quering SQLITE
commands = ["", "list", "task", "subtask", "help", "export", "exit"]
operations = ["", "create", "delete", "rename", "checkoff"]

#==================================

#===========UTIL FUNCTIONS=======================

def showManual():
	print("Commands:")
	print("---------")
	print("list:[create|delete|rename]:<name of list>:<renamed list>")
	print("task:[create|delete|rename|checkoff]:<name of task>:<name of list>:<renamed task>")
	print("subtask:[create|delete|rename|checkoff]:<name of sub task>:<name of task>:<name of list>:<renamed subtask>")
	print("exit (Close this program)")
	print("export:filename (Feature not yet implemented)")
	print("help (shows this manual)")
	print("Examples:")
	print("	task:create:my new task:my list")
	print("	task:checkoff:my new task")
	print("	subtask:create:my new sub task:my new task:my list")
	print("---------")

def getUserInput():
	global commands
	global operations

	print("What would you like to do?")
	print("type \"help\" to see the manual")
	print("(Press Enter to do nothing...)")

	userInput = input()
	userInput = userInput.strip().split(':')
	
	command = userInput[0]
	operation = []
	operands = []
	if len(userInput) > 1:
		operation = userInput[1]
		operands = userInput[2:len(userInput)]

	#Check if correct user input
	if command not in commands:
		err()
		return 1
	if len(operation) >= 1:
		if operation not in operations:
			err()
			return 1
	
	chooseOperation(command, operation, operands)

#Interpret user input and do some action based on input
def chooseOperation(command, operation, operands):
	
	match command:
		case "list":
			match operation:
				case "create":
					createLst(operands)
				case "delete":
					deleteLst(operands)
				case "rename":
					renameLst(operands)
				case _:
					err()
					return 1
		case "task":
			match operation:
				case "create":
					createTask(operands)
				case "delete":
					deleteTask(operands)
				case "rename":
					renameTask(operands)
				case "checkoff":
					checkOffTask(operands)
				case _:
					err()
					return 1
		case "subtask":
			match operation:
				case "create":
					createSubTask(operands)
				case "delete":
					deleteSubTask(operands)
				case "rename":
					renameSubTask(operands)
				case "checkoff":
					checkOffSubTask(operands)
				case _:
					err()
					return 1
		case "help":
			showManual()
		case "exit":
			print("Program closing...")
			global db
			db.close()
			quit()
		case _:
			err()
			return 1

#Print all the tasks
def showTasks():
	global db	
	cursor = db.cursor()
	#Get all lists and their ids
	cursor.execute("SELECT lst_name, id FROM lsts")
	lsts = cursor.fetchall()

	print("------------------------------------------")
	print("-------------MY TODO LIST-----------------")
	print("------------------------------------------")
	for i in range(len(lsts)):
		#Print each list name
		print("|-----------------|")
		print("| LIST: " + lsts[i][0] + "   |")
		print("|-----------------|")
		#get all the tasks and their ids
		cursor.execute("SELECT task_name, task_isDone, id FROM tasks WHERE lst_id = ?", (lsts[i][1],))
		tsks = cursor.fetchall()
		for j in range(len(tsks)):
			#Print each task
			#Tasks marked Done are striked through
			if tsks[j][1] == "YES":
				tskString = strike(tsks[j][0] + " | DONE? " + tsks[j][1])
			else:
				tskString = tsks[j][0] + " | DONE? " + tsks[j][1]
			print("|	TASK: " + tskString + " |")
			#get all the subtasks
			cursor.execute("SELECT subtask_name, subtask_isDone FROM subtasks WHERE task_id = ?", (tsks[j][2],))
			subTsks = cursor.fetchall()
			for k in range(len(subTsks)):
				#Print each subtask
				#Tasks marked Done are striked through
				if subTsks[k][1] == "YES":
					subTskString = strike(subTsks[k][0] + " | DONE? " + subTsks[k][1])
				else:
					subTskString = subTsks[k][0] + " | DONE? " + subTsks[k][1]
				print("|		SUBTASK: " + subTskString + " |")
		
	print("|-----------------|")
	print("------------------------------------------")

#Generate an ID for database entries
def generateID():
	result = ""
	for index in range(8):
		result += str(random.randint(0, 9))
	return result

#Strike through a text
def strike(text):
    result = ''
    for character in text:
        result = result + character + '\u0336'
    return result

#Send error
def err():
	print("Error. Something went wrong. Try again...")

#==================================

#===========DATABASE FUNCTIONS=======================

#===========TASK LIST FUNCTIONS=======================

def createLst(operands):
	global db
	lstName = operands[0]
	values = (generateID(), lstName)
	try:
		db.execute('INSERT INTO lsts(id, lst_name) VALUES(?, ?)', values)
		db.commit() 
		print("NEW LIST CREATED!")
	except Error:
		print(Error)
		err()
		return 1

def deleteLst(operands):
	global db
	lstName = operands[0]
	try:
		db.execute('DELETE FROM lsts WHERE lst_name = ?', (lstName,))
		db.commit() 
		print("LIST DELETED!")
	except Error:
		print(Error)
		err()
		return 1

def renameLst(operands):
	global db
	lstName = operands[0]
	newName = operands[1]
	values = (newName, lstName)
	try:
		db.execute('UPDATE lsts SET lst_name = ? WHERE lst_name = ?', values)
		db.commit() 
		print("LIST RENAMED!")
	except Error:
		print(Error)
		err()
		return 1

#Find the id of a list by name
#Returns id
def findIdList(lstName):
	global db
	cursor = db.cursor()
	cursor.execute('SELECT id FROM lsts WHERE lst_name = ?', (lstName,))
	result = cursor.fetchone()
	return result[0]

#==================================

#===========TASK FUNCTIONS=======================

def createTask(operands):
	global db
	taskName = operands[0]
	lstName = operands[1]
	values = (generateID(), taskName, "NO", findIdList(lstName))	
	try:
		db.execute('INSERT INTO tasks(id, task_name, task_isDone, lst_id) VALUES(?, ?, ?, ?)', values)
		db.commit() 
		print("TASK CREATED!")
	except Error:
		print(Error)
		err()
		return 1

def deleteTask(operands):
	global db
	taskName = operands[0]
	try:
		db.execute('DELETE FROM tasks WHERE task_name = ?', (taskName,))
		db.commit() 
		print("TASK DELETED!")
	except Error:
		print(Error)
		err()
		return 1

def renameTask(operands):
	global db
	taskName = operands[0]
	newName = operands[1]
	values = (newName, taskName)
	try:
		db.execute('UPDATE tasks SET task_name = ? WHERE task_name = ?', values)
		db.commit() 
		print("TASK RENAMED!")
	except Error:
		print(Error)
		err()
		return 1

def checkOffTask(operands):
	global db
	taskName = operands[0]
	try:
		db.execute('UPDATE tasks SET task_isDone = "YES" WHERE task_name = ?', (taskName,))
		db.commit() 
		print("TASK MARKED COMPLETE!")
	except Error:
		print(Error)
		err()
		return 1

#Find the id of a task by name in a task list
#Returns id
def findIdTask(taskName, lstName):
	global db
	list_id = findIdList(lstName)
	cursor = db.cursor()
	cursor.execute('SELECT id FROM tasks WHERE task_name = ? AND lst_id = ?', (taskName, list_id))
	result = cursor.fetchone()
	return result[0]

#==================================

#===========SUB TASK FUNCTIONS=======================

def createSubTask(operands):
	global db
	subTaskName = operands[0]
	taskName = operands[1]
	lstName = operands[2]
	values = (generateID(), subTaskName, "NO", findIdTask(taskName, lstName))	
	try:
		db.execute('INSERT INTO subtasks(id, subtask_name, subtask_isDone, task_id) VALUES(?, ?, ?, ?)', values)
		db.commit() 
		print("SUB TASK CREATED!")
	except Error:
		print(Error)
		err()
		return 1

def deleteSubTask(operands):
	global db
	subTaskName = operands[0]
	try:
		db.execute('DELETE FROM subtasks WHERE subtask_name = ?', (subTaskName,))
		db.commit() 
		print("SUB TASK DELETED!")
	except Error:
		print(Error)
		err()
		return 1

def renameSubTask(operands):
	global db
	subTaskName = operands[0]
	newName = operands[1]
	values = (newName, subTaskName)
	try:
		db.execute('UPDATE subtasks SET subtask_name = ? WHERE subtask_name = ?', values)
		db.commit()
		print("SUB TASK RENAMED!")
	except Error:
		print(Error)
		err()
		return 1

def checkOffSubTask(operands):
	global db
	subTaskName = operands[0]
	try:
		db.execute('UPDATE subtasks SET subtask_isDone = "YES" WHERE subtask_name = ?', (subTaskName,))
		db.commit() 
		print("TASK MARKED COMPLETE!")
	except Error:
		print(Error)
		err()
		return 1

#==================================

#===========PROGRAM FUNCTIONS=======================

def startProgram():
	print("Py To-Do List Copyright (C) 2022 Stephanus Koopmanschap\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it under certain conditions.") 
	print("Build Version: 1.0.0 Stable\n\n")

	while True: #Infinite loop
		showTasks()
		getUserInput()

#Create connection with the database
db = sqlite3.connect(databaseFile)
startProgram()

#Create connection with the database
# try:
# 	db = sqlite3.connect(databaseFile)
# 	startProgram()
# except Error:
# 	print("ERROR: Database file " + databaseFile + " not found.")

#Close db connection
db.close()

#==================================
