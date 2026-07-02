from io import BytesIO
from zipfile import ZipFile
from xml.etree import ElementTree
import fitz, re
from fastapi import UploadFile
from docx import Document as Docs
from video_and_audio import video_converter_service
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .vector_db_service import VectorDatabase
from typing import List

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", ".", " ", ""]
)

def process_files(files: List[UploadFile], vector_db: VectorDatabase):
    for file in files:
        chunks: list[str] = get_chunks(file)
        vector_db.upload_text_chunks(chunks, file)

def get_chunks(file: UploadFile) -> list[str]:
    content: bytes = file.file.read()

    if file.filename.endswith(".pdf"): return split_pdf_text(content)
    elif file.filename.endswith(".docx"): return split_docx_document(content)
    elif file.filename.endswith(".odt"): return split_odt_document(content)
    elif file.filename.endswith(".mp4"): return split_video_text(file)
    return []

def split_pdf_text(file_content: bytes) -> list[str]:
    document = fitz.open(stream=file_content, filetype="pdf").pages(start=1)
    pages_text = [re.sub(" +", " ", page.get_text().replace("\n", " ")) for page in document]
    return pages_text

def split_docx_document(file_content: bytes) -> list[str]:
    document = Docs(BytesIO(file_content))
    text = "\n\n".join(paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip())
    if not text: return []
    return splitter.split_text(text)


def split_odt_document(file_content: bytes) -> list[str]:
    namespaces = {
        "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
        "style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
        "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
        "fo": "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
    }

    with ZipFile(BytesIO(file_content)) as odt_file:
        content = odt_file.read("content.xml")
        styles = odt_file.read("styles.xml") if "styles.xml" in odt_file.namelist() else None

    root = ElementTree.fromstring(content)
    style_roots = [root]
    if styles:
        style_roots.append(ElementTree.fromstring(styles))

    def qname(prefix: str, name: str) -> str:
        return f"{{{namespaces[prefix]}}}{name}"

    page_break_before_styles: set[str] = set()
    page_break_after_styles: set[str] = set()

    for style_root in style_roots:
        for style_element in style_root.iter(qname("style", "style")):
            style_name = style_element.attrib.get(qname("style", "name"))
            style_family = style_element.attrib.get(qname("style", "family"))
            if not style_name or style_family != "paragraph":
                continue

            paragraph_properties = style_element.find(qname("style", "paragraph-properties"))
            if paragraph_properties is None:
                continue

            if paragraph_properties.attrib.get(qname("fo", "break-before")) == "page":
                page_break_before_styles.add(style_name)
            if paragraph_properties.attrib.get(qname("fo", "break-after")) == "page":
                page_break_after_styles.add(style_name)

    soft_page_break = qname("text", "soft-page-break")
    space = qname("text", "s")
    tab = qname("text", "tab")
    line_break = qname("text", "line-break")
    paragraph_tags = {qname("text", "p"), qname("text", "h")}
    style_name_attribute = qname("text", "style-name")
    page_break_marker = "\f"

    def extract_element_text(element: ElementTree.Element) -> str:
        if element.tag == soft_page_break:
            return page_break_marker
        if element.tag == space:
            count = int(element.attrib.get(qname("text", "c"), "1"))
            return " " * count
        if element.tag == tab:
            return "\t"
        if element.tag == line_break:
            return "\n"

        parts = [element.text or ""]
        for child in element:
            parts.append(extract_element_text(child))
            parts.append(child.tail or "")
        return "".join(parts)

    pages: list[list[str]] = [[]]

    def start_new_page() -> None:
        if pages[-1]:
            pages.append([])

    for element in root.iter():
        if element.tag not in paragraph_tags:
            continue

        paragraph_style = element.attrib.get(style_name_attribute)
        if paragraph_style in page_break_before_styles:
            start_new_page()

        paragraph_text = extract_element_text(element).strip()
        if paragraph_text:
            split_paragraph = paragraph_text.split(page_break_marker)
            pages[-1].append(split_paragraph[0])
            for text_after_break in split_paragraph[1:]:
                start_new_page()
                text_after_break = text_after_break.strip()
                if text_after_break:
                    pages[-1].append(text_after_break)

        if paragraph_style in page_break_after_styles:
            start_new_page()

    page_texts = ["\n".join(paragraphs).strip() for paragraphs in pages]
    text = "\n\n".join(page_text for page_text in page_texts if page_text)
    return splitter.split_text(text)



def split_video_text(file: UploadFile) -> list[str]:
    video_text: str = video_converter_service.from_video_to_text(file)
    return splitter.split_text(video_text)
