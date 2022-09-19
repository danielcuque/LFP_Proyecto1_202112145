from typing import (List, Dict)

from tkinter import (
    filedialog
)

from controller.token import Token


class HTMLFile:
    def __init__(self, table_of_tokens: List) -> None:
        self.table_of_tokens: List[Token] = table_of_tokens

        self._table_of_styles: List[Token] = []
        self._table_of_functions: List[Token] = []

        self._capture_tokens_for_styles()
        self._capture_tokens_to_write()

    def _capture_tokens_for_styles(self) -> None:
        open_tag_style = False

        for token in self.table_of_tokens:
            if self._is_start_tag_style(token):
                open_tag_style = True
                self._table_of_styles.append(token)

            if open_tag_style:
                self._table_of_styles.append(token)

            if self._is_end_tag_style(token):
                open_tag_style = False
                self._table_of_styles.append(token)

    def _capture_tokens_to_write(self) -> None:
        open_tag_function = False

        for token in self.table_of_tokens:
            if self._is_start_tag_function(token):
                open_tag_function = True
                self._table_of_functions.append(token)

            if open_tag_function:
                self._table_of_functions.append(token)

            if self._is_end_tag_function(token):
                open_tag_function = False
                self._table_of_functions.append(token)

    def _capture_description_to_write(self) -> str:
        description: str = ""
        open_tag_of_text: bool = False
        for token in self.table_of_tokens:
            if self._is_start_tag_text(token):
                open_tag_of_text = True

            elif open_tag_of_text and token.get_type_name() != "START_TAG" and token.get_type_name() != "CLOSE_TAG":
                description += f'{token.literal} '

            elif self._is_end_tag_text(token):
                return f'<h3>{description}</h3>'

    def _get_title_of_report(self) -> str:
        position = 1
        resp = ""
        open_tag = False

        while len(self._table_of_functions) > position:
            token: Token = self._table_of_functions[position]

            if self._is_start_tag_title(token):
                open_tag = True

            elif open_tag and token.get_type_name() != "CLOSE_TAG":
                resp += f'<h1> {token.literal} </h1>'

            elif self._is_end_tag_title(token):
                return resp
            position += 1

    @staticmethod
    def _get_content(table_of_operations: List[Dict]):
        res = "<div class='operacion'>"

        for item in table_of_operations:
            res += f'<p>{item["TIPO"]}</p>' \
                   f'<p>{item["OPERACION"]} = {item["RESULTADO"]}'

        return f'{res}</div>'

    def report_of_operations(self, table_of_operations: List[Dict]) -> str:
        res = ""

        for item in self._table_of_functions:
            if self._is_start_tag_title(item):
                res += self._get_title_of_report()

            elif item.get_type_name() == "START_TAG" and "descripcion" in item.literal.lower():
                res += self._capture_description_to_write()

            elif item.get_type_name() == "START_TAG" and "contenido" in item.literal.lower():
                res += self._get_content(table_of_operations)

        return res

    def report_of_errors(self, table_of_invalid_tokens: List[str]):
        print(table_of_invalid_tokens)

    @staticmethod
    def _get_header() -> str:
        header = """
             <!DOCTYPE html>
             <html lang="en">
             <head>
                 <meta charset="UTF-8" />
                 <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                 <title>Resultado de operaciones</title>
             </head>
             """

        return header

    @staticmethod
    def _get_attributes(token: Token) -> str:
        pass

    def _get_styles(self) -> str:
        style_title = ""
        style_description = ""
        style_content = ""

        styles = """
         <style>
             * {
                 padding: 0;
                 margin: 0;
                 box-sizing: border-box;
             }
             body {
                 padding: 2rem;
                 font-family: "Karla", sans-serif;
                 background-color: #e5eff5;
             }

             h1  {
                 font-size: 20px;
                 color: red;
             }
             
             h3  {
                 font-size: 12px;
                 color: green;
             }
             table {
                 border-collapse: collapse;
                 width: 100%;
             }
             th, td {
                 text-align: left;
                 padding: 8px;
             }
             tr:nth-child(even){background-color: #f2f2f2}
             th {
                 background-color: #4CAF50;
                 color: white;
             }
             
             .operacion {
                 font-size: 3px;
                 color: gray;
             }
         </style>
         """
        return styles

    def create_html_report(self, table_of_operations: List[Token]):
        report = f'{self._get_header()}' \
                 f'{self._get_styles()}' \
                 f'<body>' \
                 f'{self.report_of_operations(table_of_operations)}' \
                 f'</body>' \
                 f'</html>' \

        path_file = filedialog.askdirectory()
        name_file = "RESULTADOS_202112145"

        file = open(f'{path_file}/{name_file}.html', "w")
        file.write(report)
        file.close()

    @staticmethod
    def _is_start_tag_style(token: Token) -> bool:
        return bool(token.get_type_name() == "START_TAG" and "estilo" in token.literal.lower())

    @staticmethod
    def _is_end_tag_style(token: Token) -> bool:
        return bool(token.get_type_name() == "CLOSE_TAG" and "estilo" in token.literal.lower())

    @staticmethod
    def _is_start_tag_function(token: Token) -> bool:
        return bool(token.get_type_name() == "START_TAG" and "funcion" in token.literal.lower())

    @staticmethod
    def _is_start_tag_text(token: Token) -> bool:
        return bool(token.get_type_name() == "START_TAG" and "texto" in token.literal.lower())

    @staticmethod
    def _is_end_tag_function(token: Token) -> bool:
        return bool(token.get_type_name() == "CLOSE_TAG" and "funcion" in token.literal.lower())

    @staticmethod
    def _is_end_tag_text(token: Token) -> bool:
        return bool(token.get_type_name() == "CLOSE_TAG" and "texto" in token.literal.lower())

    @staticmethod
    def _is_start_tag_title(token: Token) -> bool:
        return bool(token.get_type_name() == "START_TAG" and "titulo" in token.literal.lower())

    @staticmethod
    def _is_end_tag_title(token: Token) -> bool:
        return bool(token.get_type_name() == "CLOSE_TAG" and "titulo" in token.literal.lower())
