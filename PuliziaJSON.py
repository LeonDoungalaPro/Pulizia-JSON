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
"[{"type":"header","subtype":"h1","label":" REFERTO DIMISSIONI "},{"type":"date","label":"DATA DI INGRESSO","className":"form-control","name":"DATA_INGRESSO","userData":["2022-12-13"]},{"type":"text","label":"REPARTO DI PROVENIENZA","className":"form-control","name":"REPARTO_PROVENIENZA","subtype":"text","maxlength":250,"userData":["pronto soccorso"]},{"type":"textarea","label":"MOTIVO DEL RICOVERO","className":"form-control","name":"MOTIVO_RICOVERO","subtype":"textarea","maxlength":5000,"rows":3,"userData":["ipertermia abbattimento "]},{"type":"textarea","label":"VALUTAZIONE IN ACCETTAZIONE","className":"form-control","name":"VALUTAZIONE_ACCETTAZIONE","subtype":"textarea","maxlength":5000,"rows":3,"userData":[""]},{"type":"text","label":"MEDICO RESPONSABILE DELL&#96;ACCETTAZIONE","className":"form-control","name":"MEDICO_ACCETTAZIONE","subtype":"text","maxlength":250,"userData":["Dott.ssa Elisa Agostinelli"]},{"type":"textarea","label":"AGGIORNAMENTO DELLA SITUAZIONE CLINICA","className":"form-control","name":"AGGIORNAMENTO_SITUAZIONE","subtype":"textarea","maxlength":5000,"rows":3,"userData":["Peggioramento clinico nonostante la terapia intrapresa"]},{"type":"textarea","label":"PROCEDURA DURANTE IL RICOVERO","className":"form-control","name":"PROCEDURA-DURANTE-IL-RICOVERO","subtype":"textarea","maxlength":5000,"rows":3,"userData":["esami del sangue\r\nesame delle urine \r\necoaddome\r\nrx torace"]},{"type":"textarea","label":"TERAPIE DURANTE IL RICOVERO","className":"form-control","name":"TERAPIE_RICOVERO","subtype":"textarea","maxlength":5000,"rows":3,"userData":["fluidoterapia \r\nantibioticoterapia (doppia copertura antibiotica)\r\nantidolorifico \r\ngastroprotezione"]},{"type":"date","label":"DATA DI USCITA","className":"form-control","name":"DATA_USCITA","userData":["2022-12-17"]},{"type":"text","label":"MEDICO RESPONSABILE","className":"form-control","name":"MEDICO_RESP","subtype":"text","maxlength":250,"userData":["dott.ssa Leila Magurno"]},{"type":"textarea","label":"DIAGNOSI O SOSPETTO DIAGNOSTICO","className":"form-control","name":"DIAGNOSI","subtype":"textarea","maxlength":5000,"rows":3,"userData":["Quadro clinico compatibile con ipertermia febbrile riconducibile a prostatite. Nonostante la terapia antinfiammatoria e la doppia copertura antibiotica il paziente non mostra segni di miglioramento e appare sempre pi&#249; abbattuto. Si sospetta, visto il calo piastrinico, che si stia instaurando una patologia della coagulazione associata al forte stimolo infiammatorio, coadiuvata dalla debolezza generale del paziente ed ad un decadimento delle resistenze immunitarie dovute anche all&#8216;et&#224; avanzata del paziente."]},{"type":"textarea","label":"ESAMI IN CORSO","className":"form-control","name":"ESAMI_CORSO","subtype":"textarea","maxlength":5000,"rows":3,"userData":[""]},{"type":"textarea","label":"TERAPIE DA SOMMINISTRARE A CASA","className":"form-control","name":"TERAPIE_CASA","subtype":"textarea","maxlength":5000,"rows":3,"userData":["continua :\r\ngabapentin 100 2 cps mattina e sera per sempre \r\nalevica 1 cps la sera per 10 giorni \r\nbaytril 150 3/4 o in forma iniettabile 2 ml sottocute la sera per 10 giorni \r\nclavobay 250: una compressa e mezzo ogni 12 ore o in forma iniettabile synulox 2 ml ogni 24 ore per 10 gg\r\nnorvasc 5 1/2 cps la sera per sempre \r\nomeprazolo 20: una compressa al mattino e alla sera per 10 gg\r\ncerenia 60 mg: mezza compressa ogni 24 ore per 10 gg\r\nsenilife plus: 2 birilli al giorno per sempre"]},{"type":"textarea","label":"INDICAZIONE PER IL CLIENTE","className":"form-control","name":"INDICAZIONE-PER-IL-CLIENTE","subtype":"textarea","maxlength":5000,"rows":3,"userData":["Si raccomanda di tenere strettamente monitorato il paziente, avendo cura di valutarne le grandi funzioni organiche. Le dimissioni hanno lo scopo di riportare un paziente con clinica grave in un ambiente familiare, per aiutarne lo stato psicologico in uno stato di malattia avanzato. Qualora dovesse peggiorare si raccomanda di riportarlo in clinica al fine di prestargli tutte le cure necessarie, anche palliative. "]},{"type":"textarea","label":"ULTERIORI INDICAZIONI","className":"form-control","name":"ULTERIORI-INDICAZIONI","subtype":"textarea","maxlength":5000,"rows":3,"userData":[""]},{"type":"header","subtype":"h2","label":"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"},{"type":"header","subtype":"h4","label":"FIRMA VETERINARIO"},{"type":"header","subtype":"h4","label":"_________________________________________"}]"


"""



### USAGE EXEMPLE ###

final_clean_json = DataCleaner(input_string)
print(final_clean_json)
