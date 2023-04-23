from svn import local, remote
import os
import logging


class SVN_UTILS:

    def __init__(self, svn_url: str, user: str, password: str, directory: str):
        self.directory = directory
        self.svn_url = svn_url
        self.user = user
        self.password = password
        self.checkout_svn()
        self.local_svn = local.LocalClient(self.directory, username=self.user, password=self.password)

    def checkout_svn(self):
        """
        checkout of remote svn to local
        :return:
        """
        try:
            os.system(f'rm -rf {self.directory}')
        except FileNotFoundError:
            pass

        # remote svn checkout
        logging.debug(f"current directory: {os.getcwd()}")
        os.mkdir(f"{self.directory}")
        logging.debug(os.listdir(os.getcwd()))
        r = remote.RemoteClient(self.svn_url, username=self.user, password=self.password)
        r.checkout(f"{self.directory}")

    def clear_svn(self):
        """
        delete all saved reference screenshots for microservice
        :return:
        """
        os.system(f"svn remove --force {self.directory}/*")
        self.local_svn.commit(f"removed old screenshots")
        self.local_svn.update()

    def add_files(self, files: list):
        """
        Adding all files from list to svn ass reference
        :param files: list of strings with names of files
        :return:
        """
        for file in files:
            self.local_svn.add(file)
        self.local_svn.commit(f"files added")
