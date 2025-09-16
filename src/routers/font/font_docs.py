
APPLICATION_JSON = "application/json"
__all__ = [
    "getFontsResponse",
    "getFontDetailResponse",
    "getFontFilesResponse",
    "getFontPageFilesResponse",
    "getFontFormatsResponse",
    "getFontArchivesResponse",
    "getFontCategoriesResponse",
    "getFontKindsResponse"
]
# Canonical OpenAPI response for /kinds endpoint (List all font kinds)
getFontKindsResponse = {
    200: {
        "description": "List of all font kinds.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": {"code": 200, "status": "OK", "data": ["regular", "pack", "extras"]}
                    }
                }
            }
        }
    },
    404: {
        "description": "No kinds found.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "empty": {
                        "summary": "No kinds found (404)",
                        "value": {"code": 404, "status": "Not Found", "data": []},
                        "status": 404
                    }
                }
            }
        }
    }
}

# Canonical OpenAPI response for /formats endpoint (List all font formats)
getFontFormatsResponse = {
    200: {
        "description": "List of all available font formats.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": {"code": 200, "status": "OK", "data": ["ttf", "woff", "woff2", "otf", "json"]}
                    }
                }
            }
        }
    },
    404: {
        "description": "No formats found.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "empty": {
                        "summary": "No formats found (404)",
                        "value": {"code": 404, "status": "Not Found", "data": []},
                        "status": 404
                    }
                }
            }
        }
    }
}

# Canonical OpenAPI response for /archives endpoint (List all font archive types)
getFontArchivesResponse = {
    200: {
        "description": "List of all available font archive types.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": {"code": 200, "status": "OK", "data": ["zip", "bz2", "none"]}
                    }
                }
            }
        }
    },
    404: {
        "description": "No archive types found.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "empty": {
                        "summary": "No archive types found (404)",
                        "value": {"code": 404, "status": "Not Found", "data": []},
                        "status": 404
                    }
                }
            }
        }
    }
}

# Canonical OpenAPI response for /categories endpoint (List all font categories)

getFontsResponse = {
    200: {
        "description": "Paginated list of fonts.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "total": 2,
                                "items": [
                                    {"code": "digital-khatt-v1", "name": "Digital Khatt V1 Font", "category": "Quran"},
                                    {"code": "qpc-v1", "name": "QPC V1 Font (page by page)", "category": "Page by Page"}
                                ]
                            }
                        }
                    },
                    "filter_example": {
                        "summary": "Filter by fontCode or category",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "total": 1,
                                "items": [
                                    {"code": "qpc-v1", "name": "QPC V1 Font (page by page)", "category": "Page by Page"}
                                ]
                            }
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "No fonts found.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "empty": {
                        "summary": "No fonts found (404)",
                        "value": {"code": 404, "status": "Not Found", "data": {"total": 0, "items": []}},
                        "status": 404
                    }
                }
            }
        }
    }
}

getFontDetailResponse = {
    200: {
        "description": "Font detail with files and page range.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "code": "digital-khatt-v1",
                                "name": "Digital Khatt V1 Font",
                                "category": "Quran",
                                "files": {
                                    "regular": [{"format": "ttf", "url": "https://quranhub.b-cdn.net/quran/fonts/qpc-hafs/regular/qpc-hafs.ttf"}],
                                    "pack": [],
                                    "extras": []
                                },
                                "pageRange": {"min": 1, "max": 604}
                            }
                        }
                    },
                    "not_found": {
                        "summary": "Font not found (404)",
                        "value": {"code": 404, "status": "Not Found", "data": "Font not found."},
                        "status": 404
                    }
                }
            }
        }
    },
    404: {"description": "Font not found."}
}

getFontFilesResponse = {
    200: {
        "description": "List of font files for a font.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": [
                                {"kind": "regular", "format": "ttf", "url": "..."}
                            ]
                        }
                    },
                    "not_found": {
                        "summary": "Font not found (404)",
                        "value": {"code": 404, "status": "Not Found", "data": "Font not found."},
                        "status": 404
                    }
                }
            }
        }
    },
    404: {"description": "Font not found."}
}

getFontPageFilesResponse = {
    200: {
        "description": "Font page files for a given page or paginated list of font page files.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success_page": {
                        "summary": "Canonical success response for a single page",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {"ttf": "...", "woff": "..."}
                        }
                    },
                    "success_paginated": {
                        "summary": "Canonical success response for paginated font page files",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "total": 2,
                                "items": [
                                    {"pageNumber": 1, "format": "ttf", "url": "..."},
                                    {"pageNumber": 2, "format": "woff", "url": "..."}
                                ]
                            }
                        }
                    },
                    "not_found": {
                        "summary": "Font or page not found (404)",
                        "value": {"code": 404, "status": "Not Found", "data": "Font or page not found."},
                        "status": 404
                    }
                }
            }
        }
    },
    404: {"description": "Font or page not found."}
}

getFontFormatsResponse = {
    200: {
        "description": "List of all available font formats.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": {"code": 200, "status": "OK", "data": ["ttf", "woff", "woff2", "otf", "json"]}
                    }
                }
            }
        }
    }
}

getFontArchivesResponse = {
    200: {
        "description": "List of all available font archive types.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": {"code": 200, "status": "OK", "data": ["zip", "bz2", "none"]}
                    }
                }
            }
        }
    }
}

# Canonical response for /categories endpoint
getFontCategoriesResponse = {
    200: {
        "description": "List of all font categories.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": {"code": 200, "status": "OK", "data": ["Quran", "Page by Page", "Surah by Surah"]}
                    }
                }
            }
        }
    },
    404: {
        "description": "No categories found.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "empty": {
                        "summary": "No categories found (404)",
                        "value": {"code": 404, "status": "Not Found", "data": []},
                        "status": 404
                    }
                }
            }
        }
    }
}
