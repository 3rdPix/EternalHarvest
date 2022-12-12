class Requests:

    @staticmethod
    def log_in(user_info) -> dict:
        return {
            "request": 0,
            "username": user_info.get('username'),
            "password": user_info.get('password'),
        }
