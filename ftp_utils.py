from ftplib import FTP, Error
import os


class FTP_UTILS(FTP):
    
    def __init__(self, ftp_address: str, user: str, password: str, directory: str):
        super(FTP_UTILS, self).__init__(ftp_address, user, password)
        self.encoding = "utf-8"
        self.directory = directory

    def download_all_files(self, list_of_file_names: list):
        for name in list_of_file_names:
            with open(f"{os.getcwd()}\\{name}", "wb") as file:
                self.retrbinary(f"RETR {name}", file.write)

    def upload_all_files(self, list_of_file_names: list):
        try:
            self.cwd(self.directory)
        except Error:
            self.mkd(self.directory)
            self.cwd(self.directory)
        for name in list_of_file_names:
            with open(f"{os.getcwd()}\\tmp\\{name}") as file:
                self.storbinary(f"STOR {name}", file)

    def delete_all_files_in_directory(self):
        self.cwd(self.directory)
        for file in self.nlst():
            self.delete(file)

