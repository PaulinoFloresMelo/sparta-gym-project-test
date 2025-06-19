import pytest
import requests
from data import dictionaries_membresia
from services.status_code import Status
from config import settings


@pytest.mark.critical
def test_get_all_membresias():
    response = requests.get( settings.BASE_URL + 'api/membresias/', timeout=1)
    Status.status_code_ok(response)


@pytest.mark.critical
def test_post_membresia():
    membresia_data = dictionaries_membresia.membresia_data
    response = requests.post(settings.BASE_URL + 'api/membresias/', json=membresia_data, timeout=1)
    Status.status_code_created(response)


@pytest.mark.critical
def test_put_membresia():
    put_membresia = dictionaries_membresia.put_membresia_data
    # Assuming the mebresia with id exists for update
    response = requests.put(settings.BASE_URL + 'api/membresias/9/', json=put_membresia, timeout=1)
    Status.status_code_ok(response)


@pytest.mark.critical
def test_delete_membresia():
    # Assuming the sala with id exists for deletion
    response = requests.delete(settings.BASE_URL + 'api/membresias/7/', timeout=1)
    Status.status_code_delete(response)


@pytest.mark.normal
def test_renovar_membresia():
    # Assuming the sala with id exists for renewal
    response = requests.put(settings.BASE_URL + 'api/membresias/renovar/9/', timeout=1)
    Status.status_code_ok(response)


@pytest.mark.normal
def test_aplicar_promocion():
    # Assuming the sala with id exists for renewal
    response = requests.put(settings.BASE_URL + 'api/membresias/promocion/9/', timeout=1)
    Status.status_code_ok(response)