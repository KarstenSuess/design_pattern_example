from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Iterable
import os
import xml.etree.ElementTree as ET


# ============ Helpers ============

def _txt(el: Optional[ET.Element]) -> Optional[str]:
    if el is None:
        return None
    t = el.text if el.text is not None else None
    return t.strip() if isinstance(t, str) else t


def _int(el: Optional[ET.Element]) -> Optional[int]:
    t = _txt(el)
    if t in (None, "", "NaN"):
        return None
    try:
        return int(t)
    except Exception:
        # some values may include units or be malformed; best effort: extract leading digits
        digits = "".join(ch for ch in t if ch.isdigit())
        try:
            return int(digits) if digits else None
        except Exception:
            return None


def _attr(el: Optional[ET.Element], name: str) -> Optional[str]:
    if el is None:
        return None
    return el.get(name)


# ============ Dataclasses ============

@dataclass
class ByteCount:
    lf: Optional[int] = None
    cr: Optional[int] = None
    tab: Optional[int] = None
    csvSemicolonFirstLine: Optional[int] = None
    csvLF: Optional[int] = None
    semicolon: Optional[int] = None
    pipe: Optional[int] = None
    comma: Optional[int] = None
    colon: Optional[int] = None
    minus: Optional[int] = None
    equal: Optional[int] = None
    singleQuote: Optional[int] = None
    doubleQuote: Optional[int] = None
    null: Optional[int] = None
    blank: Optional[int] = None
    upperC_D: Optional[int] = None
    upperC_O: Optional[int] = None
    upperC_T: Optional[int] = None
    lowerC_d: Optional[int] = None
    lowerC_o: Optional[int] = None
    lowerC_t: Optional[int] = None
    zeichenformat: Optional[str] = None

    @classmethod
    def from_element(cls, el: Optional[ET.Element]) -> "ByteCount":
        if el is None:
            return cls()
        return cls(
            lf=_int(el.find("lf")),
            cr=_int(el.find("cr")),
            tab=_int(el.find("tab")),
            csvSemicolonFirstLine=_int(el.find("csvSemicolonFirstLine")),
            csvLF=_int(el.find("csvLF")),
            semicolon=_int(el.find("semicolon")),
            pipe=_int(el.find("pipe")),
            comma=_int(el.find("comma")),
            colon=_int(el.find("colon")),
            minus=_int(el.find("minus")),
            equal=_int(el.find("equal")),
            singleQuote=_int(el.find("singleQuote")),
            doubleQuote=_int(el.find("doubleQuote")),
            null=_int(el.find("null")),
            blank=_int(el.find("blank")),
            upperC_D=_int(el.find("upperC_D")),
            upperC_O=_int(el.find("upperC_O")),
            upperC_T=_int(el.find("upperC_T")),
            lowerC_d=_int(el.find("lowerC_d")),
            lowerC_o=_int(el.find("lowerC_o")),
            lowerC_t=_int(el.find("lowerC_t")),
            zeichenformat=_txt(el.find("zeichenformat")),
        )


@dataclass
class Stats:
    status: Optional[str] = None
    md5: Optional[str] = None
    filesize: Optional[int] = None
    filename: Optional[str] = None
    lastmod: Optional[int] = None
    created: Optional[int] = None
    byte_count: ByteCount = field(default_factory=ByteCount)

    @classmethod
    def from_element(cls, el: Optional[ET.Element]) -> "Stats":
        if el is None:
            return cls()
        return cls(
            status=_attr(el, "status"),
            md5=_txt(el.find("md5")),
            filesize=_int(el.find("filesize")),
            filename=_txt(el.find("filename")),
            lastmod=_int(el.find("lastmod")),
            created=_int(el.find("created")),
            byte_count=ByteCount.from_element(el.find("byte-count")),
        )


@dataclass
class FileInfo:
    status: Optional[str] = None
    version: Optional[str] = None
    file_filename: Optional[str] = None
    file_version: Optional[str] = None
    file_type: Optional[str] = None
    file_mime_type: Optional[str] = None
    file_mime_encoding: Optional[str] = None

    @classmethod
    def from_element(cls, el: Optional[ET.Element]) -> "FileInfo":
        if el is None:
            return cls()
        return cls(
            status=_attr(el, "status"),
            version=_attr(el, "version"),
            file_filename=_txt(el.find("file-filename")),
            file_version=_txt(el.find("file-version")),
            file_type=_txt(el.find("file-type")),
            file_mime_type=_txt(el.find("file-mime-type")),
            file_mime_encoding=_txt(el.find("file-mime-encoding")),
        )


@dataclass
class SimpleMagic:
    status: Optional[str] = None
    version: Optional[str] = None
    filename: Optional[str] = None
    mime_type: Optional[str] = None
    message: Optional[str] = None
    simplename: Optional[str] = None

    @classmethod
    def from_element(cls, el: Optional[ET.Element]) -> "SimpleMagic":
        if el is None:
            return cls()
        return cls(
            status=_attr(el, "status"),
            version=_attr(el, "version"),
            filename=_txt(el.find("simplemagic-filename")),
            mime_type=_txt(el.find("simplemagic-mime-type")),
            message=_txt(el.find("simplemagic-message")),
            simplename=_txt(el.find("simplemagic-simplename")),
        )


@dataclass
class DroidResult:
    mimetype: Optional[str] = None
    typename: Optional[str] = None
    puid: Optional[str] = None
    x_version: Optional[str] = None
    method: Optional[str] = None

    @classmethod
    def from_element(cls, el: Optional[ET.Element]) -> "DroidResult":
        if el is None:
            return cls()
        return cls(
            mimetype=_txt(el.find("droid-mimetype")),
            typename=_txt(el.find("droid-typename")),
            puid=_txt(el.find("droid-puid")),
            x_version=_txt(el.find("droid-x-version")),
            method=_txt(el.find("droid-method")),
        )


@dataclass
class Droid:
    container_sigversion: Optional[str] = None
    sigdate: Optional[str] = None
    sigversion: Optional[str] = None
    status: Optional[str] = None
    version: Optional[str] = None
    result: DroidResult = field(default_factory=DroidResult)

    @classmethod
    def from_element(cls, el: Optional[ET.Element]) -> "Droid":
        if el is None:
            return cls()
        return cls(
            container_sigversion=_attr(el, "container-sigversion"),
            sigdate=_attr(el, "sigdate"),
            sigversion=_attr(el, "sigversion"),
            status=_attr(el, "status"),
            version=_attr(el, "version"),
            result=DroidResult.from_element(el.find("droid-result")),
        )


@dataclass
class Jhove:
    builddate: Optional[str] = None
    status: Optional[str] = None
    format: Optional[str] = None
    version: Optional[str] = None
    wellformed: Optional[str] = None
    valid: Optional[str] = None
    mime: Optional[str] = None
    compression: Optional[str] = None
    audio_numchannels: Optional[str] = None
    audio_codec: Optional[str] = None
    audio_abspieldauer: Optional[str] = None
    audio_abtastrate: Optional[str] = None
    audio_bittiefe: Optional[str] = None
    audio_name: Optional[str] = None
    audio_comment: Optional[str] = None
    audio_creationdate: Optional[str] = None
    image_length: Optional[str] = None
    image_width: Optional[str] = None
    color: Optional[str] = None
    bitspersample: Optional[str] = None
    pdf_profile: Optional[str] = None
    cnt_pages: Optional[str] = None
    cnt_images: Optional[str] = None
    cnt_chars: Optional[str] = None
    line_endings: Optional[str] = None

    @classmethod
    def from_element(cls, el: Optional[ET.Element]) -> "Jhove":
        if el is None:
            return cls()
        def g(name: str) -> Optional[str]:
            return _txt(el.find(name))
        return cls(
            builddate=_attr(el, "builddate"),
            status=_attr(el, "status"),
            format=g("jhove-format"),
            version=g("jhove-version"),
            wellformed=g("jhove-wellformed"),
            valid=g("jhove-valid"),
            mime=g("jhove-mime"),
            compression=g("jhove-compression"),
            audio_numchannels=g("jhove-audio-numchannels"),
            audio_codec=g("jhove-audio-codec"),
            audio_abspieldauer=g("jhove-audio-abspieldauer"),
            audio_abtastrate=g("jhove-audio-abtastrate"),
            audio_bittiefe=g("jhove-audio-bittiefe"),
            audio_name=g("jhove-audio_name"),
            audio_comment=g("jhove-audio_comment"),
            audio_creationdate=g("jhove-audio_creationdate"),
            image_length=g("jhove-image-length"),
            image_width=g("jhove-image-width"),
            color=g("jhove-color"),
            bitspersample=g("jhove-bitspersample"),
            pdf_profile=g("jhove-pdf-profile"),
            cnt_pages=g("jhove-cnt-pages"),
            cnt_images=g("jhove-cnt-images"),
            cnt_chars=g("jhove-cnt-chars"),
            line_endings=g("jhove-line-endings"),
        )


@dataclass
class Tika:
    status: Optional[str] = None
    version: Optional[str] = None
    type: Optional[str] = None

    @classmethod
    def from_element(cls, el: Optional[ET.Element]) -> "Tika":
        if el is None:
            return cls()
        return cls(
            status=_attr(el, "status"),
            version=_attr(el, "version"),
            type=_txt(el.find("tika-type")),
        )


@dataclass
class MediaInfo:
    status: Optional[str] = None
    version: Optional[str] = None
    tool_version: Optional[str] = None
    audio_bit_depth: Optional[str] = None
    audio_bit_rate: Optional[str] = None
    audio_channels: Optional[str] = None
    audio_duration: Optional[str] = None
    audio_codec: Optional[str] = None
    audio_sampling_rate: Optional[str] = None
    general_album: Optional[str] = None
    general_performer: Optional[str] = None
    general_track_name: Optional[str] = None
    general_duration: Optional[str] = None
    general_format: Optional[str] = None
    general_overall_bit_rate: Optional[str] = None
    video_bit_rate: Optional[str] = None
    video_color_space: Optional[str] = None
    video_display_aspect_ratio: Optional[str] = None
    video_duration: Optional[str] = None
    video_codec: Optional[str] = None
    video_frame_rate: Optional[str] = None
    video_height: Optional[str] = None
    video_width: Optional[str] = None

    @classmethod
    def from_element(cls, el: Optional[ET.Element]) -> "MediaInfo":
        if el is None:
            return cls()
        def g(name: str) -> Optional[str]:
            return _txt(el.find(name))
        return cls(
            status=_attr(el, "status"),
            version=_attr(el, "version"),
            tool_version=g("Mediainfo-tool-version"),
            audio_bit_depth=g("Audio-bit-depth"),
            audio_bit_rate=g("Audio-bit-rate"),
            audio_channels=g("Audio-channels"),
            audio_duration=g("Audio-duration"),
            audio_codec=g("Audio-codec"),
            audio_sampling_rate=g("Audio-sampling-rate"),
            general_album=g("General-album"),
            general_performer=g("General-performer"),
            general_track_name=g("General-track-name"),
            general_duration=g("General-duration"),
            general_format=g("General-format"),
            general_overall_bit_rate=g("General-overall-bit-rate"),
            video_bit_rate=g("Video-bit-rate"),
            video_color_space=g("Video-color-space"),
            video_display_aspect_ratio=g("Video-display-aspect-ratio"),
            video_duration=g("Video-duration"),
            video_codec=g("Video-codec"),
            video_frame_rate=g("Video-frame-rate"),
            video_height=g("Video-height"),
            video_width=g("Video-width"),
        )


@dataclass
class ExtractedTag:
    name: Optional[str] = None
    value: Optional[str] = None

    @classmethod
    def from_element(cls, el: Optional[ET.Element]) -> "ExtractedTag":
        if el is None:
            return cls()
        return cls(
            name=_txt(el.find("name")),
            value=_txt(el.find("value")),
        )


@dataclass
class XPictoolMetaex:
    status: Optional[str] = None
    version: Optional[str] = None
    extracted_tags: List[ExtractedTag] = field(default_factory=list)

    @classmethod
    def from_element(cls, el: Optional[ET.Element]) -> "XPictoolMetaex":
        if el is None:
            return cls()
        tags = [ExtractedTag.from_element(t) for t in el.findall("extracted-tag")] \
            if el is not None else []
        return cls(
            status=_attr(el, "status"),
            version=_attr(el, "version"),
            extracted_tags=tags,
        )


@dataclass
class LibDimagIdentify:
    guessed_mime_type: Optional[str] = None
    guessed_puid: Optional[str] = None
    guessed_title: Optional[str] = None

    @classmethod
    def from_element(cls, el: Optional[ET.Element]) -> "LibDimagIdentify":
        if el is None:
            return cls()
        return cls(
            guessed_mime_type=_txt(el.find("guessed-mime-type")),
            guessed_puid=_txt(el.find("guessed-puid")),
            guessed_title=_txt(el.find("guessed-title")),
        )


@dataclass
class Datei:
    errors: Optional[int] = None
    filename: Optional[str] = None
    status: Optional[str] = None
    stats: Stats = field(default_factory=Stats)
    file: FileInfo = field(default_factory=FileInfo)
    simplemagic: SimpleMagic = field(default_factory=SimpleMagic)
    droid: Droid = field(default_factory=Droid)
    jhove: Jhove = field(default_factory=Jhove)
    tika: Tika = field(default_factory=Tika)
    mediainfo: MediaInfo = field(default_factory=MediaInfo)
    x_pictool_metaex: XPictoolMetaex = field(default_factory=XPictoolMetaex)
    libDimagIdentify: LibDimagIdentify = field(default_factory=LibDimagIdentify)

    @classmethod
    def from_element(cls, el: Optional[ET.Element]) -> "Datei":
        if el is None:
            return cls()
        return cls(
            errors=_int_from_attr(el, "errors"),
            filename=_attr(el, "filename"),
            status=_attr(el, "status"),
            stats=Stats.from_element(el.find("stats")),
            file=FileInfo.from_element(el.find("file")),
            simplemagic=SimpleMagic.from_element(el.find("simplemagic")),
            droid=Droid.from_element(el.find("droid")),
            jhove=Jhove.from_element(el.find("jhove")),
            tika=Tika.from_element(el.find("tika")),
            mediainfo=MediaInfo.from_element(el.find("mediainfo")),
            x_pictool_metaex=XPictoolMetaex.from_element(el.find("x-pictool-metaex")),
            libDimagIdentify=LibDimagIdentify.from_element(el.find("libDimagIdentify")),
        )


@dataclass
class DateiListe:
    dateien: List[Datei] = field(default_factory=list)

    @classmethod
    def from_element(cls, el: Optional[ET.Element]) -> "DateiListe":
        if el is None:
            return cls()
        files = [Datei.from_element(d) for d in el.findall("datei")]
        # fix attributes not handled inside Datei.from_element
        for i, d_el in enumerate(el.findall("datei")):
            if i < len(files):
                files[i].errors = _int_from_attr(d_el, "errors")
                files[i].filename = files[i].filename or _attr(d_el, "filename")
                files[i].status = files[i].status or _attr(d_el, "status")
        return cls(dateien=files)


def _int_from_attr(el: Optional[ET.Element], name: str) -> Optional[int]:
    if el is None:
        return None
    v = el.get(name)
    try:
        return int(v) if v is not None else None
    except Exception:
        return None


@dataclass
class IdentifyResult:
    worker: Optional[str] = None
    version: Optional[str] = None
    start: Optional[str] = None
    datei_liste: DateiListe = field(default_factory=DateiListe)

    @classmethod
    def from_element(cls, el: ET.Element) -> "IdentifyResult":
        return cls(
            worker=_attr(el, "worker"),
            version=_attr(el, "version"),
            start=_attr(el, "start"),
            datei_liste=DateiListe.from_element(el.find("datei-liste")),
        )


# ============ Parser API ============

def parse_il_results(source: str | bytes | os.PathLike | ET.ElementTree | ET.Element) -> IdentifyResult:
    """Parse an IL results XML input into dataclasses.

    Accepts file path, XML string/bytes, ElementTree, or root Element.
    """
    if isinstance(source, ET.Element):
        root = source
    elif isinstance(source, ET.ElementTree):
        root = source.getroot()
    elif isinstance(source, (str, bytes)) and str(source).lstrip().startswith("<"):
        # XML string
        root = ET.fromstring(source)  # type: ignore[arg-type]
    else:
        # assume path-like
        tree = ET.parse(source)  # type: ignore[arg-type]
        root = tree.getroot()
    return IdentifyResult.from_element(root)
