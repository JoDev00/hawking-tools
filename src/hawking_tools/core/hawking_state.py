#!/usr/bin/env python3
import keyring

SERVICE = "hawking-tools-state"


def get_current_module(username):
    return keyring.get_password(SERVICE, username)


def set_current_module(username, module_id):
    keyring.set_password(SERVICE, username, str(module_id))


def clear_current_module(username):
    try:
        keyring.delete_password(SERVICE, username)
    except keyring.errors.PasswordDeleteError:
        pass