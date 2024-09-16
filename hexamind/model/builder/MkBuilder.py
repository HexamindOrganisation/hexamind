import markdown
from hexamind.model.model.container import Container
from hexamind.model.model.block import Block
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional


class MkBuilder:

    @classmethod
    def from_htlm(
        cls,
        htlm_content: str,
        document_title: str,
        metadatas: Optional[List[Dict[str, Any]]],
    ) -> Container:
        soup = BeautifulSoup(htlm_content, features="html.parser")
        return cls._get_document_structure(soup, document_title, metadatas)

    @staticmethod
    def _table_to_string(table):
        table_content = ""
        for row in table.find_all("tr"):
            row_text = " | ".join(
                cell.get_text(strip=True) for cell in row.find_all(["td", "th"])
            )
            table_content += row_text + "\n"
        return table_content.strip()

    @classmethod
    def _get_document_structure(
        cls, soup: str, document_title: str, metadatas: Optional[List[Dict[str, Any]]]
    ) -> Container:

        root_container = Container(
            parent_uid=None,
            title=document_title,
            level=0,
            section_number="1",
            metadatas=metadatas,
        )

        hierarchy = [root_container]
        section_counters = {0: 1}

        for element in soup.find_all(
            ["h1", "h2", "h3", "h4", "h5", "h6", "p", "table"]
        ):
            if element.name.startswith("h"):
                level = int(element.name[1])
                title = element.get_text(strip=True)

                while len(hierarchy) > 1 and hierarchy[-1].level >= level:
                    hierarchy.pop()

                if level not in section_counters:
                    section_counters[level] = 1
                else:
                    section_counters[level] += 1

                for lvl in range(level + 1, max(section_counters.keys()) + 1):
                    section_counters.pop(lvl, None)

                section_number = ".".join(
                    str(section_counters.get(i, 1)) for i in range(1, level + 1)
                )

                new_container = Container(
                    parent_uid=hierarchy[-1].uid,
                    title=title,
                    level=level,
                    section_number=section_number,
                    metadatas=metadatas,
                )

                hierarchy[-1].add_child(new_container)
                hierarchy.append(new_container)

            elif element.name == "p":
                text = element.get_text(strip=True)
                if text:
                    leaf_container = Container(
                        parent_uid=hierarchy[-1].uid,
                        title=hierarchy[-1].title,
                        level=hierarchy[-1].level,
                        section_number=hierarchy[-1].section_number,
                        metadatas=metadatas,
                    )
                    block = Block(
                        parent_uid=leaf_container.uid,
                        title=leaf_container.title,
                        level=leaf_container.level,
                        section_number=leaf_container.section_number,
                        content=text,
                        metadatas=metadatas,
                    )

                    leaf_container.add_child(block)
                    hierarchy[-1].add_child(leaf_container)

            elif element.name == "table":
                table_content = cls._table_to_string(element)
                for paragraph in element.find_all("p"):
                    table_content += "\n" + paragraph.get_text(strip=True)

                leaf_container = Container(
                    parent_uid=hierarchy[-1].uid,
                    title=hierarchy[-1].title,
                    level=hierarchy[-1].level + 1,
                    section_number=hierarchy[-1].section_number,
                    metadatas=metadatas,
                )

                block = Block(
                    parent_uid=leaf_container.uid,
                    title=leaf_container.title,
                    level=leaf_container.level,
                    section_number=leaf_container.section_number,
                    content=table_content,
                    metadatas=metadatas,
                )

                leaf_container.add_child(block)
                hierarchy[-1].add_child(leaf_container)

        return root_container
