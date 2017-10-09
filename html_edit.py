# coding: utf-8
from bs4 import BeautifulSoup
import glob
import lib as lib

__author__ = 'sogo'
cfg_dict = lib.read_config()
_prefix = str(cfg_dict.get('prefix')).replace("'", "")

def get_file_list(dir):
    """
    get file list
    :param dir:
    :return: item directory list
    """
    r = glob.glob('{}/*.html'.format(dir))
    return r


def insert_new_tag_into_header(file_name):
    """

    :param file_name:
    :return:
    """
    # read content
    content = None
    with open(file_name, 'r') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'html.parser')

    # insert content
    meta = soup.find('meta')
    css = soup.new_tag('link')
    css['rel'] = 'stylesheet'
    css['type'] = 'text/css'
    css['href'] = './meta.css'
    try:
        meta.insert_after(css)
    except AttributeError:
        print('[ERROR] {}'.format(file_name))
        raise AttributeError
    # write file
    with open(file_name, 'w') as file:
        file.write(str(soup))


def change_image_href(file_name):
    """

    :param file_name:
    :return:
    """
    global _prefix
    # read content
    content = None
    with open(file_name, 'r') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'html.parser')

    # replace content
    for img in soup.find_all('img'):
        try:
            _img_src = img['src']
        except KeyError:
            print(img)
            print('[ERROR] please check {}\n'.format(file_name))
            continue
        if '' in img['src']:
            pass
        elif _prefix in img['src']:
            pass
        else:
            img['src'] = '{}{}'.format(_prefix, img['src'])
    # replace a tag
    for a in soup.find_all('a'):
        try:
            _href = a['href']
        except KeyError:
            print(a)
            print('[ERROR] please check {}\n'.format(file_name))
            continue
        if '' in a['href']:
            pass
        elif _prefix in a['href']:
            pass
        else:
            a['href'] = '{}{}'.format(_prefix, a['href'])
    # replace so much /br into none
    soup = str(soup).replace('</br>', '')

    # write file
    with open(file_name, 'w') as file:
        file.write(str(soup))


def main():
    fl = get_file_list('./items/')
    for dir in fl:
        change_image_href(dir)
    pass
    # change_image_href('./items/test1.html')

if __name__ == "__main__":
    main()
