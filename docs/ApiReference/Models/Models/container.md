# Container

```python

class Container(
    parent_uid: Optional[str], 
    title: str, 
    level: int, 
    section_number: str)
```

## Parameters

- `parent_uid` : Optional[str]
    - The unique identifier of the parent container. If the container is a root container, the parent_uid is None.
- `title` : str
    - The title of the container. Based on the section title. 
- `level` : int
    - The level of the container in the document hierarchy. The root container has level 0.
- `section_number` : str
    - The section number of the container. The section number is a string that represents the position of the container in the document hierarchy. The section number is a sequence of integers separated by dots. For example, the section number of a container that is the first child of the root container is "1". The section number of a container that is the second child of the first child of the root container is "1.2".


## Attributes

- `uid` : str
    - The unique identifier of the container. The unique identifier is generated using the `uuid` module.
- `parent_uid` : Optional[str]
    - The unique identifier of the parent container. If the container is a root container, the parent_uid is None.
- `title` : str
    - The title of the container. Based on the section title.
- `level` : int
    - The level of the container in the document hierarchy. The root container has level 0.
- `section_number` : str
    - The section number of the container. The section number is a string that represents the position of the container in the document hierarchy. The section number is a sequence of integers separated by dots. For example, the section number of a container that is the first child of the root container is "1". The section number of a container that is the second child of the first child of the root container is "1.2".
- `children` : List[Container]
    - The list of child containers of the container.
- `parent` : Optional[Container]
    - The parent container of the container. If the container is a root container, the parent is None.
- `content` : str
    - The content of the container. The content is a markdown string.

## Methods

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        def add_child(
            self,
            child: Union['Container', 'Block']
            ) -> None
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Add a child container or block to the container and update the content of the container.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;">

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        def get_content(self) -> str
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Returns the content of the container. 
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;">

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 8px;">
        ```python
        def visualize(
            self, 
            filename='container_structure'
            ) -> None
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Called by the `Document` class to visualize the container structure.
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
        Serialize the container to a dictionary.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;">