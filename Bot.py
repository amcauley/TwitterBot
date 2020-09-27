import datetime
import os
import sys

import pandas as pd
import twitter

API_KEY = os.environ.get('TWITTER_BOT_API_KEY')
API_SECRET_KEY = os.environ.get('TWITTER_BOT_API_SECRET_KEY')
ACCESS_TOKEN_KEY = os.environ.get('TWITTER_BOT_ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_BOT_ACCESS_TOKEN_SECRET')

PIC_DIR = os.environ.get('TWITTER_BOT_PIC_DIR')
PIC_DATA_PATH = os.environ.get('TWITTER_BOT_PIC_DATA_PATH')
TEXT_FILE_PATH = os.environ.get('TWITTER_BOT_TEXT_FILE_PATH')

DATETIME_FORMAT = '%Y%m%d%H'

def getPicAndUpdateStats(statFilePath=PIC_DATA_PATH):
    df = pd.read_csv(statFilePath)

    # Add any newly detected files
    for f in os.listdir(PIC_DIR):
        if not f.endswith('.jpg'):
            continue

        if f in df['FileName'].to_list():
            continue

        dfNew = pd.DataFrame({
            'FileName': f,
            'Count': 0,
            'LastUsedDatetime': datetime.datetime.now().strftime(DATETIME_FORMAT),
            },
            index=[0],
        )

        df = pd.concat([df, dfNew], ignore_index=True)

    if df.empty:
        print('No pics found!')
        sys.exit()

    # Drop any entries that don't exist
    validFileNames = []
    for fileName in df['FileName'].to_list():
        if os.path.isfile(os.path.join(PIC_DIR, fileName)):
            validFileNames.append(fileName)

    dfValidPics = df[df['FileName'].isin(validFileNames)]

    minCount = dfValidPics['Count'].min()
    dfCandidates = dfValidPics[dfValidPics['Count'] == minCount]

    dfCandidatesOld = dfCandidates[dfCandidates['LastUsedDatetime'].astype('int') == dfCandidates['LastUsedDatetime'].astype('int').min()]

    selectedFileName = dfCandidatesOld['FileName'].sample().iloc[0]

    df.loc[df['FileName'] == selectedFileName, 'Count'] = minCount + 1
    df.loc[df['FileName'] == selectedFileName, 'LastUsedDatetime'] = datetime.datetime.now().strftime(DATETIME_FORMAT)

    df.to_csv(statFilePath, index=False)

    filePath = os.path.join(PIC_DIR, selectedFileName)
    print(f'New pic: {filePath}')
    return filePath

def getText(textFilePath=TEXT_FILE_PATH):
    df = pd.read_csv(textFilePath)

    minCount = df['Count'].min()
    dfCandidates = df[df['Count'] == minCount]

    dfCandidatesOld = dfCandidates[dfCandidates['LastUsedDatetime'] == dfCandidates['LastUsedDatetime'].min()]

    selectedText = dfCandidatesOld['Text'].sample().iloc[0]
    origText = selectedText

    now = datetime.datetime.now()
    REPLACEMENTS = {
        '<DATE>': now.strftime('%b %d, %Y'),
        '<DAY>': now.strftime('%A'),
        '<YEAR>': now.strftime('%Y'),
    }

    for k, v in REPLACEMENTS.items():
        selectedText = selectedText.replace(k, v)

    df.loc[df['Text'] == origText, 'Count'] = minCount + 1
    df.loc[df['Text'] == origText, 'LastUsedDatetime'] = datetime.datetime.now().strftime(DATETIME_FORMAT)

    df.to_csv(textFilePath, index=False)

    print(f'Text: {selectedText}')
    return selectedText

def run():
    api = twitter.Api(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET_KEY,
        access_token_key=ACCESS_TOKEN_KEY,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )

    api.PostUpdate(
        getText(),
        media=getPicAndUpdateStats(),
    )

if __name__ == "__main__":
    run()
    #print(getText())