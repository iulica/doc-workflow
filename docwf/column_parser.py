

class DirectColumnParser():
    """ parse one column, configured by the metadata """

    def __init__(self, column_name, column_index_map):
        self.column_index = column_index_map[column_name.lower()]
    
    def get_value(self, row):
        value = row[self.column_index].value
        if value is None:
            return None
        return str(value).strip()

class ConcatColumnParser():
    """ join several columns into one field, with a given separator """

    def __init__(self, column_names, column_index_map, separator=' '):
        self.direct_parsers = [
            DirectColumnParser(column_name, column_index_map)
            for column_name in column_names]
        self.separator = separator
    
    def get_value(self, row):
        return self.separator.join([
            direct_parser.get_value(row)
            for direct_parser in self.direct_parsers
        ])

class FixedSplitColumnParser():
    """ uses a subpart of a column as a field, with fixed starting point """

    def __init__(self, column, column_index_map, from_index, to_index=None):
        self.direct_parser = DirectColumnParser(column, column_index_map)
        self.from_index = from_index
        self.to_index = to_index
    
    def get_value(self, row):
        value = self.direct_parser.get_value(row)
        return value[self.from_index:self.to_index]

class RemapColumnParser():
    """ remaps the values of a column
    """
    def __init__(self, column, column_index_map, remap_dict, default_value=None):
        self.direct_parser = DirectColumnParser(column, column_index_map)
        self.remap_dict = remap_dict
        self.default_value = default_value
    
    def get_value(self, row):
        value = self.direct_parser.get_value(row)
        return self.remap_dict.get(str(value), self.default_value)

def get_parser_map(column_map_definition, column_index_map, all_columns=True):
    """ Returns a map of parsers for a sheet and a column_map definition
        column_map_definition: defines the parser map
        column_index_map: column index of the sheet

        ...
    """
    parser_map = {}
    if all_columns:
        parser_map = {
            column_name: DirectColumnParser(column_name, column_index_map)
            for column_name in column_index_map.keys()
        }
    for output_name, column_definition in column_map_definition.items():
        parser = None
        if isinstance(column_definition, str):
            parser = DirectColumnParser(column_definition, column_index_map)
        elif isinstance(column_definition, list):
            parser = ConcatColumnParser(column_definition, column_index_map)
        elif isinstance(column_definition, dict):
            parser_type = column_definition.get('type')
            if parser_type == 'fixed':
                parser = FixedSplitColumnParser(
                    column_definition['column'],
                    column_index_map,
                    column_definition['from'],
                    column_definition.get('to'))
            elif parser_type == 'remap':
                parser = RemapColumnParser(
                    column_definition['column'],
                    column_index_map,
                    column_definition['remap'],
                    default_value=column_definition.get('default'))
        if parser is None:
            raise ValueError(output_name, column_definition)
        parser_map[output_name] = parser

    return parser_map
