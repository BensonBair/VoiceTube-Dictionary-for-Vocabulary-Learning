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


def lookupEngine():
    while True:
        print('================================\n=VoiceTube Dictionary by Benson=\n================================\n')
        print("Enter 'q' to quit\n")
        file = pd.read_csv(data_path + 'vocabulary_lookup.csv', encoding='utf-8')

        # enter vocabulary
        word = input('\nEnter a vocabulary:')
        # enter q to quit the program
        if word == 'q':
            print('Thank you!')
            break
        else:
            path = 'https://tw.voicetube.com/definition/' + word
            # look up the dictionary
            try:
                # get request with user agent
                r = requests.get(path, headers={'user-agent': get_fake_user_agent()})
                r.encoding = 'utf-8'
                soup = bs4.BeautifulSoup(r.text, 'lxml')
                meta = soup.find_all('meta')
                # word info happens to be in forth line
                content = str(meta[4])
                # definition & example of the word
                definition = content[content.find('：') + 1:content.find('例句')].replace('； ', '/ ').replace('amp; ', '')[:-2]
                example = content[content.find('例句') + 3:content.find('。') + 1]
                # print out the results
                print('Definition:\n' + definition)
                print('Example:\n' + example)
                # check if the work has been looked up bef
                if word in file.Vocabulary.values:
                    print('The word is in row ' + str(file.loc[file.Vocabulary == word].index.values[0]))
                else:
                    save = input('\nEnter "Y" to save:')
                    if save == 'Y':
                        importance = input('\nEnter level of importance(1-3):')
                        file.loc[len(file)] = [word, definition, example, pd.to_numeric(importance)]
                        file.to_csv(data_path + 'vocabulary_lookup.csv', encoding='utf-8', index=False)
            # check if spelling mistakes exist
            except IndexError:
                print('Word not found. Please enter again.')


def main():
    if not os.path.isfile(data_path + 'vocabulary_lookup.csv'):
        # create empty cv file
        print('NO SUCH FILE: "vocabulary_lookup.csv".')
        temp = pd.DataFrame(columns=['Vocabulary', 'Definition', 'Example', 'importance'])
        temp.to_csv(data_path + 'vocabulary_lookup.csv', encoding='utf-8', index=False)
        print('FILE CRATED.')
    lookupEngine()


if __name__ == '__main__':

    main()