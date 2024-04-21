import json
import html
import re


def DataCleaner(input_string) -> str:
    """
    Clean and process input string containing JSON data.

    Args:
        input_string (str): Input string containing JSON data.

    Returns:
        str or None: Cleaned JSON data as a string if successful, None if cleaning failed.
    """
    
    
    ############### Cleaning JSON data #################
    
    
    try:
        def parse_string_to_json(input_string):
            """
            Parse input string into JSON format.

            Args:
                input_string (str): Input string to parse.

            Returns:
                list: Parsed JSON data.
            """
            input_string = input_string.replace('"[{"type":', '[{"type":').replace('"}]"', '"}]').replace("json_compiled","")
            input_string = ' '.join(input_string.split())
            
            data = []
            lines = input_string.split('\n')
          
            for line_number, line in enumerate(lines, start=1):
                line = line.strip()
                line
                if line:
                    data.append(json.loads(line))
                
            return data




        #################### Strip HTML tags and special characters ####################
        
        
        def strip_html_tags(text):
            """
            Strip HTML tags and special characters

            Args:
                text (str): Text containing HTML tags.

            Returns:
                str: Text with HTML tags removed.
            """
            text = html.unescape(text)
            text = re.sub(r'<[^>]*>', '', text)
            text = text.replace('\r\n', '.')
            text = text.replace('Â°C', '°C')
            text = text.replace('\"', '"')
            text = text.encode('latin1', 'ignore').decode('utf-8', 'ignore')
           
            return text




        ############ Cleaning JSON data #################
        
        
        def clean_json(data):
            """
            Clean JSON data.

            Args:
                data (list): JSON data to clean.

            Returns:
                list: Cleaned JSON data.
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
            cleaned_json = json.loads(cleaned_json)
            return cleaned_json


        ################ Mapping user data #################

        def map_user_data(referto_data, output_data):
            """
            Map user data.

            Args:
                referto_data (list): Reference JSON data.
                output_data (list): Output JSON data.

            Returns:
                list: Mapped user data.
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
                referto_data
            return referto_data




        ################# Processing JSON data #################    
        
        
        def process_file(data, output):
            """
            Process JSON data.

            Args:
                data (list): JSON data to process.
                output (list): Output JSON data.

            Returns:
                list: Processed JSON data.
            """
            map_user_data(data, output)
            data = [entry for entry in data if not entry.get("userData", "").startswith("option-")]
            filtered_data = [d for d in data if d.get('userData') is not None and d.get('userData') != '']
            
            result = json.dumps(filtered_data, indent=4)
            return json.loads(result)



        ############# Calling functions #################
        
        output_data = parse_string_to_json(input_string)
        referto_data = clean_json(output_data)
        finally_data = process_file(referto_data, output_data)
        finally_data
        cleaned_json = json.dumps(finally_data, indent=4)
        
        return cleaned_json
    except Exception as e:
        print("An error occurred:", e)
        return None





###################### Examples for testing ######################

input_string = """

Insert JSON data here to be cleaned

"""

"""
cleaned_data = DataCleaner(input_string)
print(cleaned_data)
"""