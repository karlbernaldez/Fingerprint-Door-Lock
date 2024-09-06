"""Data validators for DB Models."""

user_validation_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "title": "User Object Validation",
        "required": ["email", "password", "fingerprint_id", "date"],
        "properties": {
            "email": {
                "bsonType": "string",
                "minLength": 6,
                "description": "must be an email and is required",
            },
            "password": {
                "bsonType": "string",
                "minLength": 8,
                "description": "must be a string with min length 8 symbols and is required",
            },
            "fingerprint_id": {
                "bsonType": "binData",
                "description": "pickled np.array type for fingerprint data and is required",
            },
            "date": {
                "bsonType": "date",
                "description": "must be a date object and is required",
            },
        },
    }
}
