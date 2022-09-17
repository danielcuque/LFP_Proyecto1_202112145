def create_html_file(source: str) -> None:
    with open("index.html", "w") as file:
        file.write(source)
