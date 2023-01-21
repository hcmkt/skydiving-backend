import requests


class Line:
    access_token: str

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    def validate_token(self) -> bool:
        response = requests.get(
            url="https://api.line.me/oauth2/v2.1/verify",
            params={"access_token": self.access_token},
        )
        return response.status_code == 200

    def get_user_id(self) -> int:
        response = requests.get(
            url="https://api.line.me/v2/profile",
            headers={"Authorization": "Bearer " + self.access_token},
        )
        return response.json()["userId"]
