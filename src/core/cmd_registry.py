#!/usr/bin/env python3

commands = {}

def command(function):
	commands[function.__name__]	= function
	return function
