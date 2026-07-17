from langchain_text_splitters import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=150,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ],
    length_function=len
)


def chunk_text(text: str) -> list[str]:

    # Clean unnecessary whitespace
    text = text.strip()

    if not text:
        return []

    # Split document into overlapping chunks
    chunks = splitter.split_text(text)

    # Remove empty chunks
    return [
        chunk.strip()
        for chunk in chunks
        if chunk.strip()
    ]