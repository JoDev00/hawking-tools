#!/usr/bin/env python3

import requests
import services.hawking_tasks
from pathlib import Path
from core import cmd_registry

api_base = "https://hawking.computing.dcu.ie/api"
upload_url = api_base + "/upload"
tasks_path = api_base + "/tasks"

@cmd_registry.command
def upload(authenticated_session, file):
	file = file[0]
	file_upload = {"file": open(file, "rb")}
	module = services.hawking_tasks.get_module_from_task(authenticated_session, file)

	file = Path(file).name

	print(f"Uploading {file}...")
	try:
		request = authenticated_session.post(f"{upload_url}/{module}/{file}", files=file_upload, timeout=10)
		print(request.text)
		services.hawking_tasks.display_task_info(request.text)
	except requests.exceptions.ReadTimeout:
		print("Request timed out while uploading {file}. Try again.")
		return

	if request.status_code == 200:
		print(f"Successfully uploaded {file}!")

def bulk_upload(authenticated_session, files):
	for file in files:
		upload(authenticated_session, file)