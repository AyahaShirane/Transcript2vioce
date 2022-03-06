# -*- coding: UTF-8 -*-

import argparse
from pretreatment import run

if __name__ == '__main__':
    parse = argparse.ArgumentParser(prog='Transcript to Speech.', usage='Transcript2vioce.py [-h|--help|args]', description='This is a program use AliYun TTS API to make vioce date.')
    parse.add_argument('input', type=str, help="Input the transcript file.")
    parse.add_argument('-o', '--output', type=str, default='output/', help="You can use this to set your output dir, or the default is \'./output/\'.")
    parse.add_argument('-c', '--config', type=str, default='config.json', help="You can use this to set your config file as you like. The default of the file is config.json. The file will store you AliYun ID and some other configure.")
    parse.add_argument('-t', '--threads', type=int, default=2, help='You can set the number of concurrency. This depends not on your COMPUTER configuration but on your Alibaba Cloud plan type. FREE PLAN JUST OFFER 2----Witch is the default.')
    parse.add_argument('-i', '--intranet', action='store_true', help='If you are in AliYun ShangHai ECS intranet. You can use this flag and this wil change the program into the intranet net. It will be faster and cheaper.')
    parse.add_argument('-f', '--force-restart', action='store_true', help='If you want to restart from the scratch and loss all the progress. You can use this flag')

    args = parse.parse_args()
    print(vars(args))

    run(**vars(args))