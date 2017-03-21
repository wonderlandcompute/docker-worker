from sh import xrdfs, xrdcopy
from .base import BackendBase


class XrootdBackend(BackendBase):
    def __init__(self, xrd_server, backend_suffix=""):
        self.xrd_server = xrd_server
        self.suffix = backend_suffix

    def copy_from_backend(self, src_path, dst_path):
        xrdcopy("-r", self.xrd_server + src_path, dst_path)

    def copy_to_backend(self, src_path, dst_path):
        xrdfs(self.xrd_server, "mkdir", "-p", dst_path)
        xrdcopy("-f", "-r", src_path, self.xrd_server + dst_path + self.suffix)

    def list_uploaded(self, path):
        files = xrdfs(self.xrd_server, "ls", path).split("\n")
        return filter(None, files)
