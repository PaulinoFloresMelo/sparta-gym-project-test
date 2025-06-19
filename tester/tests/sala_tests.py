import pytest
import requests
from data import dictionaries_sala
from services.status_code import Status
from config import settings


@pytest.mark.critical
def test_get_all_salas():
    response = requests.get( settings.BASE_URL + 'api/salas/', timeout=1)
    Status.status_code_ok(response)


@pytest.mark.critical
def test_post_sala():
    sala_data = dictionaries_sala.sala_data
    response = requests.post(settings.BASE_URL + 'api/salas/', json=sala_data, timeout=1)
    Status.status_code_created(response)


@pytest.mark.critical
def test_put_sala():
    put_sala = dictionaries_sala.put_sala_data
    # Assuming the sala with id 16 exists for update
    response = requests.put(settings.BASE_URL + 'api/salas/14/', json=put_sala, timeout=1)
    Status.status_code_ok(response)


@pytest.mark.critical
def test_delete_sala():
    # Assuming the sala with id 20 exists for deletion
    response = requests.delete(settings.BASE_URL + 'api/salas/23/', timeout=1)
    Status.status_code_delete(response)
