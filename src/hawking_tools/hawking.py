#!/usr/bin/env python3

import sys
import time
from pathlib import Path

from .core import hawking_auth
from .services import hawking_upload
from .core import hawking_state

def main():
	username = hawking_auth.get_username()
	password = hawking_auth.get_password(username)
	hawking_auth.authentication_flow(username, password)
	authenticated_session = hawking_auth.get_authenticated_session(username, password)

	print("To view available commands, type 'help'.")

	while True:
		user_input = input(". ݁₊ ⊹ . ݁ Enter a command: ")
		if user_input == "exit":
			sys.exit()

		command = user_input.split(" ")[0]

		if command == "upload":
			if len(user_input.split(" ")) < 2:
				print("Please provide a file to upload.")
				continue
			files = list(Path(".").glob(user_input.split(" ")[1]))

			if not files:
				print(f"File '{user_input.split(' ')[1]}' not found.")
				continue
			
			hawking_upload.bulk_upload(authenticated_session, files)
			time.sleep(1)
		elif command == "logout":
			hawking_auth.logout(username)
			sys.exit()
		elif command == "module":
			if len(user_input.split(" ")) < 2 and hawking_state.get_current_module(username) is None:
				print("Please provide a module code to set as the current module.")
				continue
			elif len(user_input.split(" ")) < 2:
				current_module = hawking_state.get_current_module(username)
				print(f"Current module: {current_module}")
				continue
			module_code = user_input.split(" ")[1]
			hawking_state.set_current_module(username, module_code)
			print(f"Current module set to {module_code}.")

if __name__ == "__main__":
	main()