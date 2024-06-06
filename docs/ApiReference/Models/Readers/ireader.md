# IReader

## Overview

This is the interface that all readers should implement. It has a single method `convert_to_markdown` that should be implemented by the child classes.

## How to use it 

You can create your own reader class by inheriting from this interface and implementing the `convert_to_markdown` method.

### Example

```python

class MyReader(IReader):
    def __init__(self, path):
        self.path = path

    def convert_to_markdown(self):
        # Your implementation here
        pass

```