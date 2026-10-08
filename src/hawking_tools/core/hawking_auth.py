#!/usr/bin/env python3

import requests
import keyring
from getpass import getpass


def get_password(username):
	return keyring.get_password("hawking-tools", username) or getpass("Password: ")


def get_username():
	credential = keyring.get_credential("hawking-tools", None)

	if credential:
		return credential.username

	return input("⋆˚｡ Username: ").strip()


def set_password(username, password):
	keyring.set_password("hawking-tools", username, password)


def authentication_flow(username, password):
	while not is_valid_login(username, password):
		print("Invalid username or password. Please try again.")
		username = input("⋆˚｡ Username: ").strip()
		password = getpass("Password: ")

	keyring.set_password("hawking-tools", username, password)
	print("Logged in as: ", username)


def is_valid_login(username, password):
	auth_check = requests.get("https://hawking.computing.dcu.ie/api/auth", timeout=10, auth=(username, password))

	return auth_check.status_code == 200

def logout(username):
	keyring.delete_password("hawking-tools", username)
	print(f"Logged out {username} successfully.")

def get_authenticated_session(username, password):
	session = requests.Session()
	session.auth = (username, password)
	return session
