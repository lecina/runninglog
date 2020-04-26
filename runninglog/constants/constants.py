from runninglog.constants import blockNames

TO_LOAD_FOLDER = "to_load"
JSON_TEMPLATE_OUTPUT_NAME = "template%s.json"

EMPTY_JSON =  \
        "{\n  \"%s\": ,\n  \"%s\": ,\n  \"%s\": ,\n  \"%s\": ,\n  \"%s\": ,\n  \"%s\": ,\n  \"%s\": ,\n  \"%s\": {\n    \"\" : {\"%s\": , \"%s\": \"\"}\n  }\n}"%(blockNames.FileParams.type, blockNames.FileParams.date, blockNames.FileParams.time, blockNames.FileParams.distance, blockNames.FileParams.climb, blockNames.FileParams.where, blockNames.FileParams.notes, blockNames.FileParams.structure, blockNames.FileParams.distance, blockNames.FileParams.pace)
