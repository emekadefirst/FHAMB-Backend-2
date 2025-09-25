from io import BytesIO
import zipfile
import fitz  

FILE_SIGNATURES = {
    b"\xFF\xD8\xFF": "jpeg",
    b"\x89PNG\r\n\x1A\n": "png",
    b"GIF87a": "gif",
    b"GIF89a": "gif",
    b"\x42\x4D": "bmp",
    b"\x49\x49\x2A\x00": "tiff",
    b"\x4D\x4D\x00\x2A": "tiff",
    b"%PDF": "pdf",
    b"PK\x03\x04": "zip",  
    b"Rar!\x1A\x07\x00": "rar",
    b"Rar!\x1A\x07\x01\x00": "rar",
    b"\x7FELF": "elf",
    b"MZ": "exe",
    b"\x00\x00\x00\x14ftyp": "mp4",
    b"\x1F\x8B\x08": "gzip",
    b"OggS": "ogg",
    b"ID3": "mp3",
    b"\xFF\xFB": "mp3",
}

EXTENSION_MAP = {
    "jpeg": ["jpg", "jpeg"],
    "png": ["png"],
    "gif": ["gif"],
    "bmp": ["bmp"],
    "tiff": ["tif", "tiff"],
    "pdf": ["pdf"],
    "docx": ["docx"],
    "xlsx": ["xlsx"],
    "pptx": ["pptx"],
    "zip": ["zip"],
    "rar": ["rar"],
    "elf": ["elf"],
    "exe": ["exe"],
    "mp4": ["mp4"],
    "gzip": ["gz"],
    "ogg": ["ogg"],
    "mp3": ["mp3"],
}

SUPPORTED_FILE_TYPES = {".pdf", ".docx", ".pptx", ".xlsx", ".mp3", ".mp4", ".jpg", ".jpeg", ".png"}

SUSPICIOUS_PDF_KEYWORDS = ["/JavaScript", "/JS", "/AA", "/OpenAction", "/EmbeddedFile"]


def get_file_signature_from_head(head_bytes: bytes) -> str | None:
    """Fast signature guess from the first few KB."""
    for sig, ftype in FILE_SIGNATURES.items():
        if head_bytes.startswith(sig):
            return ftype
    return None


def refine_zip_office_type(full_bytes: bytes) -> str:
    """If it's a ZIP, check if it's an Office doc (docx/xlsx/pptx)."""
    try:
        zf = zipfile.ZipFile(BytesIO(full_bytes))
        names = zf.namelist()
        if "[Content_Types].xml" in names:
            if any(n.startswith("word/") for n in names):
                return "docx"
            if any(n.startswith("xl/") for n in names):
                return "xlsx"
            if any(n.startswith("ppt/") for n in names):
                return "pptx"
        return "zip"
    except Exception:
        return "zip"


def detect_type(head_bytes: bytes, maybe_full_bytes: bytes | None = None) -> str | None:
    """
    Detect type from signature quickly; if ZIP and full bytes provided, refine to docx/xlsx/pptx.
    """
    base = get_file_signature_from_head(head_bytes)
    if base == "zip" and maybe_full_bytes is not None:
        return refine_zip_office_type(maybe_full_bytes)
    return base


def scan_pdf_for_malware_bytes(pdf_bytes: bytes) -> str | bool:
    """
    In-memory PDF scan: flags embedded JS/auto-actions/embedded files.
    Returns True if clean; otherwise a warning/error string.
    """
    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            raw = []
            for i in range(len(doc)):
                raw.append(doc[i].get_text("text"))
                raw.append(str(doc[i]))  # raw object repr (quick signal)
            haystack = "".join(raw)

            for kw in SUSPICIOUS_PDF_KEYWORDS:
                if kw in haystack:
                    return f"⚠ Suspicious PDF content: {kw}"
        return True
    except Exception as e:
        return f"❌ Error scanning PDF: {e}"
