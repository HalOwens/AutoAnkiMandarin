import genanki
import requests

def notVowelorDig(char):
    if char == 'a' or char == 'i' or char == 'o' or char == 'e' or char == 'u' or str.isdigit(char):
        return False
    else:
        return True


a_tones = ['ā', 'á', 'ǎ', 'à', 'a']
o_tones = ['ō', 'ó', 'ǒ', 'ò', 'o']
e_tones = ['ē', 'é', 'ě', 'è', 'e']
i_tones = ['ī', 'í', 'ǐ', 'ì', 'i']
u_tones = ['ū', 'ú', 'ǔ', 'ù', 'u']

initialUrl = "https://www.mdbg.net/chinese/rsc/audio/voice_pinyin_pz/"
failUrl = "https://www.mdbg.net/chinese/rsc/audio/voice_pinyin_cl_mdbg/"

mandarin_model = genanki.Model(
    1607392319,
    'Mandarin Py',
    fields=[
        {'name': 'English'},
        {'name': 'Pinyin'},
        {'name': 'Character'},
        {'name': 'Sound'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Pinyin}}<br>{{Sound}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{English}}<br>{{Character}}',
        },
        {
            'name': 'Card 2',
            'qfmt': '{{Character}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Pinyin}}<br>{{English}}<br>{{Sound}}',
        },
        {
            'name': 'Card 3',
            'qfmt': '{{English}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Pinyin}}<br>{{Character}}<br>{{Sound}}',
        },
        {
            'name': 'Card 4',
            'qfmt': '{{Sound}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{English}}<br>{{Character}}<br>{{Pinyin}}',
        },
    ],
    css=
    ".card {\
     font-family: arial;\
     font-size: 52px;\
     text-align: center;\
     color: black;\
     background-color: white;\
    }\
    img { display: block; max-width: 25%; max-height: none; margin-left: auto; margin: 10px auto 10px auto;}\
    img:active { width: 100%; }"
)

my_deck = genanki.Deck(2059400110, "Mandaring Waiting room")

print("If you overestimate tough shit this code will crash cause it's ass")
cards = input("Please enter the number of cards you'd like to make: ")
for x in range(int(cards)):
    noAudio = False
    definition = input("Enter the Definition: ")
    characters = input("Enter the Characters: ")
    pinyins = input("Enter the Pinyin separated by spaces: ")
    pinyins = pinyins.split()
    noAudio = [False for i in range(len(pinyins))]
    newStr = ""
    idx = 0
    for pinyin in pinyins:
        mp3 = requests.get(initialUrl + pinyin + ".mp3")
        if mp3.status_code == 404:
            mp3 = requests.get(failUrl + pinyin + ".mp3")
            if mp3.status_code == 404:
                print("Unable to retrieve audio files")
                noAudio[idx] = True
        with open("/home/halowens/Music/AnkiSourceFiles/" + pinyin + ".mp3", "wb") as file:
            file.write(mp3.content)

        tone = None
        for tone in pinyin:
            pass
        tone = int(tone)

        toneAssigned = False
        lastVowel = None
        for char in enumerate(pinyin):
            if str.isdigit(char[1]):
                break
            if char[1] == 'a':
                newStr += a_tones[tone - 1]
                toneAssigned = True
            elif char[1] == 'e':
                newStr += e_tones[tone - 1]
                toneAssigned = True
            elif char[1] == 'o' and pinyin[char[0] + 1] == 'u':
                newStr += o_tones[tone - 1]
                toneAssigned = True
            elif notVowelorDig(pinyin[char[0] + 1]) and (char[1] == 'o' or char[1] == 'u' or char[1] == 'i'):
                if char[1] == 'i':
                    newStr += i_tones[tone-1]
                elif char[1] == 'o':
                    newStr += o_tones[tone-1]
                elif char[1] == 'u':
                    newStr += u_tones[tone-1]
            elif not str.isdigit(char[1]):
                newStr += char[1]
        idx += 1

    idx = 0
    audioStr = ""
    for pinyin in pinyins:
        if noAudio[idx]:
            audioStr += " + " + pinyin
        else:
            audioStr += "[sound:" + pinyin + ".mp3]"
        idx += 1
    new_note = genanki.Note(model=mandarin_model, fields=[definition, newStr, characters, audioStr])
    my_deck.add_note(new_note)
    print("+=+=Next Word=+=+")

genanki.Package(my_deck).write_to_file('/home/halowens/Documents/Anki/output.apkg')
print("Succesfully generated new deck")
