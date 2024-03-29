from hxm_rag.model.modelv2.element import Element
from hxm_rag.model.modelv2.block import Block
from hxm_rag.llm.llm.LlmAgent import LlmAgent
import uuid

class Container(Element):
    def __init__(self, parent_document, parent_container = None, level=0):
        super().__init__()
        self.parent_container = parent_container
        self.parent_document = parent_document
        self.parent_document_uid = parent_document.uid if parent_document else None
        self.parent_container_uid = parent_container.uid if parent_container else None
        self.children = [] # adjency list
        self.level = level
        self.content = ''
        self.embeddings = []
        self.chunk_ids = []
        self.chunks = []
        self.metadatas = []
        self.summary = ''
        self.summary_embeddings = []
        self.summary_chunk_id = []
        self.summary_chunks =  []
        self.summary_metadatas = []
    
    def get_content(self):
        content_parts = []
        for child in self.children:
            if isinstance(child, Container):
                child.get_content()
                content_parts.append(child.content)
            elif isinstance(child, Block):
                content_parts.append(child.content)
        self.content = '\n\n'.join(content_parts)
    
    
    def print_structure(self, indent=0): #DFS traversal to print the structure of the container
        if self.level == 0:
            print(f'Root container, Level : {self.level}')
        else:
            print('  '*indent + f'Container, Level : {self.level}')

        for child in self.children:
            if isinstance(child, Container):
                child.print_structure(indent+1)
            elif isinstance(child, Block):
                print('  '*(indent+1) + f'Block, Level : {child.level}')
    
    def add_child(self, child):
        self.children.append(child)
    
    
    @classmethod
    def from_dict(cls, structure_dict, parent_document=None, parent_container = None):
        container = cls(parent_document, parent_container, structure_dict.get('level', 0))

        for child in structure_dict.get('children', []):
            if child['type'] == 'container':
                child_container = cls.from_dict(child, parent_document, container)
                container.add_child(child_container)
            elif child['type'] == 'block':
                block = Block(child.get('content', ''), parent_document, container)
                container.add_child(block)
        
        return container
    
    def get_embeddings(self, llm_agent:LlmAgent):
        if not llm_agent:
            raise ValueError('LLM agent not set')

        max_length = 8192
  

        if len(self.content)<=max_length:
            self.embeddings.append(llm_agent.get_embedding(self.content))
            self.chunk_ids.append(str(uuid.uuid4()))
            self.chunks.append(self.content)
            self.metadatas.append(self.to_dict())

        for child in self.children:
            if isinstance(child, (Container)):
                child.get_embeddings(llm_agent)
    
    def get_summaries(self, llm_agent:LlmAgent):
        if not llm_agent:
            raise ValueError('LLM agent not set')
    
        if self.content:
            self.summary = llm_agent.summarize_paragraph(self.content)
            self.summary = self.summary.split('<summary>')[1] if '<summary>' in self.summary else self.summary
            self.summary_embeddings.append(llm_agent.get_embedding(self.summary))
            self.summary_chunk_id.append(str(uuid.uuid4()))
            self.summary_chunks.append(self.summary)
            self.summary_metadatas.append(self.to_dict())

        
        for child in self.children:
            if isinstance(child, (Container)):
                child.get_summaries(llm_agent)

    def to_dict(self):
        return {
            'uid' : self.uid if self.uid else '',
            'parent_document_uid' : self.parent_document_uid if self.parent_document_uid else '',
            'parent_container_uid' : self.parent_container_uid if self.parent_container_uid else '',
            'level' : self.level if self.level else 0,
            'children' : str([child.uid for child in self.children])
        }