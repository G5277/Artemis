STRICT_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "artemis_resume_output",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "ResumeSuggestions": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "Projects": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "current": {"type": "string"},
                                    "change": {
                                        "type": "string",
                                        "maxLength": 120,
                                        "description": "Rewrite aligned with JD (≤20 words)."
                                    },
                                    "rationale": {
                                        "type": "string",
                                        "maxLength": 60,
                                        "description": "Why this improves ATS/clarity/impact."
                                    },
                                    "jd_alignment": {
                                        "type": "string",
                                        "maxLength": 80,
                                        "description": "Which JD skill/requirement this matches."
                                    }
                                },
                                "required": ["current", "change", "rationale", "jd_alignment"]
                            }
                        },
                        "Experience": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "current": {"type": "string"},
                                    "change": {
                                        "type": "string",
                                        "maxLength": 120,
                                        "description": "Rewrite aligned with JD (≤20 words)."
                                    },
                                    "rationale": {
                                        "type": "string",
                                        "maxLength": 60,
                                        "description": "Why this improves ATS/clarity/impact."
                                    },
                                    "jd_alignment": {
                                        "type": "string",
                                        "maxLength": 80,
                                        "description": "Which JD skill/requirement this matches."
                                    }
                                },
                                "required": ["current", "change", "rationale", "jd_alignment"]
                            }
                        }
                    },
                    "required": ["Projects", "Experience"]
                },
                "CoverLetter": {"type": "string"},
                "Summary": {"type": "string"}
            },
            "required": ["ResumeSuggestions", "CoverLetter", "Summary"]
        }
    }
}
