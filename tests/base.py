import logging
import os
import shutil

from tvrenamr.config import Config
from tvrenamr.main import File, TvRenamr


logging.disable(logging.CRITICAL)


class BaseTest(object):
    def setup(self):
        # absolute path to the file is pretty useful
        self.path = os.path.abspath(os.path.dirname(__file__))

        def build_path(path):
            if not os.path.exists(path):
                os.mkdir(path)

            return path

        def join_path(path):
            return os.path.join(self.path, path)

        self.files = build_path(join_path('files'))
        self.subfolder = build_path(join_path('subfolder'))
        self.organised = build_path(join_path('organised'))
        self.renamed = join_path('renamed')

        for path in (self.files, self.subfolder):
            self.build_files(path)

        # instantiate tvr
        self.config = Config()
        self.config.config['defaults']['renamed'] = self.files
        self.tv = TvRenamr(self.files, self.config, cache=False)

        self._file = File('The Big Bang Theory', '3', ['01'], '.mp4')
        self._file.episodes[0].title = 'The Electric Can Opener Fluctuation'

    def teardown(self):
        shutil.rmtree(self.files)
        shutil.rmtree(self.subfolder)

    def build_files(self, path):
        """Build the file list"""
        with open(os.path.join(self.path, 'file_list'), 'r') as f:
            for fn in f.readlines():
                filepath = os.path.abspath(os.path.join(path, fn.strip()))
                with open(filepath, 'w') as f:
                    f.write('')
