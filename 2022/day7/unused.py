# @dataclass
# class File:
#     name: str
#     size: int


# class Directory:
#     def __init__(self, name, parent_name=None):
#         self.name = name
#         self.parent_name = parent_name
#         self.files = []
#         self.dirs = {}
#         self.size: int = 0

#     def __repr__(self):
#         return f"Directory({self.name}, parent={self.parent_name}, {self.size}, {self.dirs})"

#     def add_file(self, file_name, file_size):
#         self.files.append(File(file_name, file_size))
#         self.size = self.get_total_size()
#         logger.info(f"Added file {file_name} to {self.name}")

#     def add_dir(self, dir_name):
#         if self.dirs.get(dir_name) is None:
#             self.dirs[dir_name] = Directory(dir_name, self.name)
#             logger.info(f"Created new dir: {self.dirs[dir_name]}")
#         return self.dirs[dir_name]

#     def get_total_size(self):
#         total_size = 0
#         logger.debug(f"Getting total size for {self.name} with {len(self.files)} files")
#         for file in self.files:
#             total_size += file.size
#         for dir in self.dirs.values():
#             dir.get_total_size()
#             total_size += dir.size
#         return total_size

#     def get_parent(self, search_dir, child=None):
#         # Recursively search dirs for parent
#         if not child:
#             child = self
#         logger.info(f"Searching for parent of {child.name} in {search_dir.name}")
#         logger.debug(f"{search_dir.name}: \n {pformat(search_dir.__dict__)}")
#         if search_dir.name == child.parent_name:
#             logger.info(f"Found parent: {search_dir.name}")
#             return search_dir
#         else:
#             for dir in search_dir.dirs.values():
#                 return dir.get_parent(dir, child)
#         # If we don't find anything, raise an error
#         raise ValueError("No parent found")


# root = Directory("/")
# current_dir = root
# for line in PUZZLE_INPUT:
#     logger.info(
#         f"> {current_dir.name} #> {PUZZLE_INPUT.index(line)} {line}",
#     )
#     line_items = line.split(" ")
#     match line_items[0]:
#         case "$":
#             match line_items[1]:
#                 case "cd":
#                     dir_name = line_items[-1]
#                     logger.info(f"changing from: {current_dir.name} to {dir_name}")
#                     match dir_name:
#                         case "..":
#                             current_dir = current_dir.get_parent(root)
#                         case "/":
#                             current_dir = root
#                         case _:
#                             current_dir = current_dir.change_dir(dir_name)
#                 case "ls":
#                     # find all lines between this line and the next command
#                     files_in_dir = []
#                     for tmp_line in PUZZLE_INPUT[PUZZLE_INPUT.index(line) + 1 :]:
#                         if tmp_line[0] == "$":
#                             break
#                         files_in_dir.append(tmp_line)
#                     logger.info(f"files in {current_dir.name}: {files_in_dir}")
#         case "dir":
#             dir_name = line_items[-1]
#             logger.info("found dir: %s", dir_name)
#             current_dir.add_dir(dir_name)
#             logger.debug("current dir: %s", current_dir)
#         case x if int(x):
#             file_name = line_items[-1]
#             file_size = int(line_items[0])
#             logger.info(f"found file: {line_items[-1]} with size {file_size}")
#             current_dir.add_file(file_name, file_size)
#         case _:
#             raise ValueError("Failed to parse line_items: %s", line_items)


# # pprint(file_system)
# pprint(root.get_total_size())


# -------------------------
