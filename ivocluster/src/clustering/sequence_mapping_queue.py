from src.io.file_services import paf_file_service, utils

class SequenceMappingQueue():
    """
    A queue for the parallel reading of sequences and their corresponding mappings from
    .paf-files.

    Idea:
    The Queue holds a single query and a list of n mappings, the first n-1 of them
    corresponding to the query pair.

    Using queue() yields the query and all it's corresponding mappings and removes
    them from the queue. The previous state of the queue is then restored by first loading
    the next query. If it does not correspond to the query, the state of the queue is
    already restored. If not, more mappings are loaded until we find one that does not
    correspond to the query pair.
    """

    def get_query_id(cls, query):

        return query["header"][1:].split(" ")[0]

    def __init__(self, query, paf):

        self.queries = utils.get_read_reader(query).read(query)
        self.paf     = paf_file_service.PafFileService().read(paf)

        self.current_query    = None
        self.current_mappings = [next(self.paf)]

        self.restore_state()
                
    def print_current_state(self):

        print("Current query:")
        print(self.get_query_id(self.current_query))
        print("Current mappings:")
        for m in self.current_mappings:
            print("Query: "+m["query_name"]+" Reference: "+m["target_name"])
            print(m)
        print()

    def restore_state(self):
    
        self.current_query = next(self.queries)
        
        query_id = self.get_query_id(self.current_query)

        while query_id in self.current_mappings[len(self.current_mappings)-1]["query_name"]:
            self.current_mappings.append(next(self.paf))

    def queue(self):
        
        while True:

            yield self.current_query, self.current_mappings[:-1]

            try:  
                self.current_query      = None
                self.current_mappings   = [self.current_mappings[-1]]
                self.restore_state()
            except:
                break