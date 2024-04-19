import json
import html
import re

def DataCleaner(input_string) -> str:
    """
    Clean and process the input JSON data.

    Args:
    input_string (str): The input JSON data as a string.

    Returns:
    str: The cleaned and processed JSON data as a string, or 0 if the data is empty.
    """
    ############## PARSING ##############
    
    def parse_string_to_json(input_string):
        
        """
        Parse the input string into JSON format.

        Args:
        input_string (str): The input JSON data as a string.

        Returns:
        dict: The parsed JSON data.
        """
        
        input_string = input_string.replace('"[{"type":', '[{"type":').replace('"}]"', '"}]')
        input_string = ' '.join(input_string.split())
        data = []
        lines = input_string.split('\n')  # Split the string into lines
        for line_number, line in enumerate(lines, start=1):
            line = line.strip()
            if line:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    pass
        data = json.dumps(data, indent=4)                
        return json.loads(data)
    
    
    
    ############ CLEANIN  ##############
    
    def strip_html_tags(text):
        
        """
        Remove HTML tags and special characters from the input text.

        Args:
        text (str): The input text containing HTML tags and special characters.

        Returns:
        str: The text with HTML tags and special characters removed.
        """
        text = html.unescape(text)
        text = re.sub(r'<[^>]*>', '', text)
        text = text.replace('\r\n', '.') 
        text = text.replace('Â°C', '°C')  
        text = text.replace('\"', '"') 
        text = text.encode('latin1', 'ignore').decode('utf-8', 'ignore')
        text = text.capitalize()
        return text
            
            
            
            
    def clean_json_file(data):
        """
        Clean the JSON data by removing unnecessary information and formatting the data.

        Args:
        data (list): The input JSON data to be cleaned.

        Returns:
        list: The cleaned JSON data.
        """
        cleaned_data = []
        for item_list in data:
            for item in item_list:
                if isinstance(item, dict) and 'userData' in item and 'label' in item:
                    label = item.get('label')
                    user_data = item.get('userData')
                    if isinstance(user_data, list) and isinstance(label, str):
                        for data_item in user_data:
                            if data_item.strip():  # Check if user data is not empty
                                cleaned_item = {
                                    'label': strip_html_tags(label),
                                    'userData': strip_html_tags(data_item)
                                }
                                cleaned_data.append(cleaned_item)
        cleaned_json = json.dumps(cleaned_data, indent=4)
        return json.loads(cleaned_json)
    
    
    
    
    ########## MAPING ##############
    
    def map_user_data(referto_data, output_data):
        
        """
        Map user data based on reference data and output data.

        Args:
        referto_data (list): The reference data to be mapped.
        output_data (list): The output data used for mapping.

        Returns:
        list: The mapped user data.
        """
        for entry in referto_data:
            for output_entry_list in output_data:
                for output_entry in output_entry_list:
                    if entry.get("label") == output_entry.get("label"):
                        user_data_option = entry.get("userData")
                        values = output_entry.get("values", [])
                        selected_value = next((value.get("value") for value in values if value.get("selected")), None)
                        if selected_value:
                            entry["userData"] = selected_value
                        else:
                            for value in values:
                                if value.get("value") == user_data_option:
                                    entry["userData"] = value.get("label", "")
                                    if not value.get("label"):
                                        entry["userData"] = ""
                                    break
                            else:
                                if user_data_option in [value.get("label") for value in values]:
                                    entry["userData"] = user_data_option
                        break
                else:
                    continue
                break
        return referto_data
    
    
    ########### PROCESSING ##############
    
    def process_file(data, output):
        """
        Process the JSON data and filter out unnecessary information.

        Args:
        data (list): The input JSON data to be processed.
        output (list): The output JSON data used for processing.

        Returns:
        str: The processed JSON data as a string.
        """
        map_user_data(data, output)
        data = [entry for entry in data if not entry.get("userData", "").startswith("option-")]
        filtered_data = [d for d in data if d.get('userData') is not None and d.get('userData') != '']
        result = json.dumps(filtered_data, indent=4)
        
        return result 
    
    output_data = parse_string_to_json(input_string)
    referto_data = clean_json_file(output_data)
    finally_data = process_file(referto_data, output_data)
    cleaned_json = json.dumps(finally_data, indent=4)
    cleaned_json = json.loads(cleaned_json)
    
    if finally_data :
        
        return cleaned_json
    
    else :
        return 0



######################## TESTING #########################

#Insert the input string to use the function

input_string ="""
Insert the input string here to use the function

"""



### USAGE EXEMPLE ###

final_clean_json = DataCleaner(input_string)
print(final_clean_json)
