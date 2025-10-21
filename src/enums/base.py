from enum import Enum


class FileType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"
    AUDIO = "audio"


class ImageExtension(str, Enum):
    JPG = "jpg"
    PNG = "png"
    JPEG = "jpeg"
    GIF = "gif"
    WEBP = "webp"
    BMP = "bmp"
    TIFF = "tiff"


class VideoExtension(str, Enum):
    MP4 = "mp4"
    AVI = "avi"
    MKV = "mkv"
    MOV = "mov"
    WMV = "wmv"
    FLV = "flv"
    WEBM = "webm"


class DocumentExtension(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    PPTX = "pptx"
    XLSX = "xlsx"
    TXT = "txt"
    ODT = "odt"
    RTF = "rtf"


class AudioExtension(str, Enum):
    MP3 = "mp3"
    WAV = "wav"
    AAC = "aac"
    FLAC = "flac"
    OGG = "ogg"
    WMA = "wma"
    M4A = "m4a"


class Action(str, Enum):
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"



class Resource(str, Enum):
    FILE = "file"
    AUTH = "auth"
    MAIL = "mail"
    PUBLIC = "punlic"


class EmailStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class EmailCategory(str, Enum):
    PROMOTIONAL = "promotional"
    TRANSACTIONAL = "transactional"
    NOTIFICATION = "notification"
    NEWSLETTER = "newsletter"


class ContentStatus(str, Enum):
    PUBLISH = "published"
    DRAFT = "draft"