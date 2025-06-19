import requests

class Status:

    @staticmethod
    def status_code_ok(response: requests.Response) -> None:
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"


    @staticmethod
    def status_code_created(response: requests.Response) -> None:
        assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"

    @staticmethod
    def status_code_delete(response: requests.Response) -> None:
        assert response.status_code == 204, f"Expected status code 204, got {response.status_code}"