from jsonschema import validate, ValidationError
from fastapi import UploadFile
import yaml

#uv run .\validate.py

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
                    "chapter_point": {"type": "string", "pattern": "^[0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}$"},
                    "stills": {"type": "string", "pattern": "^[0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}$"}
                },
                "required": ["chapter_point", "stills"]
            }
        },
        "previews": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "episode": {"type": "integer"},
                    "id": {"type": "string"},
                    "duration_sec": {"type": "integer"},
                    "duration_hms": {"type": "string", "pattern": "^[0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}$"}
                },
                "required": ["episode", "id", "duration_sec", "duration_hms"]
            }
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
                            "burnt_in_subtitles": {"type": "boolean"},
                            "burnt_in_narratives": {"type": "boolean"},
                            "full_subtitles": {"type": "boolean"},
                            "forced_subtitles": {"type": "boolean"}
                        },
                        "required": ["episodes", "spoken_audio", "framerate", "burnt_in_subtitles",
                                     "burnt_in_narratives", "full_subtitles", "forced_subtitles"]
                    }
                },
                "feature": {
                    "type": "object",
                    "properties": {
                        "spoken_audio": {"type": "string"},
                        "frame_rate": {"type": "string"},
                        "burnt_in_subtitles": {"type": "boolean"},
                        "burnt_in_narratives": {"type": "boolean"},
                        "alternate_audio": {"type": "boolean"},
                        "full_subtitles": {"type": "boolean"},
                        "forced_subtitles": {"type": "boolean"}
                    },
                    "required": ["spoken_audio", "frame_rate", "burnt_in_subtitles", "burnt_in_narratives",
                                 "alternate_audio", "full_subtitles", "forced_subtitles"]
                },
                "trailer": {
                    "type": "object",
                    "properties": {
                        "spoken_audio": {"type": "string"},
                        "frame_rate": {"type": "string"},
                        "burnt_in_subtitles": {"type": "boolean"},
                        "burnt_in_narratives": {"type": "boolean"},
                        "alternate_audio": {"type": "boolean"},
                        "full_subtitles": {"type": "boolean"},
                        "forced_subtitles": {"type": "boolean"}
                    },
                    "required": ["spoken_audio", "frame_rate", "burnt_in_subtitles", "burnt_in_narratives",
                                 "alternate_audio", "full_subtitles", "forced_subtitles"]
                }
            },
            "minProperties": 1  # Ensures at least one of episode, feature, or trailer is present
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
                                    "episodes": {"type": "array", "items": {"type": "integer"}},
                                    "crop_top": {"type": "integer"},
                                    "crop_bottom": {"type": "integer"},
                                    "crop_left": {"type": "integer"},
                                    "crop_right": {"type": "integer"}
                                },
                                "required": ["episodes", "crop_top", "crop_bottom", "crop_left", "crop_right"]
                            }
                        },
                        {  # Single object format
                            "type": "object",
                            "properties": {
                                "crop_top": {"type": "integer"},
                                "crop_bottom": {"type": "integer"},
                                "crop_left": {"type": "integer"},
                                "crop_right": {"type": "integer"}
                            },
                            "required": ["crop_top", "crop_bottom", "crop_left", "crop_right"]
                        }
                    ]
                },
                "feature": {
                    "type": "object",
                    "properties": {
                        "crop_top": {"type": "integer"},
                        "crop_bottom": {"type": "integer"},
                        "crop_left": {"type": "integer"},
                        "crop_right": {"type": "integer"}
                    },
                    "required": ["crop_top", "crop_bottom", "crop_left", "crop_right"]
                },
                "trailer": {
                    "type": "object",
                    "properties": {
                        "crop_top": {"type": "integer"},
                        "crop_bottom": {"type": "integer"},
                        "crop_left": {"type": "integer"},
                        "crop_right": {"type": "integer"}
                    },
                    "required": ["crop_top", "crop_bottom", "crop_left", "crop_right"]
                }
            },
            "minProperties": 1  # Ensures at least one of episode, feature, or trailer is present
        }
    },
    "required": ["media_info", "crop_info"]  # Only these two are mandatory
}

async def validate_yaml_schema(file: UploadFile, schema=schema):
    """
    Validates a YAML file from an UploadFile object.
    Ensures the file is not larger than 10MB and has a valid YAML extension.
    Returns the 'title' from the YAML and a validation message.
    """
    title = "N/A"

    # Check file extension
    if not file.filename.lower().endswith((".yaml", ".yml")):
        return title, f"❌ Error: '{file.filename}' is not a valid YAML file (must be .yaml or .yml)."

    # Read the file content
    content = await file.read()

    # Check file size
    if len(content) > MAX_FILE_SIZE:
        return title, f"❌ Error: '{file.filename}' exceeds the maximum file size of 10MB."

    file.seek(0)  # Reset file pointer for further processing

    try:
        # Parse YAML content
        data = yaml.safe_load(content)

        if data is None:
            return title, f"❌ Error: YAML file '{file.filename}' is empty or has invalid content."

        # Extract title if available
        title = data.get("title", "N/A")

    except yaml.YAMLError as e:
        return title, f"❌ YAML Syntax Error in '{file.filename}': {e}"

    # Validate against the schema
    try:
        validate(instance=data, schema=schema)
        return title, f"✅ YAML file '{file.filename}' is valid and follows the schema."
    except ValidationError as e:
        return title, f"❌ Schema validation error in '{file.filename}': {e.message}"

