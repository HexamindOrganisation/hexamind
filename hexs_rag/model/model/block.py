# Description: Block class that represents the lower information level of a document.

class Block: 
    """
    Block class that represents the lower information level of a document. 
    Attributes:
    - doc: the document path
    - title: the title of the document
    - content: the content of the document
    - index: the index of the block in the document
    - rank: the rank of the block in the document
    - level: the level of the block in the document
    - distance: the distance of the block to the query
    """

    def __init__(self, doc: str= '',title: str = '', content: str = '',
                index: str = '', rank: int = 0, level: int = 0, distance: float = 99999):
        self.doc = doc
        self.title = title
        self.content = content
        self.index = index
        self.rank = rank
        self.level = level
        self.distance = distance
    
    @property
    def distance_str(self) -> str:
        """
        Returns the distance as a string with two decimal digits
        """
        try:
            return format(self.distance, '.2f')
        except Exception as e:
            raise ValueError(f"Could not get distance as string: {e}")
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a block from a dictionary
        """
        expected_keys = {'doc' : str,
                        'title' : str,
                        'content' : str,
                        'index' : str,
                        'rank' : int,
                        'level' : int,
                        'distance' : float}
        
        if not isinstance(data, dict):
            raise AssertionError('data should be a dictionary')
        
        if set(data.keys()) != expected_keys.keys():
            raise AssertionError('data should contain the following keys: {}'.format(expected_keys.keys()))
        
        for key, expected_type in expected_keys.items():
            if not isinstance(data[key], expected_type):
                raise AssertionError('data[{}] should be of type {}'.format(key, expected_type))
        
        try:
            return cls(doc=data.get('doc', ''),
                    title=data.get('title', ''),
                    content=data.get('content', ''),
                    index=data.get('index', ''),
                    rank=data.get('rank', 0),
                    level=data.get('level', 0),
                    distance=data.get('distance', 99999))
        except Exception as e:
            raise ValueError(f"Could not create block from dictionary: {e}")
    
    def to_dict(self) -> dict:
        """
        Returns the block as a dictionary
        TODO : check if it is a necessary method since we can use the __dict__ attribute
        """
        try:
            return {'doc': self.doc,
                    'title': self.title,
                    'content': self.content,
                    'index': self.index,
                    'rank': self.rank,
                    'level': self.level,
                    'distance': self.distance}
        except Exception as e:
            raise ValueError(f"Could not get block as dictionary: {e}")
    
