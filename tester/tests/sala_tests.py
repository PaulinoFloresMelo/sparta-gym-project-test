import pytest
import requests
from data import url
from data import dictionaries_sala


@pytest.mark.critical
def test_get_all_salas():
    response = requests.get( url.BASE_URL + '/salas/', timeout=1)
    assert response.status_code == 200


@pytest.mark.critical
def test_post_sala():
    sala_data = dictionaries_sala.sala_data
    response = requests.post(url.BASE_URL + '/salas/', json=sala_data, timeout=1)
    assert response.status_code == 201


@pytest.mark.critical
def test_put_sala():
    put_sala = dictionaries_sala.put_sala_data
    # Assuming the sala with id 16 exists for update
    response = requests.put(url.BASE_URL + '/salas/15/', json=put_sala, timeout=1)
    assert response.status_code == 200


@pytest.mark.critical
def test_delete_sala():
    # Assuming the sala with id 20 exists for deletion
    response = requests.delete(url.BASE_URL + '/salas/21/', timeout=1)
    assert response.status_code == 204
