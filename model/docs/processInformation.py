def read_information(path_file: str) -> str:
    info_file = open(path_file, "r", encoding="utf8", errors="ignore")
    information: str = info_file.read()
    info_file.close()
    return information


def save_information(path_file: str, information: str) -> None:
    info_file = open(path_file, "w", encoding="utf8", errors="ignore")
    info_file.write(information)
    info_file.close()
