def list_to_string(input_list):
    output_string = ''
    if len(input_list) > 1:
        for current_index in input_list:
            output_string += str(current_index) + ','
        output_string = ' " ' + output_string[:-1] + ' " '
    elif len(input_list) == 1:
        output_string = str(input_list[0])
    return output_string


