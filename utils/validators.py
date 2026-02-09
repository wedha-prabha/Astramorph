import os
import json
from jsonschema import validate, ValidationError
from utils.logger import logger

def validate_json(data, schema_path_or_dict):
    """
    Validates a JSON data object against a given JSON schema.

    Args:
        data (dict): The JSON data object to validate.
        schema_path_or_dict (str or dict): Path to JSON schema file or schema dict.

    Raises:
        ValidationError: If the data does not conform to the schema.
        Exception: For other errors during validation.
    """
    try:
        # Load schema if path is provided
        if isinstance(schema_path_or_dict, str):
            with open(schema_path_or_dict, 'r') as f:
                schema = json.load(f)
        else:
            schema = schema_path_or_dict
        
        validate(instance=data, schema=schema)
        logger.info("JSON data validated successfully against schema.")
        return True
    except ValidationError as e:
        logger.error(f"JSON validation error: {e.message}")
        raise ValidationError(f"Data failed schema validation: {e.message}") from e
    except Exception as e:
        logger.error(f"An unexpected error occurred during JSON validation: {e}")
        raise Exception(f"An unexpected error occurred during JSON validation: {e}") from e


# Example usage (for demonstration, not part of the deployed module):
# if __name__ == "__main__":
#     # Example Schema
#     test_schema = {
#         "type": "object",
#         "properties": {
#             "name": {"type": "string"},
#             "age": {"type": "integer", "minimum": 0}
#         },
#         "required": ["name", "age"]
#     }

#     # Valid Data
#     valid_data = {{"name": "Alice", "age": 30}}
#     print("Validating valid_data: {valid_data}".format(valid_data=valid_data)) # FIX: Replaced f-string with .format()
#     try:
#         validate_json(valid_data, test_schema)
#         print("Valid data passed validation.")
#     except (ValidationError, Exception) as e:
#         print("Valid data failed validation unexpectedly: {}".format(e)) # FIX: Replaced f-string with .format()

#     # Invalid Data (missing required field)
#     invalid_data_missing = {{"name": "Bob"}}
#     print("\nValidating invalid_data_missing: {invalid_data_missing}".format(invalid_data_missing=invalid_data_missing)) # FIX: Replaced f-string with .format(), escaped newline
#     try:
#         validate_json(invalid_data_missing, test_schema)
#         print("Invalid data (missing) passed validation unexpectedly.")
#     except ValidationError as e:
#         print("Invalid data (missing) failed validation as expected: {}".format(e.message)) # FIX: Replaced f-string with .format()
#     except Exception as e:
#         print("Invalid data (missing) failed with unexpected error: {}".format(e)) # FIX: Replaced f-string with .format()

#     # Invalid Data (wrong type)
#     invalid_data_type = {{"name": "Charlie", "age": "twenty"}}
#     print("\nValidating invalid_data_type: {invalid_data_type}".format(invalid_data_type=invalid_data_type)) # FIX: Replaced f-string with .format(), escaped newline
#     try:
#         validate_json(invalid_data_type, test_schema)
#         print("Invalid data (type) passed validation unexpectedly.")
#     except ValidationError as e:
#         print("Invalid data (type) failed validation as expected: {}".format(e.message)) # FIX: Replaced f-string with .format()
#     except Exception as e:
#         print("Invalid data (type) failed with unexpected error: {}".format(e)) # FIX: Replaced f-string with .format()

