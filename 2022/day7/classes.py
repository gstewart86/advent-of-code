import sys
import logging
from pprint import pformat, pprint
from dataclasses import dataclass
from uuid import uuid1

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


@dataclass
class Inode:
    path: str
    name: str
    inode_type: str
    size: int

    def __repr__(self):
        return f"inode({self.path}, {self.name}, {self.inode_type}, {self.size})"


class FileInode(Inode):
    def __init__(
        self,
        path,
        name,
        size,
    ):
        super().__init__(Path(path), name, "file", size)


class DirInode(Inode):
    def __init__(
        self,
        path,
        name,
        size=0,
    ):
        super().__init__(Path(path), name, "dir", size)


class SuperBlock:
    def __init__(self, inodes=[]):
        self.inodes = [DirInode("/", "/")] + inodes
        self.root = self.inodes[0]

    def __repr__(self):
        return f"super_block({self.inodes})"

    def find_inodes(self, inode_params: dict = {}):
        """Finds Inode objects by a related Inode parameter

        A good way to ensure one dict is a subset of another

        Args:
            inode_params (dict, optional):
            {
                name: 'zfdc',
                path: '/rhrqttg/hmz'
            }

        Raises:
            KeyError: error when inode is not found

        Returns:
            Inode: inode object
        """
        found_inodes = []
        logger.debug(f"Searching for inode with params: {inode_params}")
        for node in self.inodes:
            if all(
                node.__dict__.get(key, None) == val for key, val in inode_params.items()
            ):
                found_inodes.append(node)
        return found_inodes

    def add_inode(self, inode):
        self.inodes.append(inode)

    def inode_children(self, path, name, filter="file", recursive=False):
        tmp_list = []

        if isinstance(name, str):
            inode = self.find_inodes({"name": name})

        def _find_children(inode):
            for node in self.inodes:
                if node.name == inode:
                    if node.inode_type == filter:
                        if node not in tmp_list:
                            tmp_list.append(node)
                    if recursive:
                        _find_children(node)

        _find_children(name)
        return tmp_list


class Path(list):
    def __init__(self, path=[]):
        if isinstance(path, str) and path != "/":
            path = path.split("/")
        if " " in path:
            raise ValueError(f"Path cannot contain spaces: {path}")
        super().__init__(path)

    def as_string(self):
        return "/".join(self)


class Bash:
    def __init__(self, filesystem):
        self.filesystem = filesystem
        self.pwd = Path("/")
        self.oldpwd = self.pwd

    def __repr__(self):
        return f"Bash({self.pwd})"

    @property
    def prompt(self):
        return f"{self.pwd.as_string()} > "

    def _get_path(self, inode):
        path = []
        while inode.path != self.filesystem.root.name:
            path.append(inode.name)
            inode = self.filesystem.find_inode({"path": inode.path})
        path.append(inode.name)
        return "/".join(path[::-1])

    def ls(self, path=None):
        if not path:
            path = self.pwd
        logger.debug("looking up files in %s", path.as_string())
        found_inodes = self.filesystem.find_inodes({"path": path.as_string()})
        logger.info(
            f"all inodes in '{path.as_string()}': {[node.name for node in found_inodes]}"
        )
        return found_inodes

    def cd(self, path=None):
        self.oldpwd = self.pwd
        if not path:
            path = self.filesystem.root.path
        if path == "/":
            destination_path = Path("/")
        elif path == "..":
            if self.pwd == "/":
                destination_path = self.pwd
            else:
                destination_path = self.pwd[:-1]
        else:
            destination_path = self.pwd + [path]
        logger.info(f"changed from {self.pwd} to {destination_path}")
        self.pwd = Path(destination_path)
        return self.pwd

    def pwd(self):
        print(self.pwd.name)
        return self

    def mkdir(self, dir_name):
        logger.info(f"Creating dir inode: {dir_name}")
        inode = DirInode(self.pwd, dir_name)
        # if inode in self.filesystem.inodes:
        #     print([node for node in self.filesystem.inodes if node.name == dir_name])
        #     raise ValueError(f"Directory {dir_name} already exists")
        self.filesystem.add_inode(inode)
        return self

    def touch(self, file_name, size=0):
        logger.info(f"Creating file inode: {file_name}")
        self.filesystem.add_inode(FileInode(self.pwd, file_name, size))
        return self

    def du(self, inode=None, all=False):
        logger.debug(f"Calculating size of {inode} (all={all}")
        total_size = 0
        if inode is None:
            inode = self.pwd
        if isinstance(inode, str):
            inode = self.filesystem.find_inodes({"path": inode})
        print(inode)
        return total_size
