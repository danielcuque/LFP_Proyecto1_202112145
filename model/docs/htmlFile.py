from typing import (List, Dict)
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

    def report_of_operations(self, table_of_results: List[Dict]):
        print(table_of_results)


    def report_of_errors(self, table_of_invalid_tokens: List[str]):
        print(table_of_invalid_tokens)

    def create_html_report(self):
        pass

    @staticmethod
    def _is_start_tag_style(token: Token) -> bool:
        return bool(token.get_type_name() == "START_TAG" and "estilo" in token.literal.lower())

    @staticmethod
    def _is_end_tag_style(token: Token) -> bool:
        return bool(token.get_type_name() == "END_TAG" and "estilo" in token.literal.lower())

    @staticmethod
    def _is_start_tag_function(token: Token) -> bool:
        return bool(token.get_type_name() == "START_TAG" and "funcion" in token.literal.lower())

    @staticmethod
    def _is_end_tag_function(token: Token) -> bool:
        return bool(token.get_type_name() == "END_TAG" and "funcion" in token.literal.lower())

    @staticmethod
    def create_file_header() -> str:
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
    def styles_for_document() -> str:
        styles = """
        <style>
            body {
                background-color: #1a1a1a;
                color: #fff;
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
        </style>
        """
        return styles


