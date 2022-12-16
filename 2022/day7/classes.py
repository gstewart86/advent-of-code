import sys
import logging

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class Inode:
    def __init__(self, path: str, name: str, inode_type: str, size: int):
        self.path = path
        self.name = name
        self.inode_type = inode_type
        self.size = size

        if self.name == "/":
            self.fqdn = "/"
        else:
            self.fqdn = str(self.path) + self.name if self.name else str(self.path)

    def __repr__(self):
        return f"inode({str(self.path)}, {self.name}, {self.inode_type}, {self.size})"

    def __str__(self) -> str:
        return f"{self.fqdn}" if self.name != "/" else "/"


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

        # expand path argument
        if "path" in inode_params:
            inode_params["path"] = Path(inode_params["path"])

        for node in self.inodes:
            if all(
                node.__dict__.get(key, None) == val for key, val in inode_params.items()
            ):
                found_inodes.append(node)
        return sorted(
            sorted(found_inodes, key=lambda x: x.inode_type),
            key=lambda x: x.size,
            reverse=True,
        )

    def add_inode(self, inode):
        self.inodes.append(inode)


class Path(list):
    """Describes list of inodes present in path to file

    Args:
        list (_type_): subclass of list
    """

    def __init__(self, path=[]):
        """generate a path object.
        If path is a string, it will be split on '/' and converted to a list.
        Ensures the path does not contain spaces.
        An empty list represents the root directory.

        Args:
            path (list, optional): list of inodes. Defaults to [].

        Raises:
            ValueError: _description_
        """
        if " " in path:
            raise ValueError(f"Path cannot contain spaces: {path}")

        if path == "/":
            path = []
        elif isinstance(path, str):
            path = path.split("/")

        path = [node for node in path if node != ""]

        super().__init__(path)

    def __str__(self):
        path = self
        if self == []:
            path = "/"
        elif self == ["/"]:
            path = "/"
        else:
            path = "/" + "/".join(self)
        return path


class Bash:
    def __init__(self, filesystem):
        self.filesystem = filesystem
        self.pwd = Path("/")
        self.oldpwd = self.pwd

    def __repr__(self):
        return f"Bash({self.pwd})"

    @property
    def prompt(self):
        return f"{str(self.pwd)} > "

    def _get_path(self, inode):
        path = []
        while inode.path != self.filesystem.root.name:
            path.append(inode.name)
            inode = self.filesystem.find_inode({"path": inode.path})
        path.append(inode.name)
        return "/".join(path[::-1])

    def ls(self, path=None, recursive=False):
        if not path:
            path = self.pwd
        logger.debug(
            f"looking up files in {str(path)}{', recursively' if recursive else ''}"
        )
        found_inodes = self.filesystem.find_inodes({"path": str(path)})
        if recursive:
            for node in found_inodes:
                if node.inode_type == "dir":
                    found_inodes.extend(self.ls(node.fqdn, recursive=True))
        if not recursive:
            logger.info(
                f"nodes found': {[(str(node), node.size) for node in found_inodes]}"
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

    def du(self, path=None, recursive=False):
        # Determine Path, sanitize input
        if path is None:
            path = str(self.pwd)
        # Gather sizes, recursively if all=True
        logger.debug(
            f"Calculating size of {str(path)} {', recursively' if recursive else ''})"
        )
        total_size = 0
        if recursive:
            logger.debug(
                f"  Starting recursive size calculation",
            )
            inodes = self.ls(path, recursive=recursive)
            for inode in inodes:
                total_size += inode.size
        else:
            inodes = self.ls(path)
            total_size += sum([node.size for node in inodes])
        return total_size
