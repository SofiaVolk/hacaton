import sys
import re
import pymorphy2 as pm2
from bot import ret_news


def main(msg: str):
    morphy = pm2.MorphAnalyzer()

    if '--NEG:' in msg:
        msg_pos, msg_neg = msg.split('!')
        norm_msg_pos = [morphy.normal_forms(x)[0] for x in re.findall(r"\w+", msg_pos)]
        norm_msg_neg = [morphy.normal_forms(x)[0] for x in re.findall(r"\w+", msg_neg)]
    else:
        norm_msg_pos = [morphy.normal_forms(x)[0] for x in re.findall(r"\w+", msg)]
        norm_msg_neg = ''

    return ret_news(word_tuple=(norm_msg_pos, norm_msg_neg))


if __name__ == "__main__":
    main(sys.argv[1])
