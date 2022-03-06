# -*- coding: UTF-8 -*-

from pathlib import Path
from random import randint
import time
# from pretreatment import voice_value
import threading
import API_network

# Token_dict = {}
thread_lock = False

def treatment(configure:dict, finished_voice):
    end_rows = 0
    thread_list = []
    global thread_lock
    # global Token_dict
    Token_dict = API_network.get_token(configure['AccessKeyId'], configure['AccessKeySecret'])
    alive_threads = threading.active_count()
    while Path(configure['input_path']).stat().st_size > end_rows:
        if threading.active_count()-alive_threads > configure['threads']:
            time.sleep(0.1)
            continue
        else:
            text_date, end_rows = get_a_row_text(configure['input_path'], end_rows, finished_voice)
            if text_date == 'empty' or end_rows == -1:
                break
            for t in thread_list:
                if not t.is_alive():
                    thread_list.remove(t)
            if time.time() >= Token_dict['Token']['ExpireTime']-1:
                thread_lock = True
                del Token_dict
                Token_dict = API_network.get_token(configure['AccessId'], configure['AccessKeySecret'])
                # global Token_dict
                thread_lock = False
            thread_running = threading.Thread(target=run_one_thread, args=[configure, text_date, Token_dict])
            thread_running.start()
            thread_list.append(thread_running)
            thread_running.join()
            
        
def get_a_row_text(text_path:Path, start_rows:int, finished):
    with open(text_path, mode="r", encoding='utf-8') as text_file:
        text_file.seek(start_rows)
        while text_path.stat().st_size > text_file.tell():
            result_text = text_file.readline().strip()
            if result_text in finished:
                continue
            else:
                end_rows = text_file.tell()
                return result_text, end_rows
        return 'empty', -1
        

def run_one_thread(configure:dict, input_text:str, Token_dict):
    from pretreatment import voice_value
    if configure['voice'] == 'random':
        configure['voice'] = voice_value[randint(0,len(voice_value)-1)]
    voice_dir = Path(configure['output_path'], configure['voice'])
    if not voice_dir.exists():
        voice_dir.mkdir(parents=True, exist_ok=True)
    url = 'https://' + configure['domain'] + '/stream/v1/tts'
    http_headers = {
        'Content-Type': 'application/json'
        }
    voice_id, voice_text = input_text.split(' ', maxsplit=1)
    post_json = {'appkey':configure['appkey'], 'text':voice_text, 'token':Token_dict['Token']['Id'], 'format':configure['format'], 'sample_rate':configure['sample_rate'], 'voice':configure['voice'], 'volume':configure['volume'], 'speech_rate':configure['speech_rate'], 'pitch_rate':configure['pitch_rate']}
    date_result = API_network.TTS_Ali(configure['domain'], url, http_headers, post_json)
    if date_result != 'ERROR':
        output_path = Path(configure['output_path']/configure['voice'], voice_id+'.'+configure['format'])
        with open(output_path,mode='wb') as voice:
            voice.write(date_result)
        return
    else:
        with open('ERROR_TEXTS.txt', mode='a') as E:
            E.write(input_text+'\n')
        return
        

