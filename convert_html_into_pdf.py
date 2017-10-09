# encoding: utf-8
import html_edit as html_edit
import lib as lib

__desc__ = '원래 여기다가 구성하려고 했는데 func에서 테스트하느라 구현 다 해서 의미 없이 쓰고 있는 함수. 누추하지만 들어오쇼.'
__author__ = 'sogo'
cfg_dict = lib.read_config()
_prefix = str(cfg_dict.get('prefix')).replace("'", "")
_save_file_prefix = str(cfg_dict.get('_save_file_prefix')).replace("'", "")
_href_site = str(cfg_dict.get('_href_site')).replace("'", "")

import pdfkit
options = {
    'page-size': 'A4',
    'margin-top': '0.40in',
    'margin-bottom': '0.0in',
    'margin-right': '0.40in',
    'margin-left': '0.40in',
    'encoding': "UTF-8",
    'no-outline': None,
    'dpi': 400,
    'load-media-error-handling': 'ignore',
    'load-error-handling': 'ignore'
}

def main():
    fl = html_edit.get_file_list('./items/')
    # split into chunks
    _size = 50
    r = lib.chunks(fl, size=_size)
    # pdfkit.from_file(fl[:100], './pdfs/{}_{}.pdf'.format(_prefix, _idx), options=options, toc=toc)

    import time
    _idx = 0
    for chunk in r:
        _idx += 1
        toc = {
            'load-media-error-handling': 'ignore',
            'load-error-handling': 'ignore'
        }
        print('{} >>> {} ({:.2f}%)'.format(_idx*_size, len(fl), float(_idx*_size)*100/len(fl)))
        try:
            pdfkit.from_file(chunk, './pdfs/{}_{}.pdf'.format(_prefix, _idx), options=options, toc=toc)
        except IOError:
            print('\t[IOERROR] Error in this index: {}'.format(_idx))
            continue
        time.sleep(3)

if __name__ == "__main__":
    main()
