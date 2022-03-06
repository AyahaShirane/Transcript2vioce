# -*- coding: UTF-8 -*-

from json import load
from pathlib import Path
from treatment import treatment
voice_value = ('xiaoyun','xiaogang','ruoxi','siqi','sijia','sicheng','aiqi','aijia','aicheng','aida','ninger','ruilin','siyue','aiya','aixia','aimei','aiyu','aiyue','aijing','xiaomei','aina','yina','sijing','sitong','xiaobei','aitong','aiwei','aibao','random')     #If you need more, add in this tuple. I get tired to add all. Just make sure 'random' always the last one.

def get_configure(config_path):
    text = {}
    with open(config_path, mode='r', encoding='utf-8') as config_file:
        text = load(config_file)
    if text["format"] in ('wav', 'pcm', 'mp3') and text["sample_rate"] in (8000, 16000) and 0 <= text["volume"] <= 100 and-500 <= text["speech_rate"] <= 500 and -500 <= text["pitch_rate"] <= 500 and text["voice"] in voice_value:
        return text
    else:
        raise TypeError(f'config file ERROR. Read README.md to fix the problem.\n{text}')

def run(input: str, output: str, config: str, threads:int, intranet: bool, force_restart: bool):
    input_path = Path(input)
    output_path = Path(output)
    config_path = Path(config)
    if not output_path.exists():
        output_path.mkdir(exist_ok=True, parents=True)

    if not output_path.is_dir():
        raise TypeError('Output path should be a dir.')
    if input_path.suffix != '.txt':
        raise TypeError('Input path should be a \'.txt\' file.')
    if config_path.suffix != '.json':
        raise TypeError('Configure path should be a \'.json\' file.')

    configure = get_configure(config_path.resolve())
    configure['input_path'] = input_path
    configure['output_path'] = output_path
    configure['threads'] = threads
    configure['force_restart'] = force_restart
    finished_voice = []
    if force_restart:
        for next in output_path.glob(f'*.{configure["format"]}'):
            finished_voice.append(next.stem)
    else:
        pass
    if intranet:
        configure['domain'] = 'nls-gateway.cn-shanghai-internal.aliyuncs.com'
    else:
        configure['domain'] = 'nls-gateway.cn-shanghai.aliyuncs.com'

    treatment(configure, finished_voice)
    
