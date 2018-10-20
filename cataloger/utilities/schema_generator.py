from cataloger.models import Schema
import openpyxl
import json


"""Takes in a file and parses it and generates a schema."""
class schema_generator:
    
    def build(file,file_name):
        #Depending on the type of the file, it uses a different function to generate the schema.
        if file_name.lower().endswith('.csv'):
            return schema_generator.__csv_schema_generator(file)
        elif file_name.lower().endswith('.json'):
            return schema_generator.__json_schema_generator(file)
        elif file_name.lower().endswith('.xlsx'):
            return schema_generator.__xlsx_schema_generator(file)
        #If there doesn't exist a function for that type of file, no schema is generated.
        return None

    """Takes in a given csv file and returns the schema for it. We are assuming that the top row contains the headers for the sections."""
    def __csv_schema_generator(file):
        try:
            #parses the first line of the file to get all the headers.
            metadata = file.readline().split(',')
            #Will be further implemented in phase 3.
            return schema_generator.__build_schema(metadata)
        except:
            return None
 
    """Takes in a given json file and returns the schema for it."""
    def __json_schema_generator(file):
        data = json.load(file)
        metadata_set = set()
        for datum in data:
            for datum_property in datum:
                metadata_set.add(datum_property)
        metadata_list = list(metadata_set)
        #assumes list of objects with sparsse data
        #OR
        #for data_property in data[0]:
        #    metadata_list.append(data_property)
        #assumes list of objects and that first entry has full list of properties

        return schema_generator.__build_schema(metadata_list)

    """Takes in a given json file and returns the schema for it. We are assuming that the top row of the first worksheet contains the headers for the sections."""
    def __xlsx_schema_generator(file):
        try:
            #Loads the temporary file into a workbook.
            workbook = openpyxl.load_workbook(file)

            #Gets the name of all the sheets in the workbook.
            sheet_names = wb.sheetnames
    
            #The first row on the first sheet is then added into a list.
            metadata_list = list()
            for cell in workbook[sheet_names[0]][1]:
                metadata_list.append(cell)

            return schema_generator.__build_schema(metadata_list)
        except:
            return None

    """Takes in a list words and creates a new schema."""
    def __build_schema(metaData):
        try:
            #Builds the dictionary that represents the schema.
            jsonField = {}
            jsonField['title'] = None
            jsonField['type'] = None
            jsonField['properties'] = []
            for x in metaData:
                jsonField['properties'].append({
                    'name': x,
                    'type': None,
                    'description': None})
            #Creates a new instance of the schema and inserts the dictionary as a json into the field and returns it.
            returned_schema = Schema()
            returned_schema.data = json.dumps(jsonField)
            return returned_schema
        except:
            #Any errors with this process and it returns None to signify the failure.
            return None