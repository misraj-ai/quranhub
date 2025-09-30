# 🕌 Quran Hub API

<div align="center">

![QuranHub Logo](https://qurani.ai/app-logo.svg)

![QuranHub Logo](https://img.shields.io/badge/QuranHub-API-00897B?style=for-the-badge)
[![License: NCL](https://img.shields.io/badge/License-NCL-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-316192)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%2B-red)](https://www.sqlalchemy.org/)
[![Misraj AI](https://img.shields.io/badge/By-Misraj%20AI-gold)](https://misraj.ai)

**A comprehensive REST API providing access to the Holy Quran in +300 editions across +50 languages**

**Developed and Maintained by [Misraj AI](https://misraj.ai)**

[Documentation](https://qurani.ai) • [Features](#-features) • [Quick Start](#-quick-start) • [API Reference](#-api-documentation) • [MCP Server](#-quranhub-mcp-server) • [License](#-license)

</div>

---

## 📖 Overview

Quran Hub API is a powerful, feature-rich REST API developed by **Misraj AI** that provides comprehensive access to Quranic content, including multiple translations, tafsir (commentaries), audio recitations, and advanced search capabilities. Built with modern Python technologies and PostgreSQL, it serves as a complete backend solution for Islamic applications and research projects.

**Full Documentation**: [https://qurani.ai](https://qurani.ai)

### 📊 Database Statistics

<table>
<tr>
<td>

**Content Coverage**
- 📚 **+430** Total Editions
- 📝 **+342** Text Editions  
- 🔊 **+88** Audio Editions
- 📊 **+354,346** Audio Files

</td>
<td>

**Edition Types**
- 📖 **+156** Tafsir Editions
- 🌍 **+164** Translations
- 🎤 **+45** Surah Recitations
- 📤 **+12** Quran Scripts
- 📿 **+43** Verse-by-Verse
- 🗣️ **+8** Narrations

</td>
</tr>
</table>

## 📖 Quran Hub MCP Server

The Quran Hub MCP Server provides a rich set of tools for accessing and exploring the Quran programmatically. You can use these tools inside Cursor or any other MCP-compatible client.

### ⚙️ Setup

Add the server to your MCP configuration file:

```json
{
  "servers": {
    "quranhub": {
      "type": "http",
      "url": "https://mcp.quranhub.com/mcp"
    }
  }
}
```

The MCP server provides the same comprehensive tools available in the API, allowing seamless integration with compatible development environments and AI assistants.

## ✨ Features

### 🕌 Core Quran Tools
Essential tools for retrieving Quran content by structure.

| Tool | Description | Example Input |
|------|-------------|---------------|
| `get_complete_quran` | Get the entire Quran in default edition | - |
| `get_complete_quran_by_edition` | Get complete Quran in specific edition | `"quran-uthmani"` |
| `get_surah` | Get a complete Surah with all verses | `2` (Al-Baqarah) |
| `get_surah_by_edition` | Get Surah in specific edition | `surah: 1, edition: "en.sahih"` |
| `get_surah_by_multiple_editions` | Get Surah in multiple editions | `surah: 1, editions: "quran-uthmani,en.sahih"` |
| `get_ayah` | Get a specific verse by reference | `"2:255"` |
| `get_ayah_by_edition` | Get ayah in specific edition | `ref: "2:255", edition: "en.sahih"` |
| `get_ayah_by_multiple_editions` | Get ayah in multiple editions | `ref: "2:255", editions: "quran-uthmani,en.sahih"` |
| `get_juz` | Get a complete Juz (1-30) | `3` |
| `get_juz_by_edition` | Get Juz in specific edition | `juz: 1, edition: "en.sahih"` |
| `get_page` | Get a specific Quran page (1-604) | `255` |
| `get_page_by_edition` | Get page in specific edition | `page: 1, edition: "quran-uthmani"` |
| `get_hizb` | Get a Hizb section (1-60) | `15` |
| `get_hizb_by_edition` | Get Hizb in specific edition | `hizb: 1, edition: "quran-uthmani"` |
| `get_hizb_quarter` | Get Hizb Quarter (1-240) | `120` |
| `get_hizb_quarter_by_edition` | Get Hizb Quarter in specific edition | `quarter: 1, edition: "quran-uthmani"` |
| `get_manzil` | Get a Manzil for weekly reading (1-7) | `5` |
| `get_manzil_by_edition` | Get Manzil in specific edition | `manzil: 1, edition: "quran-uthmani"` |
| `get_ruku` | Get a Ruku section | `40` |
| `get_ruku_by_edition` | Get Ruku in specific edition | `ruku: 1, edition: "quran-uthmani"` |

### 🔍 Search & Discovery
Tools to search, explore, and discover Quranic content.

| Tool | Description | Example Input |
|------|-------------|---------------|
| `search_quran` | Search Arabic text and translations | `"mercy"` |
| `get_random_ayah` | Get a random verse | - |
| `get_random_ayah_by_edition` | Random verse in specific edition | `"en.sahih"` |
| `get_random_ayah_by_multiple_editions` | Random verse in multiple editions | `"quran-uthmani,en.sahih"` |
| `get_similar_ayahs_hafs` | Find verses similar to given ayah (Hafs) | `surah: 1, ayah: 1` |
| `get_similar_ayahs_by_edition` | Find similar verses by edition | `surah: 1, ayah: 1, edition: "quran-uthmani"` |
| `get_mutashabihat_phrases_hafs` | Find similar phrases (Hafs) | `surah: 2, ayah: 255` |
| `get_mutashabihat_phrases_by_edition` | Find similar phrases by edition | `surah: 2, ayah: 255, edition: "quran-uthmani"` |
| `get_ayah_themes` | List all available themes | - |
| `get_themes_for_ayah` | Get themes for specific ayah | `surah: 1, ayah: 1` |

### 📚 Editions & Translations
Manage and retrieve different Quran editions, translations, and formats.

| Tool | Description | Example Input |
|------|-------------|---------------|
| `get_all_editions` | List all editions with filters | `language: "en", type: "translation"` |
| `get_all_languages` | Get all supported languages | - |
| `get_editions_by_language` | Editions by language | `"ar"` or `"en"` |
| `get_all_types` | Get edition types | - |
| `get_editions_by_type` | Editions by type | `"translation"` |
| `get_all_formats` | Get edition formats | - |
| `get_editions_by_format` | Editions by format | `"audio"` or `"text"` |
| `get_editions_by_format_and_type` | Editions by format and type | `format: "text", type: "narration"` |
| `get_editions_analysis` | Statistical overview of editions | - |

### 🔊 Audio & Recitation
Access audio recitations and reciter information.

| Tool | Description | Example Input |
|------|-------------|---------------|
| `get_distinct_audio_editions` | List unique audio reciters | - |
| `get_all_narrator_identifiers` | Get all reciter identifiers | - |
| `get_audio_editions_by_narrator` | Audio by specific reciter | `"quran-warsh"` |

### 📖 Special Features
Advanced features for studying and understanding the Quran.

| Tool | Description | Example Input |
|------|-------------|---------------|
| `get_tajweed_rules` | Tajweed rules for specific words | `"1:1:2"` |
| `get_word_line_number` | Line number for word location | `"1:1:2"` |
| `get_word_image` | Word-by-word images | `location: "1:1:2", type: "v4"` |
| `get_all_sajdas` | Get all prostration verses | - |
| `get_sajdas_by_edition` | Sajda verses in specific edition | `"quran-uthmani"` |
| `get_narrations_differences` | Compare different narrations | `page: 1, source: "hafs", target: "warsh"` |

### 📊 Metadata & Structure
Organizational and structural information about the Quran.

| Tool | Description | Example Input |
|------|-------------|---------------|
| `get_quran_metadata` | Complete Quran structure metadata | - |
| `get_all_surahs` | List all 114 Surahs with details | `revelationOrder: false` |
| `get_surahs_by_revelation_city` | Surahs grouped by Meccan/Medinan | - |
| `get_surahs_by_juz` | Surahs organized by Juz | - |
| `get_all_pages_metadata` | Metadata for all 604 pages | - |
| `get_pages_metadata_by_edition` | Page metadata for specific edition | `"quran-uthmani"` |
| `get_all_juzs_metadata` | Metadata for all 30 Juz | - |
| `get_juzs_metadata_by_edition` | Juz metadata for specific edition | `"quran-uthmani"` |
| `get_all_hizbs_metadata` | Metadata for all 60 Hizbs | - |
| `get_hizbs_metadata_by_edition` | Hizb metadata for specific edition | `"quran-uthmani"` |

### 🖋️ Typography & Display
Font resources and page layout information.

| Tool | Description | Example Input |
|------|-------------|---------------|
| `get_font_kinds` | List all font kinds | - |
| `get_font_formats` | List all font formats | - |
| `get_font_archives` | List all font archive types | - |
| `get_font_categories` | List all font categories | - |
| `get_font_detail` | Get specific font details | `"uthmani"` |
| `get_font_files` | List font files for download | `fontCode: "uthmani"` |
| `get_font_page_files` | Get font files for specific page | `font: "uthmani", page: 1` |
| `list_font_page_files` | List paginated font files | `font: "uthmani", format: "ttf"` |

### 📝 Mushaf Layouts
Page layout and line structure information.

| Tool | Description | Example Input |
|------|-------------|---------------|
| `list_mushaf_layouts` | List mushaf page layouts | `linesPerPage: 15` |
| `get_layout_detail` | Specific layout information | `"hafs_15"` |
| `get_layout_page_lines` | Line structure for pages | `layout: "hafs_15", page: 1` |
| `get_layout_surah_lines` | Line structure for surah | `layout: "hafs_15", surah: 1` |
| `layout_word_lookup` | Find page/line by word position | `layout: "hafs_15", from: 1, to: 7` |

### 🔧 Utility Functions
Basic utility and test functions.

| Tool | Description | Example Input |
|------|-------------|---------------|
| `get_response` | Basic API response test | - |

For complete API documentation and additional features, visit [https://qurani.ai](https://qurani.ai)


## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/misraj-ai/quranhub-api.git
cd quranhub-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your PostgreSQL database credentials
```

5. **Set up PostgreSQL database**
```bash
# Create database
createdb quranhub

# Import the database snapshot
psql -U your_user -d quranhub -f database/quranhub_snapshot_dump.sql
```

6. **Run the application**
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8080`

### 🐳 Docker Installation

```bash
# Build and run with Docker Compose
docker-compose up -d

# The API will be available at http://localhost:8080
# API documentation at http://localhost:8080/docs
```

## 📚 API Documentation

### Interactive Documentation
- **Full Documentation**: [https://qurani.ai](https://qurani.ai)
- **Swagger UI**: `https://api.quranhub.com/docs`

### Example Requests

#### Get Surah Al-Fatiha in English
```bash
curl -X GET "https://api.quranhub.com/v1/surah/1/en.sahih"
```

#### Search for verses about "mercy"
```bash
curl -X GET "https://api.quranhub.com/v1/search/mercy?language=en"
```

#### Get random verse in multiple editions
```bash
curl -X GET "https://api.quranhub.com/v1/ayah/random/editions/quran-uthmani,en.sahih"
```

## 📄 License

**License: NCL — Non-Commercial License**

This project is licensed under the Non-Commercial License (NCL). You may use, copy, modify, and distribute this software for non-commercial purposes only.

Commercial use, including but not limited to selling, sublicensing, or using the software as part of a commercial product or service, is strictly prohibited without explicit written permission from Misraj AI.

For commercial licensing, please contact:
- **Email**: hello@misraj.ai
- **Website**: [https://misraj.ai](https://misraj.ai)

See the [LICENSE](LICENSE) file for full terms and conditions.

## 🤝 Contributing

While this is proprietary software, we welcome bug reports and feature suggestions:

1. **Bug Reports**: Please open an issue with detailed information
2. **Feature Requests**: Submit via GitHub issues with use case description
3. **Security Issues**: Email hello@misraj.ai directly

For accepted contributions, contributors will need to sign a Contributor License Agreement (CLA) transferring rights to Misraj AI.

## 📞 Support

- **Documentation**: [https://qurani.ai](https://qurani.ai)
- **Issues**: [GitHub Issues](https://github.com/misraj-ai/quranhub/issues)
- **Commercial Support**: hello@misraj.ai
- **Website**: [https://misraj.ai](https://misraj.ai)

---

<div align="center">

**Developed with ❤️ by [Misraj AI](https://misraj.ai)**

**© 2025 Misraj AI. All Rights Reserved.**

[⬆️ Back to Top](#-quranhub-api)

</div>