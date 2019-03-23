# -*- coding: utf-8 -*-
import hashlib


def trans_str_to_md5(url: str):
    if isinstance(url, str):
        url = url.encode("utf-8")
    md = hashlib.md5()
    md.update(url)
    return md.hexdigest()


if __name__ == '__main__':
    print(trans_str_to_md5('wsj'))
