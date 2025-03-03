from jsonschema import validate, ValidationError
from fastapi import UploadFile
import yaml

# uv run .\validate.py

# Define max file size (10MB = 10 * 1024 * 1024 bytes)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Define the schema for validation
schema = {
    "type": "object",
    "properties": {
        "version": {"type": "number"},
        "title": {"type": "string"},
        "vendor_id": {"type": "string"},
        "chapters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "chapter_point": {
                        "type": "string",
                        "pattern": "^[0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}$",
                    },
                    "stills": {
                        "type": "string",
                        "pattern": "^[0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}$",
                    },
                },
                "required": ["chapter_point", "stills"],
            },
        },
        "previews": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "episode": {"type": "integer"},
                    "id": {"type": "string"},
                    "duration_sec": {"type": "integer"},
                    "duration_hms": {
                        "type": "string",
                        "pattern": "^[0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}$",
                    },
                },
                "required": ["episode", "id", "duration_sec", "duration_hms"],
            },
        },
        "media_info": {
            "type": "object",
            "properties": {
                "episode": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "episodes": {"type": "array", "items": {"type": "integer"}},
                            "spoken_audio": {"type": "string"},
                            "framerate": {"type": "string"},
                            "burnt_in_subtitles": {
                                "oneOf": [{"type": "boolean"}, {"type": "string"}]
                            },
                            "burnt_in_narratives": {
                                "oneOf": [{"type": "boolean"}, {"type": "string"}]
                            },
                            "full_subtitles": {
                                "oneOf": [{"type": "boolean"}, {"type": "string"}]
                            },
                            "forced_subtitles": {
                                "oneOf": [{"type": "boolean"}, {"type": "string"}]
                            },
                        },
                        "required": [
                            "episodes",
                            "spoken_audio",
                            "framerate",
                            "burnt_in_subtitles",
                            "burnt_in_narratives",
                            "full_subtitles",
                            "forced_subtitles",
                        ],
                    },
                },
                "feature": {
                    "type": "object",
                    "properties": {
                        "spoken_audio": {"type": "string"},
                        "frame_rate": {"type": "string"},
                        "burnt_in_subtitles": {
                            "oneOf": [{"type": "boolean"}, {"type": "string"}]
                        },
                        "burnt_in_narratives": {
                            "oneOf": [{"type": "boolean"}, {"type": "string"}]
                        },
                        "alternate_audio": {
                            "oneOf": [{"type": "boolean"}, {"type": "string"}]
                        },
                        "full_subtitles": {
                            "oneOf": [{"type": "boolean"}, {"type": "string"}]
                        },
                        "forced_subtitles": {
                            "oneOf": [{"type": "boolean"}, {"type": "string"}]
                        },
                    },
                    "required": [
                        "spoken_audio",
                        "frame_rate",
                        "burnt_in_subtitles",
                        "burnt_in_narratives",
                        "alternate_audio",
                        "full_subtitles",
                        "forced_subtitles",
                    ],
                },
                "trailer": {
                    "type": "object",
                    "properties": {
                        "spoken_audio": {"type": "string"},
                        "frame_rate": {"type": "string"},
                        "burnt_in_subtitles": {
                            "oneOf": [{"type": "boolean"}, {"type": "string"}]
                        },
                        "burnt_in_narratives": {
                            "oneOf": [{"type": "boolean"}, {"type": "string"}]
                        },
                        "alternate_audio": {
                            "oneOf": [{"type": "boolean"}, {"type": "string"}]
                        },
                        "full_subtitles": {
                            "oneOf": [{"type": "boolean"}, {"type": "string"}]
                        },
                        "forced_subtitles": {
                            "oneOf": [{"type": "boolean"}, {"type": "string"}]
                        },
                    },
                    "required": [
                        "spoken_audio",
                        "frame_rate",
                        "burnt_in_subtitles",
                        "burnt_in_narratives",
                        "alternate_audio",
                        "full_subtitles",
                        "forced_subtitles",
                    ],
                },
            },
            "minProperties": 1,
            "maxProperties": 1,
            "additionalProperties": False
        },
        "crop_info": {
            "type": "object",
            "properties": {
                "episode": {
                    "oneOf": [
                        {  # List format
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "episodes": {
                                        "type": "array",
                                        "items": {"type": "integer"},
                                    },
                                    "crop_top": {"type": "integer"},
                                    "crop_bottom": {"type": "integer"},
                                    "crop_left": {"type": "integer"},
                                    "crop_right": {"type": "integer"},
                                },
                                "required": [
                                    "episodes",
                                    "crop_top",
                                    "crop_bottom",
                                    "crop_left",
                                    "crop_right",
                                ],
                            },
                        },
                        {  # Single object format
                            "type": "object",
                            "properties": {
                                "crop_top": {"type": "integer"},
                                "crop_bottom": {"type": "integer"},
                                "crop_left": {"type": "integer"},
                                "crop_right": {"type": "integer"},
                            },
                            "required": [
                                "crop_top",
                                "crop_bottom",
                                "crop_left",
                                "crop_right",
                            ],
                        },
                    ]
                },
                "feature": {
                    "type": "object",
                    "properties": {
                        "crop_top": {"type": "integer"},
                        "crop_bottom": {"type": "integer"},
                        "crop_left": {"type": "integer"},
                        "crop_right": {"type": "integer"},
                    },
                    "required": ["crop_top", "crop_bottom", "crop_left", "crop_right"],
                },
                "trailer": {
                    "type": "object",
                    "properties": {
                        "crop_top": {"type": "integer"},
                        "crop_bottom": {"type": "integer"},
                        "crop_left": {"type": "integer"},
                        "crop_right": {"type": "integer"},
                    },
                    "required": ["crop_top", "crop_bottom", "crop_left", "crop_right"],
                },
            },
            "minProperties": 1,
            "maxProperties": 1,
            "additionalProperties": False
        },
    },
    "required": ["media_info", "crop_info"],  # Only these two are mandatory
}

class DuplicateKeyError(Exception):
    pass

class UniqueKeyLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                raise DuplicateKeyError(f"Duplicate key found: {key}")
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping

async def validate_yaml_schema(file: UploadFile, schema=schema):
    """
    Validates a YAML file from an UploadFile object.
    Ensures the file is not larger than 10MB and has a valid YAML extension.
    Returns the 'title' from the YAML and a validation message.
    """
    title = "N/A"

    # Check file extension
    if not file.filename.lower().endswith((".yaml", ".yml")):
        return title, "❌ Error: Not a valid YAML file (must be .yaml or .yml)."

    # Read the file content
    content = await file.read()

    # Check file size
    if len(content) > MAX_FILE_SIZE:
        return title, "❌ Error: File exceeds the maximum file size of 10MB."

    file.seek(0)  # Reset file pointer for further processing

    try:
        # Parse YAML content
        data = yaml.load(content, Loader=UniqueKeyLoader)

        if data is None:
            return title, "❌ Error: YAML file is empty or has invalid content."

        # Extract title if available
        title = data.get("title", "N/A")
        
    except DuplicateKeyError as e:
        return title, f"❌ YAML Duplicate Key Error: {e}"        

    except yaml.YAMLError as e:
        return title, f"❌ YAML Syntax Error: {e}"

    # Validate against the schema
    try:
        validate(instance=data, schema=schema)
        return title, "✅ YAML file is valid and follows the schema."
    except ValidationError as e:
        return title, f"❌ Schema Validation Error: {e.message}"
