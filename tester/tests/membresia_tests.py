import pytest
import requests
from data import url
from data import dictionaries_membresia


@pytest.mark.critical
def test_get_all_membresias():
    response = requests.get( url.BASE_URL + '/membresias/', timeout=1)
    assert response.status_code == 200


@pytest.mark.critical
def test_post_membresia():
    membresia_data = dictionaries_membresia.membresia_data
    response = requests.post(url.BASE_URL + '/membresias/', json=membresia_data, timeout=1)
    assert response.status_code == 201


@pytest.mark.critical
def test_put_membresia():
    put_membresia = dictionaries_membresia.put_membresia_data
    # Assuming the mebresia with id exists for update
    response = requests.put(url.BASE_URL + '/membresias/4/', json=put_membresia, timeout=1)
    assert response.status_code == 200


@pytest.mark.critical
def test_delete_membresia():
    # Assuming the sala with id exists for deletion
    response = requests.delete(url.BASE_URL + '/membresias/6/', timeout=1)
    assert response.status_code == 204


@pytest.mark.critical
def test_renovar_membresia():
    # Assuming the sala with id exists for deletion
    response = requests.put(url.BASE_URL + '/membresias/renovar/4/', timeout=1)
    assert response.status_code == 200

@pytest.mark.critical
def test_aplicar_promocion():
    renovar_membresia = dictionaries_membresia.renovar_membresia_data
    # Assuming the sala with id exists for deletion
    response = requests.put(url.BASE_URL + '/membresias/promocion/3/', timeout=1)
    assert response.status_code == 200