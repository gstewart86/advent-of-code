import sys
import logging
from typing import Union

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
            self.abspath = Path("/")
        elif name:
            self.abspath = Path(str(self.path) + "/" + self.name)
        else:
            self.abspath = Path(self.path)

    def __repr__(self):
        return f"inode({str(self.path)}, {self.name}, {self.inode_type}, {self.size})"

    def __str__(self) -> str:
        return f"{self.abspath}" if self.name != "/" else "/"


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

    def find_inodes(self, inode_params: dict = {}, ignore_root: bool = True):
        """Finds Inode objects by a related Inode parameter

        A good way to ensure one dict is a subset of another

        Args:
            inode_params (dict, optional):
            {
                name: 'zfdc',
                path: '/rhrqttg/hmz'
            }
            ignore_root: bool = True (default) - ignore root directory in results
                necessary to avoid infinite recursion in some cases

        Raises:
            KeyError: error when inode is not found

        Returns:
            Inode: inode object
        """
        found_inodes = []
        logger.debug(f"find_inodes - Searching for inode with params: {inode_params}")

        if not isinstance(inode_params, dict):
            raise TypeError(f"inode_params must be a dict, not {type(inode_params)}")

        # expand path argument
        if "path" in inode_params:
            inode_params["path"] = Path(inode_params["path"])
        if "abspath" in inode_params:
            inode_params["abspath"] = Path(inode_params["abspath"])

        for node in self.inodes:
            if all(
                node.__dict__.get(key, None) == val for key, val in inode_params.items()
            ):
                found_inodes.append(node)

        # Handle root directory return
        # i.e., it usually shouldn't be.
        if ignore_root and found_inodes and self.root in found_inodes:
            found_inodes.remove(self.root)

        logger.debug(f"find_inodes - Found {len(found_inodes)} inodes")
        return sorted(
            sorted(found_inodes, key=lambda x: x.inode_type),
            key=lambda x: x.size,
            reverse=True,
        )

    def add_inode(self, inode):
        self.inodes.append(inode)
        return inode


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

        if isinstance(path, list):
            pass
        elif isinstance(path, Path):
            path = path.copy()
        elif isinstance(path, Inode):
            path = path.path.copy()
        elif path == "/":
            path = ["/"]
        elif isinstance(path, str):
            path = path.split("/")

        # ensure the first empty element is a slash
        if path:
            if path[0] == "":
                path[0] = "/"

        # lastly remove all empty strings
        path = [node for node in path if node != ""]
        super().__init__(path)

    def __str__(self):
        path = self
        if self == []:
            path = "/"
        else:
            # join the parts, removing any duplicate slashes
            # I tried a regex here like so:
            #    path = re.sub(r"(.)\1{2,}", r"\1\1", path)
            # But extra slashes remained, dont know why.
            path = "/".join(self)
            path = path.replace("///", "/")
            path = path.replace("//", "/")
        return path

    def abspath(self):
        return Path(str(self))


class Bash:
    def __init__(self, filesystem):
        self.filesystem: SuperBlock = filesystem
        self.pwd: Union(DirInode | None) = None
        self.oldpwd: DirInode = self.pwd

        try:
            self.pwd = self.filesystem.root
        except IndexError:
            self.mkdir("/")
            self.pwd = self.filesystem.root

    def __repr__(self):
        return f"Bash({self.pwd.abspath})"

    @property
    def prompt(self):
        return f"{str(self.pwd.abspath)} > "

    def ls(self, path=None, recursive=False):
        if not path:
            path = self.pwd
        logger.debug(
            f"ls - looking up files in {str(path)}{', recursively' if recursive else ''}"
        )
        if isinstance(path, str):
            path = self.find(path)
        found_inodes = self.filesystem.find_inodes({"path": path.abspath})
        if recursive:
            for node in found_inodes:
                if node.inode_type == "dir":
                    found_inodes.extend(self.ls(node.abspath, recursive=True))
        if not recursive:
            logger.info(
                f"  nodes found': {[(str(node), node.size) for node in found_inodes]}"
            )

        return found_inodes

    def cd(self, path=None):
        self.oldpwd = self.pwd
        logger.info(f"changing from {self.oldpwd.abspath} to {path}")
        match path:
            case None | "/":
                self.pwd = self.filesystem.root
            case "..":
                if self.pwd.name == "/":
                    self.pwd = self.filesystem.root
                else:
                    self.pwd = self.find(self.pwd.path)
            case "-":
                self.pwd = self.oldpwd
            case _:
                self.pwd = self.find(str(self.pwd.abspath) + "/" + path)
        return self.pwd

    def pwd(self):
        print(self.pwd.name)
        return self

    def mkdir(self, dir_name):
        logger.info(f"mkdir - Creating dir inode: {dir_name}")
        inode = DirInode(self.pwd.abspath, dir_name)
        if self.filesystem.find_inodes({"path": inode.abspath}):
            raise ValueError(f"Directory {dir_name} already exists")
        self.filesystem.add_inode(inode)
        return self

    def touch(self, file_name, size=0, update_dir_size=True):
        logger.info(f"touch - Creating file inode: {file_name}")
        inode = self.filesystem.add_inode(FileInode(self.pwd.abspath, file_name, size))

        if update_dir_size:
            # Update dir size of parent, recursively
            def _update_dir_size(child_inode):
                dir_inode = self.find(child_inode.path)
                dir_inode.size += size
                if dir_inode is not self.filesystem.root:
                    _update_dir_size(dir_inode)

            _update_dir_size(inode)

        return self

    def du(self, path=None, recursive=False):
        # Determine Path, sanitize input
        if path is None:
            path = str(self.pwd)
        # Gather sizes, recursively if all=True
        logger.debug(
            f"du - Calculating size of {str(path)} {', recursively' if recursive else ''})"
        )
        total_size = 0
        inodes = self.ls(path)
        if recursive:
            total_size += sum([inode.size for inode in inodes])
        else:
            total_size += sum(
                [inode.size for inode in inodes if inode.inode_type == "file"]
            )
        logger.debug(f"du - Total size: {total_size} bytes")

        return total_size

    def find(self, abspath):
        """Finds a single inode by absolute path (abspath)

        Args:
            abspath (_type_): Absolute path, an inode parameter

        Raises:
            ValueError: raise if nothing found

        Returns:
            Inode: a single Inode object
        """
        try:
            inode = self.filesystem.find_inodes(
                {"abspath": abspath}, ignore_root=False
            )[0]
        except (ValueError, IndexError):
            raise ValueError(f"{abspath} not found")
        return inode
