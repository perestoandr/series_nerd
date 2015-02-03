import re
from os import listdir
from sys import argv
from apps.main import db, models

def save_srt_to_db(path):
    text = str()
    with open(path) as f:
        for line in f:
            line = line.rstrip()
            if not (re.match('[XY0-9:,>\s-]+$', line) or re.match('<', line)):
                text += line + ' '
    for word in text.split():
        if word[0].isupper():
            try:
                upper_word = models.UpperWords(word=word)
                db.session.add(upper_word)
                db.session.commit()
            except:
                db.session.rollback()
    srt = models.Srt(set_of_words=' '.join(set(text.split())), list_of_words=text)
    db.session.add(srt)
    db.session.commit()

def main():
    if len(argv)==1:
        print('no argumets - nothing to do')
    else:
        for path in listdir(argv[1]):
            if path[len(path)-4:] == '.srt':
                save_srt_to_db(argv[1] + '/' + path)

if __name__ == '__main__':
    main()