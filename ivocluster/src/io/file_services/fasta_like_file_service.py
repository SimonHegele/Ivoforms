from abc    import ABC, abstractmethod
from typing import Generator

class FastaLikeFileService(ABC):

    @classmethod
    @abstractmethod
    def parse_string(cls, string: str)->dict:
        pass

    @classmethod
    @abstractmethod
    def parse_dict(cls, data: dict)->str:
        pass

    @classmethod
    def read(cls, file_path:str)->Generator:
         
        string = ""
        
        with open(file_path, "r") as f:

            for i, line in enumerate(f):

                if (line[0] == cls.separator) and (i > 0):
                    if i > 0:
                        yield cls.parse_string(string)
                        string = ""
                
                string += line

            yield cls.parse_string(string)

    @classmethod
    def write(cls, file_path: str, data: list[dict], mode="w")->None:

        with open(file_path, mode) as file:
            for d in data:
                file.writelines(cls.parse_dict(d))
