import logging
from io import StringIO

import lasio


class LasClientException(BaseException):
    pass


class LasFileReadError(LasClientException):
    pass


class LasFileWriteError(LasClientException):
    pass


class LasClient:
    decode_formats = ["ascii", "utf-8", "windows-1252"]
    sensitive_mnemonics = [
        "COMP",
        "WELL",
        "FLD",
        "LOC",
        "PROV",
        "STAT",
        "CNTY",
        "CTRY",
        "DATE",
        "UWI",
        "LIC",
        "API",
        "SRVC",
    ]

    def __init__(self, las_file: bytes):
        self.file_bytes = las_file
        self.file = self._read_file(las_file)

    def _read_file(self, las_file: bytes) -> lasio.LASFile:
        """
        Read las file.
        """
        decoded_las = self._decode_file(las_file)
        if decoded_las:
            try:
                las_file = lasio.read(
                    decoded_las,
                    ignore_header_errors=False,
                    autodetect_encoding_chars=None,
                    mnemonic_case="preserve",
                )
                return las_file
            except (KeyError, IndexError) as exc:
                logging.exception(exc)
                raise LasFileReadError(str(exc)) from exc

    def _decode_file(self, las_file: bytes) -> str:
        """
        Decode las file.
        """
        for decode_format in self.decode_formats:
            try:
                decoded_las = las_file.decode(decode_format)
                return decoded_las
            except UnicodeDecodeError:
                continue

    def remove_sensitive_mnemonics_data(self) -> lasio.LASFile:
        """
        Removes all sensitive data from las file.
        """
        for mnemonic in self.sensitive_mnemonics:
            if mnemonic in self.file.well:
                self.file.well[mnemonic] = self.file.well[mnemonic].clear()
        return self.file

    def insert_sensitive_mnemonics_data_from_file(
        self, source_file: bytes
    ) -> lasio.LASFile:
        """
        Insert all sensitive data from source las file to current.
        """
        source = self._read_file(source_file)
        for mnemonic in self.sensitive_mnemonics:
            if mnemonic in source.well:
                self.file.well[mnemonic] = source.well[mnemonic]
        return self.file

    def get_file_data(self) -> str:
        """
        Create file-like object to have an ability to upload or download file data.
        """
        try:
            output = StringIO()
            lasio.writer.write(self.file, output)
            output.seek(0)
            return output.read()
        except (KeyError, IndexError) as exc:
            raise LasFileWriteError(str(exc)) from exc
