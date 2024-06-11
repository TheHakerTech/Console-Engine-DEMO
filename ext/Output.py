class Output():
    @staticmethod
    def print(text) -> None:
        with open("data/output.txt", "a") as file:
            file.write(text)