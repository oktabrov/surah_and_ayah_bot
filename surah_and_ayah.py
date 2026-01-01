import requests         
import json
def get_user_info(surah: int, ayah: int | None = ' ') -> bool:
    '''Takes information from the user and checks it'''
    if not 0<surah<115:
        raise OverflowError(f"Invalid number: Surah must be between 1 and 114")
    url = f"https://api.alquran.cloud/v1/surah/{surah}/en.asad"
    response = requests.get(url)
    max_ayah_number = json.loads(response.text)["data"]["numberOfAyahs"]
    if not 0<ayah<max_ayah_number+1:
        raise OverflowError(f"Invalid number: Ayah must be between 1 and {max_ayah_number}")
    return True
def get_data(url: str) -> str:
    '''Gets data from the given url'''
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Invalid API key: {response.status_code}")
def process_data(data: str) -> list:
    '''Takes the raw data and returns the most important information as a list'''
    surah_number = data['data']['surah']['number']
    text = data['data']['text']
    serial_number = data['data']['number'] # “You are number 12”
    data_surah = data['data']['surah']
    index_of_en_name = list(data_surah.keys())[2]
    english_name = data_surah[index_of_en_name]
    ayah_number = data['data']['numberInSurah']
    english_translation = data['data']['surah']['englishNameTranslation']
    surah_name = data['data']['surah']['name']
    return [surah_number, text, serial_number, english_name, ayah_number, english_translation, surah_name]
def display_results_less(list_of_data):
    formatted_info = f'''<b>ARABIC:</b>
<blockquote>{list_of_data[7]}</blockquote>

<b>ENGLISH:</b>
<blockquote>{list_of_data[1].strip('"').strip("'")}</blockquote>'''
    return formatted_info
def display_results(list_of_data):
    formatted_info = f'''{'INFORMATION'.center(50, '-')}
<b>Surah number:</b> <code>{list_of_data[0]}</code>
<b>Ayah number:</b>  <code>{list_of_data[4]}</code>
<b>Surah name:</b>   <code>{list_of_data[6]}</code>
<b>English name:</b>   <code>{list_of_data[3]}</code>
<b>English translation:</b>   <code>{list_of_data[5]}</code>

{'AYAH'.center(50, '-')}
<b>ARABIC:</b>
<blockquote>{list_of_data[7]}</blockquote>
<b>ENGLISH:</b>
<blockquote>{list_of_data[1].strip('"').strip("'")}</blockquote>

{'ADDITIONAL INFO'.center(50, '-')}
<b>Ayah's position in Qur'an:</b> <code>{list_of_data[2]}</code>'''
    return formatted_info
# Main function which takes suitable data from various functions and gives appropriate arguments to other functions
def main(surah: int, ayah: int, is_more_info: bool):
    try:
        get_user_info(surah, ayah)
    except OverflowError as error:
        return str(error)
    except Exception as error:
        return f"You entered invalid number: {error}"
    url1 = f"https://api.alquran.cloud/v1/ayah/{surah}:{ayah}/en.asad"
    url2 = f"https://api.alquran.cloud/v1/ayah/{surah}:{ayah}"
    try:
        data = get_data(url1)
        text_arabic = requests.get(url2).json()['data']['text']
    except Exception as error:
        return str(error)
    try:
        processed_data_list = process_data(data)
        processed_data_list.append(text_arabic)
    except Exception as error:
        return str(error)
    try:
        if is_more_info: return display_results(processed_data_list)
        else:            return display_results_less(processed_data_list)
    except Exception as error:
        return str(error)
if __name__ == '__main__': print(main(2, 255, True))