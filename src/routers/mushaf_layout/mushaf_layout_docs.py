
APPLICATION_JSON = "application/json"
__all__ = [
    "getMushafLayoutsResponse",
    "getMushafLayoutDetailResponse",
    "getMushafLayoutPageLinesResponse",
    "getMushafLayoutSurahLinesResponse",
    "getMushafLayoutLookupResponse"
]

getMushafLayoutsResponse = {
    200: {
        "description": "Paginated list of mushaf layouts.",
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
                                    {"code": "qpc-v1-15-lines", "name": "Quran Complex V1 ( 1405 print )", "numberOfPages": 604, "linesPerPage": 15, "font": {"code": "qpc-v1", "name": "QPC V1 Font (page by page)", "category": "Page by Page"}},
                                    {"code": "indopak-13-lines-layout-qudratullah", "name": "Indopak 13 lines - Qudratullah", "numberOfPages": 849, "linesPerPage": 13, "font": {"code": "indopak-nastaleeq", "name": "Indopak Nastaleeq font", "category": "Quran"}}
                                ]
                            }
                        }
                    },
                    "empty": {
                        "summary": "No layouts found (404)",
                        "value": {"code": 404, "status": "Not Found", "data": {"total": 0, "items": []}},
                        "status": 404
                    }
                }
            }
        }
    }
}

getMushafLayoutDetailResponse = {
    200: {
        "description": "Mushaf layout detail with resolved font.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "layoutCode": "qpc-v1-15-lines",
                                "name": "Quran Complex V1 ( 1405 print )",
                                "numberOfPages": 604,
                                "linesPerPage": 15,
                                "font": {"code": "qpc-v1", "name": "QPC V1 Font (page by page)", "category": "Page by Page"}
                            }
                        }
                    },
                    "not_found": {
                        "summary": "Layout not found (404)",
                        "value": {"code": 404, "status": "Not Found", "data": "Layout not found."},
                        "status": 404
                    }
                }
            }
        }
    },
    404: {"description": "Layout not found."}
}

getMushafLayoutPageLinesResponse = {
    200: {
        "description": "Lines for a page.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": [
                                {"lineNumber": 1, "lineType": "ayah", "isCentered": False, "surahNumber": 1}
                            ]
                        }
                    },
                    "not_found": {
                        "summary": "Layout or page not found (404)",
                        "value": {"code": 404, "status": "Not Found", "data": "Layout or page not found."},
                        "status": 404
                    }
                }
            }
        }
    },
    404: {"description": "Layout or page not found."}
}

getMushafLayoutSurahLinesResponse = {
    200: {
        "description": "Lines for a surah.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": [
                                {"pageNumber": 1, "lineNumber": 2, "lineType": "ayah", "isCentered": True, "fromWord": 1, "toWord": 5},
                                {"pageNumber": 1, "lineNumber": 3, "lineType": "ayah", "isCentered": True, "fromWord": 6, "toWord": 10},
                                {"pageNumber": 1, "lineNumber": 4, "lineType": "ayah", "isCentered": True, "fromWord": 11, "toWord": 17},
                                {"pageNumber": 1, "lineNumber": 5, "lineType": "ayah", "isCentered": True, "fromWord": 18, "toWord": 23}
                            ]
                        }
                    },
                    "not_found": {
                        "summary": "Layout or surah not found (404)",
                        "value": {"code": 404, "status": "Not Found", "data": "Layout or surah not found."},
                        "status": 404
                    }
                }
            }
        }
    },
    404: {"description": "Layout or surah not found."}
}

getMushafLayoutLookupResponse = {
    200: {
        "description": "Result for /word/{fromWord}/{toWord} page/line spans by word id range (fromWord and toWord as path parameters).",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": [
                                {"pageNumber": 1, "lineNumber": 2, "lineType": "ayah", "isCentered": True, "fromWord": 1, "toWord": 5},
                                {"pageNumber": 1, "lineNumber": 3, "lineType": "ayah", "isCentered": True, "fromWord": 6, "toWord": 10},
                                {"pageNumber": 1, "lineNumber": 4, "lineType": "ayah", "isCentered": True, "fromWord": 11, "toWord": 17},
                                {"pageNumber": 1, "lineNumber": 5, "lineType": "ayah", "isCentered": True, "fromWord": 18, "toWord": 23}
                            ]
                        }
                    },
                    "not_found": {
                        "summary": "No lines found for lookup (404)",
                        "value": {"code": 404, "status": "Not Found", "data": "No lines found for lookup."},
                        "status": 404
                    },
                    "bad_request": {
                        "summary": "Range too large (400)",
                        "value": {"code": 400, "status": "Bad Request", "data": "The difference between toWord and fromWord must not be greater than 20."},
                        "status": 400
                    }
                }
            }
        }
    },
    400: {"description": "The difference between toWord and fromWord must not be greater than 20."},
    404: {"description": "No lines found for lookup."}
}
