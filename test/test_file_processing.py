import sys
import types

import pytest

from slack_assistant.utils import file_processing


class FakeResponse:
    def __init__(self, content=b"text", status_code=200):
        self.content = content
        self.status_code = status_code


@pytest.mark.parametrize(
    ("file_name", "content"),
    [("notes.txt", b"plain text"), ("notes.md", b"markdown")],
)
def test_processes_text_files(monkeypatch, file_name, content):
    monkeypatch.setattr(
        file_processing.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(content),
    )

    result = file_processing.process_files(
        {"files": [{"name": file_name, "url_private": "http://file"}]},
        lambda message: None,
    )

    assert result == content.decode("utf-8")


def test_processes_html_file(monkeypatch):
    monkeypatch.setattr(
        file_processing.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(b"<p>Hello</p>"),
    )

    assert file_processing.process_files(
        {"files": [{"name": "page.html", "url_private": "http://file"}]},
        lambda message: None,
    ) == "Hello"


def test_processes_pdf_and_docx_files(monkeypatch):
    class Page:
        def extract_text(self):
            return "pdf text"

    fake_pdf = types.ModuleType("PyPDF2")
    fake_pdf.PdfReader = lambda content: types.SimpleNamespace(pages=[Page()])
    fake_docx = types.ModuleType("docx")
    fake_docx.Document = lambda content: types.SimpleNamespace(
        paragraphs=[types.SimpleNamespace(text="docx text")]
    )
    monkeypatch.setitem(sys.modules, "PyPDF2", fake_pdf)
    monkeypatch.setitem(sys.modules, "docx", fake_docx)
    monkeypatch.setattr(
        file_processing.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(b"file"),
    )

    assert file_processing.process_files(
        {"files": [{"name": "file.pdf", "url_private": "http://file"}]},
        lambda message: None,
    ) == "pdf text"
    assert file_processing.process_files(
        {"files": [{"name": "file.docx", "url_private": "http://file"}]},
        lambda message: None,
    ) == "docx text"


def test_reports_failed_and_unsupported_files(monkeypatch):
    messages = []
    responses = iter([FakeResponse(status_code=500), FakeResponse(b"data")])
    monkeypatch.setattr(
        file_processing.requests,
        "get",
        lambda *args, **kwargs: next(responses),
    )

    result = file_processing.process_files(
        {
            "files": [
                {"name": "bad.txt", "url_private": "http://file"},
                {"name": "image.png", "url_private": "http://file"},
            ]
        },
        messages.append,
    )

    assert result == ""
    assert messages == [
        "Failed to securely download the file.",
        "Unsupported file type: image.png",
    ]


def test_reports_processing_exception(monkeypatch):
    messages = []

    def raise_error(*args, **kwargs):
        raise RuntimeError("failed")

    monkeypatch.setattr(file_processing.requests, "get", raise_error)

    assert file_processing.process_files(
        {"files": [{"name": "file.txt", "url_private": "http://file"}]},
        messages.append,
    ) == ""
    assert messages == ["An error occurred while analyzing the document."]