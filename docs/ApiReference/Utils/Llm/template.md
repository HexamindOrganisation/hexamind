# Template 

## Overview 

This is the class where the prompt template are defined.  There is one prompt template by LlmAgent function. 

## Templates 

#### generate_paragraph

Generate a paragraph from the prompt.

**Parameters**

- `query`(str): The user query.
- `context`(str): The context related to the user query.
- `histo` (List[(str,str)]): The history of the conversation.

**Returns**

- `str`: The final prompt.

#### translate

Translate the prompt to another language.

**Parameters**

- `text`(str): The prompt to be translated.

**Returns**

- `str`: The final prompt. Only english is supported for now.

#### summarize_paragraph

Summarize a paragraph.

**Parameters**

- `prompt`(str): The paragraph to be summarized.
- `location`(str): The location of the paragraph.
- `context`(str): The context of the paragraph.
- `language`(str): The language of the paragraph.

**Returns**

- `str`: The final prompt.


#### detect_language

Detect the language of a paragraph.

**Parameters**

- `text`(str): The paragraph to detect the language.

**Returns**

- `str`: The final prompt.

