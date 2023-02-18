"""Data validators for DB Models."""

user_validation_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "title": "User Object Validation",
        "required": ["email", "password", "image", "face_id", "date"],
        "properties": {
            "email": {
                "bsonType": "string",
                "description": "must be an email and is required",
            },
            "password": {
                "bsonType": "object",
                "minLength": 8,
                "description": "must be string with min length 8 symbols and is required",
            },
            "image": {
                "bsonType": "string",
                "description": "must be a link to image and is required",
            },
            "face_id": {
                "bsonType": "array",
                "description": "a list of arrays with face encodings",
                "minItems": 1,
                "items": {
                    "bsonType": "array",
                },
            },
            "date": {
                "bsonType": "date",
                "description": "must be a date object and is required",
            },
        },
    }
}
