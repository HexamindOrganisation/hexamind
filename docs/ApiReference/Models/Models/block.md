# Block 

```python

class Block(
    parent_uid: Optional[str], 
    title: str, 
    level: int, 
    section_number: str, 
    content: str
    )

```

## Parameters

- `parent_uid` : Optional[str]
    - The unique identifier of the parent container. If the block is a root block, the parent_uid is None.
- `title` : str
    - The title of the block. Based on the section title.
- `level` : int
    - The level of the block in the document hierarchy. The root block has level 0.
- `section_number` : str
    - The section number of the block. The section number is a string that represents the position of the block in the document hierarchy. The section number is a sequence of integers separated by dots. For example, the section number of a block that is the first child of the root container is "1". The section number of a block that is the second child of the first child of the root container is "1.2".
- `content` : str
    - The content of the block. 


## Attributes

- `uid` : str
    - The unique identifier of the block. The unique identifier is generated using the `uuid` module.
- `parent_uid` : Optional[str]
    - The unique identifier of the parent container. If the block is a root block, the parent_uid is None.
- `title` : str
    - The title of the block. Based on the section title.
- `level` : int
    - The level of the block in the document hierarchy. The root block has level 0.
- `section_number` : str
    - The section number of the block. The section number is a string that represents the position of the block in the document hierarchy. The section number is a sequence of integers separated by dots. For example, the section number of a block that is the first child of the root container is "1". The section number of a block that is the second child of the first child of the root container is "1.2".
- `parent` : Optional[Container]
    - The parent container of the block. If the block is a root block, the parent is None.
- `content` : str
    - The content of the block.

## Methods

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        def get_content(self) -> str
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Returns the content of the block.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;">

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        def to_dict(self) -> Dict[str, Any]
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Serialize the block to a dictionary.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;">