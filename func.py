# encoding: utf-8
# basic library
import re
import time
import random

# user specific library
import lib as lib
from temp import cnos

__author__ = 'sogo'
cfg_dict = lib.read_config()
_prefix = str(cfg_dict.get('prefix')).replace("'", "")
_save_file_prefix = str(cfg_dict.get('save_file_prefix')).replace("'", "")

def get_cnos(url):
    """
    get ws=x then return cno url list
    :param url: ws
    :return: cno(category number object) url list
    """
    soup = lib.get_bs_object(url=url)
    _return_list = []
    for link in soup.find_all('a'):
        link_txt = link.get('href')
        if 'DNO' in link_txt:
            # DNO 는 상세한 게시물 들어가는 링
            continue
        elif 'CNO' in link_txt:
            # print('\t[CNO] {}'.format(link_txt))
            # link split
            splitted = link_txt.split('&')
            for query in splitted:
                if 'CNO' in query:
                    try:
                        cate_no = int(re.search(r'\d+', query).group())
                        if cate_no >= 300:
                            print(link_txt)
                            _return_list.append(link_txt)
                    except AttributeError:
                        break
                else:
                    pass
        else:
            # print(link_txt)
            pass
    return _return_list

def write_board_item(url):
    """

    :param url:
    :return: if success return True, else False
    """
    global _prefix
    # open file
    with open('item_list.txt', "a+") as file:
        soup = lib.get_bs_object(url=url)
        # type1
        tb_list = soup.find_all('table', {'class': 'board-list'})
        # type2
        ul_list  = soup.find_all('ul', {'class': 'thum-list2'})
        ul_list2 = soup.find_all('ul', {'class': 'list-thumText2'})
        # if no board in url:
        if len(tb_list) == 0 and len(ul_list) == 0 and len(ul_list2) == 0:
            return False
        elif len(tb_list) != 0:
            _list = tb_list
        elif len(ul_list) != 0:
            _list = ul_list
        elif len(ul_list2) != 0:
            _list = ul_list2
        else:
            print('\t[ERROR] ERROR in {}'.format(url))
            return False
        # else: continue
        for board_obj in _list:
            item = board_obj.find_all('a')
            if len(item) == 0:
                # no item
                print('\t[NOTE] no item in board ({})'.format(url))
                return False
            else:
                # success to write
                for detail in item:
                    # write file http://url/query
                    file.write('{}/{}\n'.format(_prefix, detail.get('href')))
                return True


def get_item_list(cno_list):
    """
    get <a> tags from boards when cno list was given.
    :param cno_list:
    :return: a tag list
    """
    for link in cno_list:
        # get link without session
        _link = link.split('PHP')[0]
        for _index in range(1, 2000):
            # sleep with randrange 1 ~ 2 seconds
            time.sleep(float(random.randrange(10, 20))/10)
            _full_link = '{}{}&BC=|{}'.format(_prefix,
                                              _link,
                                              _index
                                              )
            print('[GET:{}] {}'.format(_index, _full_link))
            r = write_board_item(url=_full_link)
            if r is False:
                break
    return None

def save_item(url, file_name, session=None):
    """

    :param url:
    :param file_name:
    :param session:
    :return:
    """
    soup = lib.get_bs_object(url=url, session_=session)
    with open('./items/' + file_name, 'w') as file:
        contents = soup.find_all('div', {'class': 'board-view'})
        if len(contents) == 0:
            print('\t[ERROR] there is no content in {}'.format(url))
        else:
            # file write
            file.write('<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /></head>')
            for content in contents:
                try:
                    file.write(str(content))
                except RecursionError:
                    print('\t[ERROR] Recursion error occurred. Please check {}'.format(url))
                    break
            file.write('</html>')

def save_articles(file_position):
    """

    :param file_position:
    :return:
    """
    global _save_file_prefix

    with open(file_position, 'r') as file:
        _idx = 0
        for line in file:
            if _idx <= 12640:
                # if something is happened continue pass through.
                _idx += 1
                continue
            _url = line.split('PHP')[0]
            session = None
            if _idx % 143 == 0:
                print('\t[IDX:{}({:.2f}%)] session refresh'.format(_idx, float(_idx)*100/12967))
                session = lib.requests.Session()

            # save file
            _file_name = '{}_{}.html'.format(_save_file_prefix, _idx)
            # wait for a few moments
            _wait = float(random.randrange(5, 25))/10
            print('[SAVE] saving <{}> and wait {:.2f} seconds. ({:.2f}%)'.format(_file_name,
                                                                                 _wait,
                                                                                 float(_idx)*100/12967))
            save_item(url=_url, file_name=_file_name, session=session)
            # sleep with randrange 1 ~ 4 seconds
            time.sleep(_wait)
            _idx += 1


def test_base():
    global cfg_dict
    _url1 = cfg_dict.get('test1')
    _article_url = cfg_dict.get('test2')

    # get_cnos(_url1)
    # get_item_list(cno_list=cnos)
    # save_item(url=_article_url, file_name='test.html')
    save_articles('./item_list.txt')
    pass

if __name__ == "__main__":
    test_base()
