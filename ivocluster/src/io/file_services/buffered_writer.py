from os   import path
from time import sleep

class BufferedWriter():
    """
    For each file out of an arbitrary large amount of files the BufferedWriter stores a
    list of lines. Only when they exceed a predefined limit their contents are 
    collectively written to the filesystem. By preventing repeated opening and closing of
    files the BufferedWriter reduces computation time.
    """

    def __init__(self, out_dir=".", lines_per_file=24):
        """
        Args:
            out_dir (str, optional):        Base path for all files you want to write to.
                                            Defaults to ".".
            lines_per_file (int, optional): Maximum number of lines to buffer for each file.
                                            Defaults to 25.
        """

        self.buffer          = {}
        self.lines_per_file  = lines_per_file
        self.out_dir         = out_dir

    def __enter__(self):
        return self
    
    def __exit__(self, exec_type, exec_val, exec_tb):
        self.flush()

    def flush_file(self, file_path: str):
        """
        Write buffered content to chosen file

        Args:
            file_path (str):
        """
        try:
            with open(path.join(self.out_dir, file_path), "a") as file:
                for line in self.buffer[file_path]:
                    file.write(line+"\n")
            self.buffer[file_path] = []
        except:
            sleep(1/1000)
            self.flush_file(file_path)

    def flush(self):
        """
        Write all buffered content to their respective files
        """
        for file_path in self.buffer.keys():
            self.flush_file(file_path)

    def write_line(self, file_path: str, line: str):
        """
        Add a line to the buffer

        Args:
            file_path (str):
            line (str):
        """
        try:
            self.buffer[file_path].append(line)
        except:
            self.buffer[file_path] = [line]

        if len(self.buffer[file_path]) > self.lines_per_file:
            self.flush_file(file_path)
