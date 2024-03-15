"""
Utility functions related to the block class but not directly related to the class itself
"""
import math

from hexs_rag.model.model.block import Block


def separate_1_block_in_n(block: Block, max_size=3000) -> list[Block]:
    """
    Separate a block in n blocks of equal size
    """
    content_length = len(block.content)
    n = math.ceil(content_length / max_size)
    block_size = content_length // n
    new_blocks = []
    for i in range(n):
        start = i * block_size
        end = (i + 1) * block_size if i < n - 1 else None
        new_blocks.append(
            Block(
                doc=block.doc,
                title=block.title + f"_part{i}",
                content=block.content[start:end],
                index=block.index + f"_{i}",
                rank=block.rank,
                level=block.level,
            )
        )
    return new_blocks
