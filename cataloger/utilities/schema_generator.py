from cataloger.models import Schema
import openpyxl
import json
import logging


class FailedCreatingSchemaException(Exception):
    """The exception raised if there is an error with creating the schema."""
    def __init__(self, *args):
        self.args = args


class SchemaGenerator:
    """Takes in a file and parses it and generates a schema."""
    valid_extensions = ('.csv', '.xlsx', '.json')

    @staticmethod
    def build(file, file_name):
        """Depending on the type of the file, it uses a different function to generate the schema."""
        if file_name.lower().endswith('.csv'):
            return SchemaGenerator.__csv_schema_generator(file)
        elif file_name.lower().endswith('.json'):
            return SchemaGenerator.__json_schema_generator(file)
        elif file_name.lower().endswith('.xlsx'):
            return SchemaGenerator.__xlsx_schema_generator(file)

        # If there doesn't exist a function for that type of file, an exception is raised.
        logging.error('Non-support file type inputted into schema generator: ' + file_name.lower())
        raise FailedCreatingSchemaException("The file isn't a supported type to generate a schema.")

    @staticmethod
    def __csv_schema_generator(file):
        """Takes in a given csv file and returns the schema for it. We are assuming that the top row contains the
        headers for the sections."""
        try:
            # Parses the first line of the file to get all the headers.
            metadata = str(file.readline().decode('utf-8')).strip().split(',')
            # Will be further implemented in phase 3.
            return SchemaGenerator.__build_schema(metadata)
        except Exception as e:
            logging.error('Failed to parse csv file into schema: ' + str(e))
            raise FailedCreatingSchemaException("Failed to create schema from csv file.")

    @staticmethod
    def __json_schema_generator(file):
        """Takes in a given json file and returns the schema for it."""
        try:
            data = json.load(file)
            metadata_set = set()
            try:
                for datum in data['meta']['view']['columns']:
                    metadata_set.add(datum['name'])
            except Exception as e:
                metadata_set.clear()
                for datum in data:
                    if isinstance(datum, str):
                        metadata_set.add(datum)
                    else:
                        for datum_property in datum:
                            metadata_set.add(str(datum_property))

            metadata_list = list(metadata_set)
            # assumes list of objects with sparsse data
            # OR
            # for data_property in data[0]:
            #    metadata_list.append(data_property)
            # assumes list of objects and that first entry has full list of properties

            return SchemaGenerator.__build_schema(metadata_list)
        except Exception as e:
            logging.error('Failed to parse json file into schema: ' + str(e))
            raise FailedCreatingSchemaException("Failed to create schema from json file.")

    @staticmethod
    def __xlsx_schema_generator(file):
        """Takes in a given json file and returns the schema for it. We are assuming that the top row of the first
        worksheet contains the headers for the sections."""
        try:
            # Loads the temporary file into a workbook.
            workbook = openpyxl.load_workbook(file)

            # Gets the name of all the sheets in the workbook.
            sheet_names = workbook.sheetnames
    
            # The first row on the first sheet is then added into a list.
            metadata_list = list()
            for cell in workbook[sheet_names[0]][1]:
                metadata_list.append(str(cell.value))
            return SchemaGenerator.__build_schema(metadata_list)
        except Exception as e:
            logging.error('Failed to parse xlsx file into schema: ' + str(e))
            raise FailedCreatingSchemaException("Failed to create schema from xlsx file.")

    @staticmethod
    def __build_schema(meta_data):
        """Takes in a list words and creates a new schema."""
        
        # Builds the dictionary that represents the schema.
        temporary_dictionary = {'title': None, 'type': None, 'properties': []}
        for x in meta_data:
            temporary_dictionary['properties'].append({
                'name': x,
                'type': None,
                'description': None})
        # Creates a new instance of the schema and inserts the dictionary as a json into the field and returns it.
        returned_schema = Schema()
        returned_schema.data = json.dumps(temporary_dictionary)
        return returned_schema
