#!/usr/bin/env python3

import sys
import hawking_auth
from services import hawking_upload
from pathlib import Path
import time

commands = {}

def command(function):
	commands[function.__name__]	= function
	return function

@command
def test(authenticated_session, *args):
	print(args)

def main():
	username = hawking_auth.get_username()
	password = hawking_auth.get_password(username)
	hawking_auth.authentication_flow(username, password)
	authenticated_session = hawking_auth.get_authenticated_session(username, password)

	cmd = sys.argv[1]
	args = sys.argv[2:]
	commands[cmd](authenticated_session, args)

if __name__ == "__main__":
	main()
