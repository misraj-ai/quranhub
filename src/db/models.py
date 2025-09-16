# Imports (deduplicated and ordered)
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY, JSONB
from sqlalchemy import Column, Integer, Text, ForeignKey, String, ARRAY, UniqueConstraint, Index, Boolean, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from db.session import Base
from sqlalchemy.sql import func
# Constants
SURAT_FOREIGN_KEY = "quranhub_schema.surat.id"
class Ayat(Base):
    __tablename__ = "ayat"
    __table_args__ = {'schema': 'quranhub_schema'}  # Correct way to set schema
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    surat_id = Column(Integer, ForeignKey(SURAT_FOREIGN_KEY), nullable=True)
    edition_id = Column(Integer, ForeignKey("quranhub_schema.edition.id"), nullable=True)
    juz_id = Column(Integer, ForeignKey("quranhub_schema.juz.id"), nullable=True)
    number = Column(Integer, nullable=False, index=True)
    text = Column(Text, nullable=False)
    numberinsurat = Column(Integer, nullable=False, index=True)
    manzil_id = Column(Integer, ForeignKey("quranhub_schema.manzil.id"), nullable=True)
    page_id = Column(Integer, ForeignKey("quranhub_schema.page.id"), nullable=True)
    ruku_id = Column(Integer, ForeignKey("quranhub_schema.ruku.id"), nullable=True)
    sajda_id = Column(Integer, ForeignKey("quranhub_schema.sajda.id"), nullable=True)
    hizbquarter_id = Column(Integer, ForeignKey("quranhub_schema.hizb_quarter.id"), nullable=True)
    hizb_id = Column(Integer, ForeignKey("quranhub_schema.hizb.id"), nullable=True)

    # Relationships
    surat = relationship("Surat", backref="ayat")
    edition = relationship("Edition", backref="ayat")
    juz = relationship("Juz", backref="ayat")
    manzil = relationship("Manzil", backref="ayat")
    page = relationship("Page", backref="ayat")
    ruku = relationship("Ruku", backref="ayat")
    sajda = relationship("Sajda", backref="ayat")
    hizb_quarter = relationship("HizbQuarter", backref="ayat")
    hizb = relationship("Hizb", backref="ayat")


class Edition(Base):
    __tablename__ = "edition"
    __table_args__ = {"schema": "quranhub_schema"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    identifier = Column(String(100), nullable=False, index=True)
    language = Column(String(2), nullable=False, index=True)
    englishname = Column(String(500), nullable=False)
    format = Column(String(50), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)
    bitrates = Column(ARRAY(Integer), nullable=True)
    source = Column(String(500), nullable=True)
    lastupdated = Column(String(50), nullable=True)
    name = Column(String(1000), nullable=False)
    direction = Column(String(3), nullable=True)
    narrator_identifier = Column(String(100), nullable=True, index=True)
    # New relationship field
    reciter_id = Column(Integer, ForeignKey("quranhub_schema.reciter.id"), nullable=True)
    reciter = relationship("Reciter", back_populates="editions")
    tafsir_id = Column(Integer, ForeignKey("quranhub_schema.tafsir.id"), nullable=True)
    tafsir = relationship("Tafsir", back_populates="editions")

class Tafsir(Base):
    __tablename__ = "tafsir"
    __table_args__ = {"schema": "quranhub_schema"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    englishname = Column(String(255), nullable=False)
    image_url = Column(String(1000), nullable=True)

    editions = relationship("Edition", back_populates="tafsir")


class Reciter(Base):
    __tablename__ = "reciter"
    __table_args__ = {"schema": "quranhub_schema"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    englishname = Column(String(255), nullable=False)
    short_description = Column(JSONB, nullable=True)
    image_url = Column(String(1000), nullable=True)

    # Reverse relationship
    editions = relationship("Edition", back_populates="reciter")

class Hizb(Base):
    __tablename__ = "hizb"
    __table_args__ = {"schema": "quranhub_schema"}

    id = Column(Integer, primary_key=True, nullable=False)

class HizbQuarter(Base):
    __tablename__ = "hizb_quarter"
    __table_args__ = {"schema": "quranhub_schema"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

class Juz(Base):
    __tablename__ = "juz"
    __table_args__ = {"schema": "quranhub_schema"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

class Manzil(Base):
    __tablename__ = "manzil"
    __table_args__ = {"schema": "quranhub_schema"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

class NarrationsDifferences(Base):
    __tablename__ = "narrations_differences"
    __table_args__ = {"schema": "quranhub_schema"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    surat_id = Column(Integer, ForeignKey(SURAT_FOREIGN_KEY), nullable=False)
    numberinsurat = Column(Integer, nullable=False)
    edition_id = Column(Integer, ForeignKey("quranhub_schema.edition.id"), nullable=False)
    difference_text = Column(Text, nullable=False)
    difference_content = Column(Text, nullable=False)

    # Relationships
    surat = relationship("Surat", backref="narrations_differences")
    edition = relationship("Edition", backref="narrations_differences")

class NarrationsNumbering(Base):
    __tablename__ = "narrations_numbering"
    __table_args__ = {"schema": "quranhub_schema"}

    # Proper primary key after database ALTER
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    surah_number = Column(Integer, ForeignKey(SURAT_FOREIGN_KEY, ondelete="CASCADE"), nullable=False, index=True)
    quran_hafs = Column("quran-hafs", ARRAY(Integer), nullable=False, default=lambda: [])
    quran_qaloon = Column("quran-qaloon", ARRAY(Integer), nullable=False, default=lambda: [])
    quran_warsh = Column("quran-warsh", ARRAY(Integer), nullable=False, default=lambda: [])
    quran_albazzi = Column("quran-albazzi", ARRAY(Integer), nullable=False, default=lambda: [])
    quran_qunbul = Column("quran-qunbul", ARRAY(Integer), nullable=False, default=lambda: [])
    quran_aldouri = Column("quran-aldouri", ARRAY(Integer), nullable=False, default=lambda: [])
    quran_alsoosi = Column("quran-alsoosi", ARRAY(Integer), nullable=False, default=lambda: [])
    quran_shoba = Column("quran-shoba", ARRAY(Integer), nullable=False, default=lambda: [])

    # Relationship
    surat = relationship("Surat", backref="narrations_numbering")


class Page(Base):
    __tablename__ = "page"
    __table_args__ = {"schema": "quranhub_schema"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

class Ruku(Base):
    __tablename__ = "ruku"
    __table_args__ = {"schema": "quranhub_schema"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

class Sajda(Base):
    __tablename__ = "sajda"
    __table_args__ = {"schema": "quranhub_schema"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recommended = Column(Boolean, nullable=False)
    obligatory = Column(Boolean, nullable=False)

class Surat(Base):
    __tablename__ = "surat"
    __table_args__ = {"schema": "quranhub_schema"}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(1000), nullable=False)
    englishname = Column(String(200), nullable=False)
    englishtranslation = Column(String(500), nullable=False)
    revelationcity = Column(String(15), nullable=False)
    numberofayats = Column(Integer, nullable=True)
    revelation_order = Column(Integer, nullable=True)

class Word(Base):
    __tablename__ = "word"
    __table_args__ = (
        UniqueConstraint('surat_id', 'numberinsurat', 'position', name='uq_word_location'),
        Index('idx_word_surah_ayah_number_position', 'surat_id', 'numberinsurat', 'position'),
        {"schema": "quranhub_schema"},
    )

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    surat_id = Column(Integer, ForeignKey(SURAT_FOREIGN_KEY), nullable=True)
    numberinsurat = Column(Integer, nullable=True)
    position = Column(Integer, nullable=True)
    line_number = Column(Integer, nullable=True)
    text = Column(Text, nullable=True)
    # Database generated column (computed by DB, not SQLAlchemy)
    location = Column(Text, nullable=True)
    tajweed = Column(JSONB, nullable=True)
    v4_img_url = Column(Text, nullable=True)
    rq_img_url = Column(Text, nullable=True)
    qa_img_url = Column(Text, nullable=True)

    # Relationships
    surat = relationship("Surat", backref="words")

    def __repr__(self):
        return f"<Word(id={self.id}, surat_id={self.surat_id}, numberinsurat={self.numberinsurat}, position={self.position}, text='{self.text}')>"

    @property
    def computed_location(self):
        """
        Compute the location string as done by the database generated column
        Format: surat_id:numberinsurat:position
        """
        if all([self.surat_id is not None, self.numberinsurat is not None, self.position is not None]):
            return f"{self.surat_id}:{self.numberinsurat}:{self.position}"
        return None

class QuranPhrase(Base):
    __tablename__ = "quran_phrase"
    __table_args__ = (
        UniqueConstraint('source_surat_id', 'source_numberinsurat', 'source_from_pos', 'source_to_pos', name='uq_quran_phrase_source_span'),
        Index('idx_quran_phrase_source_ayah', 'source_surat_id', 'source_numberinsurat'),
        {'schema': 'quranhub_schema'}
    )

    phrase_id = Column(Integer, primary_key=True, nullable=False)
    source_surat_id = Column(Integer, nullable=False)
    source_numberinsurat = Column(Integer, nullable=False)
    source_from_pos = Column(Integer, nullable=False)
    source_to_pos = Column(Integer, nullable=False)
    surah_count = Column(Integer, nullable=False)
    ayah_count = Column(Integer, nullable=False)
    occurrence_count = Column(Integer, nullable=False)
    created_at = Column(String, nullable=False)

class QuranPhraseOccurrence(Base):
    __tablename__ = "quran_phrase_occurrence"
    __table_args__ = (
        UniqueConstraint('phrase_id', 'surat_id', 'numberinsurat', 'start_pos', 'end_pos', name='uq_quran_phrase_occ_span'),
        Index('idx_quran_phrase_occ_ayah', 'surat_id', 'numberinsurat'),
        Index('idx_quran_phrase_occ_ayah_phrase', 'surat_id', 'numberinsurat', 'phrase_id'),
        Index('idx_quran_phrase_occ_phrase', 'phrase_id'),
        {'schema': 'quranhub_schema'}
    )

    occurrence_id = Column(Integer, primary_key=True, nullable=False)
    phrase_id = Column(Integer, nullable=False)
    surat_id = Column(Integer, nullable=False)
    numberinsurat = Column(Integer, nullable=False)
    start_pos = Column(Integer, nullable=False)
    end_pos = Column(Integer, nullable=False)
    occurrence_idx = Column(Integer, nullable=True)
    created_at = Column(String, nullable=False)


# --- Similar Ayah Matching Tables ---

from sqlalchemy import ForeignKeyConstraint

class QuranAyahMatch(Base):
    __tablename__ = "quran_ayah_match"
    __table_args__ = (
        UniqueConstraint('source_surat_id', 'source_numberinsurat', 'matched_surat_id', 'matched_numberinsurat', name='uq_quran_ayah_match'),
        Index('idx_qam_source', 'source_surat_id', 'source_numberinsurat'),
        Index('idx_qam_matched', 'matched_surat_id', 'matched_numberinsurat'),
        Index('idx_qam_pair', 'source_surat_id', 'source_numberinsurat', 'matched_surat_id', 'matched_numberinsurat'),
        {'schema': 'quranhub_schema'}
    )

    source_surat_id = Column(Integer, primary_key=True, nullable=False)
    source_numberinsurat = Column(Integer, primary_key=True, nullable=False)
    matched_surat_id = Column(Integer, primary_key=True, nullable=False)
    matched_numberinsurat = Column(Integer, primary_key=True, nullable=False)
    matched_words_count = Column(Integer, nullable=False)
    coverage = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(String, nullable=False)


class QuranAyahMatchSpan(Base):
    __tablename__ = "quran_ayah_match_span"
    __table_args__ = (
        UniqueConstraint('source_surat_id', 'source_numberinsurat', 'matched_surat_id', 'matched_numberinsurat', 'start_pos', 'end_pos', name='uq_qams_span'),
        Index('idx_qams_source', 'source_surat_id', 'source_numberinsurat'),
        Index('idx_qams_matched', 'matched_surat_id', 'matched_numberinsurat'),
        Index('idx_qams_pair', 'source_surat_id', 'source_numberinsurat', 'matched_surat_id', 'matched_numberinsurat'),
        {'schema': 'quranhub_schema'}
    )

    source_surat_id = Column(Integer, primary_key=True, nullable=False)
    source_numberinsurat = Column(Integer, primary_key=True, nullable=False)
    matched_surat_id = Column(Integer, primary_key=True, nullable=False)
    matched_numberinsurat = Column(Integer, primary_key=True, nullable=False)
    start_pos = Column(Integer, primary_key=True, nullable=False)
    end_pos = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(String, nullable=False)


class QuranTheme(Base):
    __tablename__ = "quran_theme"
    __table_args__ = (
        UniqueConstraint('name', name='uq_quran_theme_name'),
        Index('idx_quran_theme_keywords_gin', 'keywords', postgresql_using='gin'),
        {'schema': 'quranhub_schema'}
    )

    theme_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(Text, nullable=False)
    keywords = Column(PG_ARRAY(Text), nullable=True)
    total_ayahs = Column(Integer, nullable=True)
    created_at = Column(String, nullable=False)

    ayah_links = relationship("QuranAyahTheme", back_populates="theme")


class QuranAyahTheme(Base):
    __tablename__ = "quran_ayah_theme"
    __table_args__ = (
        Index('idx_qat_ayah', 'surat_id', 'numberinsurat'),
        {'schema': 'quranhub_schema'}
    )

    theme_id = Column(Integer, ForeignKey('quranhub_schema.quran_theme.theme_id'), primary_key=True, nullable=False)
    surat_id = Column(Integer, nullable=False)
    numberinsurat = Column(Integer, nullable=False)
    created_at = Column(String, nullable=False)

    theme = relationship("QuranTheme", back_populates="ayah_links")

# --- Font and Mushaf Layout Models ---



class Font(Base):
    __tablename__ = 'font'
    __table_args__ = {'schema': 'quranhub_schema'}

    font_id = Column(Integer, primary_key=True)
    code = Column(Text, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    category = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    files = relationship('FontFile', back_populates='font', cascade="all, delete-orphan")
    page_files = relationship('FontPageFile', back_populates='font', cascade="all, delete-orphan")
    mushaf_layouts = relationship('MushafLayout', back_populates='font')


class FontFile(Base):
    __tablename__ = 'font_file'
    __table_args__ = (
        UniqueConstraint('font_id', 'kind', 'format', 'archive_ext', name='ux_font_file'),
        {'schema': 'quranhub_schema'}
    )

    file_id = Column(Integer, primary_key=True)
    font_id = Column(Integer, ForeignKey('quranhub_schema.font.font_id', ondelete='CASCADE'), nullable=False)
    kind = Column(Text, nullable=False)
    format = Column(Text, nullable=False)
    archive_ext = Column(Text)
    url = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    font = relationship('Font', back_populates='files')


class FontPageFile(Base):
    __tablename__ = 'font_page_file'
    __table_args__ = (
        UniqueConstraint('font_id', 'page_number', 'format', name='uq_font_page'),
        {'schema': 'quranhub_schema'}
    )

    page_file_id = Column(Integer, primary_key=True)
    font_id = Column(Integer, ForeignKey('quranhub_schema.font.font_id', ondelete='CASCADE'), nullable=False)
    page_number = Column(Integer, nullable=False)
    format = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    font = relationship('Font', back_populates='page_files')


class MushafLayout(Base):
    __tablename__ = 'mushaf_layout'
    __table_args__ = {'schema': 'quranhub_schema'}

    layout_id = Column(Integer, primary_key=True)
    code = Column(Text, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    number_of_pages = Column(Integer, nullable=False)
    lines_per_page = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    font_id = Column(Integer, ForeignKey('quranhub_schema.font.font_id'))

    font = relationship('Font', back_populates='mushaf_layouts')
    lines = relationship('MushafLine', back_populates='layout', cascade="all, delete-orphan")


class MushafLine(Base):
    __tablename__ = 'mushaf_line'
    __table_args__ = (
        UniqueConstraint('layout_id', 'page_number', 'line_number', name='mushaf_line_pkey'),
        {'schema': 'quranhub_schema'}
    )

    layout_id = Column(Integer, ForeignKey('quranhub_schema.mushaf_layout.layout_id', ondelete='CASCADE'), primary_key=True)
    page_number = Column(Integer, primary_key=True)
    line_number = Column(Integer, primary_key=True)
    line_type = Column(Text, nullable=False)
    is_centered = Column(Boolean, nullable=False, default=False)
    surah_number = Column(Integer)
    ext_first_word_id = Column(Integer)
    ext_last_word_id = Column(Integer)

    layout = relationship('MushafLayout', back_populates='lines')

