import sys
import re
import pymorphy2 as pm2
from bot import ret_news


def main(msg: str):
    morphy = pm2.MorphAnalyzer()
    norm_msg = [morphy.normal_forms(x)[0] for x in re.findall(r"\w+", msg)]
    return ret_news(norm_msg)


if __name__ == "__main__":
    main(sys.argv[1])
