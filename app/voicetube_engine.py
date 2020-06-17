import requests
from fake_useragent import UserAgent
import bs4
import pandas as pd
import os

relative_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
data_path = os.path.join(relative_path, 'data', '')


def get_fake_user_agent():
    ua = UserAgent()
    return ua.ie

def search(word):

    path = 'https://tw.voicetube.com/definition/' + word
    # look up the dictionary
    try:
        # get request with user agent
        r = requests.get(path, headers={'user-agent': get_fake_user_agent()})
        r.encoding = 'utf-8'
        soup = bs4.BeautifulSoup(r.text, 'lxml')

        rows = []
        def_list = soup.find_all("li", {"class": "word-def-list-defs"})
        for defs in def_list:
            pos = soup.find("span", {"class": "pos"}).text
            definitions = defs.find_all("span", {"class": "definition"})

            definition_list = [d.text for d in definitions]
            # definition = [content.text for content in definitions]
            definition = ''.join([d.replace('；', '/').replace(' ', '') for d in definition_list])
            rows.append(pos + definition)

        definition = ' ; '.join(rows)
        sentence_list = soup.find_all("li", {"class": "word-def-list-example"})
        sentences = '\n'.join([sent.text for sent in sentence_list])

        # print out the results
        print('Definition:\n', definition)
        print('Example:\n', sentences)
        return definition, sentences

    # check if spelling mistakes exist
    except IndexError:
        print('Word not found. Please enter again.')


def lookupEngine():
    while True:
        print('================================\n=VoiceTube Dictionary by Benson=\n================================\n')
        # print("Enter 'q' to quit\n")
        file = pd.read_csv(data_path + 'vocabulary_lookup.csv', encoding='utf-8')

        # enter vocabulary
        word = input('\nEnter a vocabulary:')
        # enter q to quit the program
        if word == 'q':
            print('Thank you!')
            break
        else:
            definition, sentences = search(word)
            add_word_importance(word, definition, sentences)


def check_file_exist():
    if not os.path.isfile(data_path + 'vocabulary_lookup.csv'):
        # create empty cv file
        print('No such file: "vocabulary_lookup.csv".')
        temp = pd.DataFrame(columns=['Vocabulary', 'Definition', 'Example', 'importance'])
        temp.to_csv(data_path + 'vocabulary_lookup.csv', encoding='utf-8', index=False)
        print('File created.')


def add_word_importance(word, definition, sentences):
    file = pd.read_csv(data_path + 'vocabulary_lookup.csv', encoding='utf-8')

    if word in file.Vocabulary.values:
        print('The word is in row', file[file['Vocabulary'] == word].index[0])
    else:
        save = input('\nEnter "Y" to save:')
        if save == 'Y':
            importance = input('\nEnter level of importance(1-3):')
            file.loc[len(file)] = [word, definition, sentences, pd.to_numeric(importance)]
            file.to_csv(data_path + 'vocabulary_lookup.csv', encoding='utf-8', index=False)


def main():
    check_file_exist()
    lookupEngine()

    # definition, sentences = search(word)
    # add_word_importance(word, definition, sentences)


if __name__ == '__main__':

    # search(word='desperate')
    main()
