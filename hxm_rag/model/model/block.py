class Block:
    """
    Block class that represents a unit of content within a document. 
    It stores information relevant to the content such as its title, text, position in the document,
    and any metadata that may be useful for retrieval and processing in a RAG system.
    
    Attributes:
        doc_path (str): The path to the document from which the block originates.
        title (str): The title or heading of the block.
        content (str): The actual textual content of the block.
        index (str): A hierarchical index indicating the block's position within the document structure.
        rank (int): A numerical rank that may be used for sorting or prioritization in retrieval tasks.
        level (int): The level in the document hierarchy, with lower numbers indicating higher levels.
        distance (float): Represents the relevance or similarity of the block to a query, with lower numbers indicating higher relevance.
    """

    def __init__(
        self,
        doc_path: str = "",
        title: str = "",
        content: str = "",
        index: str = "",
        rank: int = 0,
        level: int = 0,
        distance: float = 99999,
    ):
        self.doc_path = doc_path
        self.title = title
        self.content = content
        self.index = index
        self.rank = rank
        self.level = level
        self.distance = distance

    @property
    def distance_str(self) -> str:
        """
        Returns the distance as a string formatted to two decimal places. If the distance is
        not a float, a ValueError will be raised.
        """
        if not isinstance(self.distance, float):
            raise ValueError("Distance must be a float.")
        return f"{self.distance:.2f}"

    @classmethod
    def from_dict(cls, data: dict) -> "Block":
        """
        Creates an instance of Block from a dictionary. This method validates the input dictionary
        to ensure it contains the necessary keys and values of appropriate types.
        
        Parameters:
            data (dict): The dictionary from which to create the Block instance.
        
        Returns:
            Block: An instance of the Block class.
        
        Raises:
            ValueError: If the provided dictionary does not contain the correct keys and value types.
        """
        if not isinstance(data, dict):
            raise AssertionError("data must be dict")

        required_keys = {
            "doc_path": str,
            "title": str,
            "content": str,
            "index": str,
            "rank": int,
            "level": int,
            "distance": float,
        }

        missing_keys = required_keys.keys() - data.keys()
        if missing_keys:
            raise AssertionError(f"Missing keys in data: {missing_keys}")

        for key, expected_type in required_keys.items():
            if not isinstance(data[key], expected_type):
                raise AssertionError(
                    f"Key '{key}' must be of type {expected_type.__name__}."
                )

        return cls(**data)

    def to_dict(self) -> dict:
        """
        Converts the Block instance to a dictionary. 
        
        Returns:
            dict: The dictionary representation of the Block instance.
        """
        return {
            "doc_path": self.doc_path,
            "title": self.title,
            "content": self.content,
            "index": self.index,
            "rank": self.rank,
            "level": self.level,
            "distance": self.distance,
        }
