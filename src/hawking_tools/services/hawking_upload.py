#!/usr/bin/env python3

from pathlib import Path

import requests

from hawking_tools.services import hawking_tasks

api_base = "https://hawking.computing.dcu.ie/api"
upload_url = api_base + "/upload"
tasks_path = api_base + "/tasks"


def upload_file(authenticated_session, file):
	with open(file, "rb") as file_handle:
		file_upload = {"file": file_handle}
		
		module = hawking_tasks.get_module_from_task(authenticated_session, file)

		filename = Path(file).name

		try:
			request = authenticated_session.post(f"{upload_url}/{module}/{filename}", files=file_upload, timeout=10)
			print(request.json())
			hawking_tasks.display_task_info(request.text)
		except requests.exceptions.ReadTimeout:
			print(f"Request timed out while uploading {filename}. Try again.")
			return

	if request.status_code == 200:
		print(f"Successfully uploaded {filename}!")


def bulk_upload(authenticated_session, files):
	for file in files:
		upload_file(authenticated_session, file)
