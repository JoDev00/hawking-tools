#!/usr/bin/env python3

import base64
import json
from pathlib import Path

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import guess_lexer
from termcolor import cprint

from hawking_tools.core import hawking_state

api_base = "https://hawking.computing.dcu.ie/api"
module_for_task = api_base + "/moduleForTask"
tasks_url = api_base + "/tasks" # finds tasks for every module


def select_module_from_task(module_id):
	for i, module in enumerate(module_id):
		print(f"{i + 1}. {module['banner']} (ID: {module['id']})")
	while True:
		selected_index = input("Enter the number of the correct module: ")
		if selected_index.isdigit() and 1 <= int(selected_index) <= len(module_id):
			return module_id[int(selected_index) - 1]["id"]
		else:
			print("Invalid selection. Please try again.")

def get_module_from_task(authenticated_session, task):
	module_id = authenticated_session.get(f"{module_for_task}/{Path(task).name}").json()

	if hawking_state.get_current_module(authenticated_session.auth[0]) is not None:
		current_module = hawking_state.get_current_module(authenticated_session.auth[0])
		for module in module_id:
			if module["banner"] == current_module:
				return module["id"]
		print(f"Current module '{current_module}' does not match any modules for {task}. Please select the correct module from the following list:")
		return select_module_from_task(module_id)

	if len(module_id) > 1:
		print(f"Multiple modules found for {task}. \n Please select the correct module from the following list:")
		return select_module_from_task(module_id)
	elif len(module_id) == 1:
		return module_id[0]["id"]
	else:
		print(f"No module found for {task}. Please check the task name and try again.")
		return None


def display_task_info(response):
	data = json.loads(response)["output"]
	script = data["attempt"]["source"]
	highlighted_script = highlight(script, guess_lexer(script), TerminalFormatter(style="monokai"))
	print(f"\n{highlighted_script}\n")

	for test, result in zip(data["tests"], data["results"]):
		args = base64.b64decode(test["args"]).decode("utf-8").strip().replace("\n", " ")
		correct = result["correct"]
		color = "green" if correct else "red"

		print("-" * 30)
		cprint(f"{test['name']} | {args}", color)
		cprint(f"expected stdout: {test['expectedStdout'].strip()}", color)
		cprint(f"actual stdout: {result['stdout'].strip()}", color)
		cprint(f"stderr: {result['stderr'].strip()}", color)
		print("-" * 30)

def get_tasks(auth_session):
	response = auth_session.get(tasks_url, timeout=10)
	if response.status_code != 200:
		print(f'Error fetching tasks: {response.reason}')
		return None
	
	data = response.json()
	if isinstance(data, dict) and "error" in data:
		print(f'Error fetching tasks: {data['error']}')
		return None
	
	return set(data)

def get_latest_file(auth_session, directory="."):
	tasks = get_tasks(auth_session)
	if tasks is None:
		return None

	candidates = [p for p in Path(directory).iterdir() if p.is_file() and p.name in tasks]
	if not candidates:
		print("You have no tasks in this folder to upload")
		return None
	
	return max(candidates, key=lambda p: p.stat().st_mtime)
	
