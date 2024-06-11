# Summarizer

```python

class Summarizer(llm_agent: LlmAgent)

```

## Overview 

The `Summarizer` is a class defined to create summary of differents block, level, section number or document. 

## Parameters

- `llm_agent` : The llm agent used to generate the summary.


## Attributes

- `llm_agent` : The llm agent used to generate the summary. 


## Methods

<div style="display: flex; flex-direction: row; justify-content: space-between; magin-bottom: 10px">
    <div style="flex: 1; padding: 10px;">
        ```python
        def summarize(
            self, 
            text: str, 
            doc_name: str, 
            section_name:str
            ) -> str
        ```
    </div>
    <div style="flex: 2; padding: 20px; ">
        Generate a summary of the text.
    </div>
</div>

<hr style="border: none; border-top: 1px solid #ccc; margin 20px 0;"> 

## Usage Example

```python

if section_number:
            container = self._find_container_by_section_number(self.root_container, section_number)
            if container: 
                return self.summarizer.summarize(container.get_content(), self.title, container.title)

```
