import json
import xml.etree.ElementTree as ET
from pprint import pprint
from qazm import posintput, date_logger



def json_parsing_word(file):
    news_list = []
    for new in json.load(file)['rss']['channel']['items']:
        news_list.append(new['description'])
    return news_list

def xml_parsing_word(file):
    news_list = []
    parcer = ET.XMLParser(encoding='utf-8')
    tree = ET.parse(file, parcer)
    root = tree.getroot()
    for new in root.findall('channel/item/description'):
        news_list.append(new.text)
    return news_list

def find_top(news_list, number_sign=0, number_top=10):
    words_list = []
    top = []
    #print(news_list)
    for new in news_list:
        #print(new)
        for word in new.split():
            #print(word)
            if len(word) > number_sign:
                words_list.append(word.lower())
    words_set = set(words_list)
    for word in words_set:
        top.append([word,int(words_list.count(word))])
    top.sort(key=lambda i:i[1], reverse=True)
    return top[:number_top]


if __name__ == '__main__':
    while True:
        print('Сейчас попробуем извлечь слова из файлов новостей и составить рейтинг самых популярных слов')
        number_sign = posintput('Введите минимальное количество букв для слов в рейтинге: ')
        number_top = posintput('Введите сколько самых популярных слов будет отображаться в рейтинге: ')

        with date_logger():
            with open('newsafr.json', encoding='utf8') as news_file_json:
                print('Рейтинг по json:')
                for top in find_top(json_parsing_word(news_file_json),number_sign,number_top):
                    print(f' {top[0]} - {top[1]} раз')

            with open('newsafr.xml',encoding='utf8') as news_file_xml:
                print('Рейтинг по xml:')
                for top in find_top(xml_parsing_word(news_file_xml),number_sign,number_top):
                    print(f' {top[0]} - {top[1]} раз')

        if input('Попробуем еще раз?(да/нет)').lower() != 'да':
            break






