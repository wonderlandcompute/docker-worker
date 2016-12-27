from .base import BackendBase


class NoneBackend(BackendBase):
    def copy_from_backend(self, src_path, dst_path):
        pass

    def copy_to_backend(self, src_path, dst_path):
        pass

    def list_uploaded(self, path):
        return []
