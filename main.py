import genanki
import requests
import re

a_tones = ['ā', 'á', 'ǎ', 'à', 'a']
o_tones = ['ō', 'ó', 'ǒ', 'ò', 'o']
e_tones = ['ē', 'é', 'ě', 'è', 'e']
i_tones = ['ī', 'í', 'ǐ', 'ì', 'i']
u_tones = ['ū', 'ú', 'ǔ', 'ù', 'u']
v_tones = [' ', 'ǘ', 'ǚ', 'ǜ', ' ']

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

print("To stop making cards put exit into the definition field")
definition = str()
while definition != "exit":
    noAudio = False
    definition = input("Enter the Definition: ")
    if definition == "exit":
        break
    characters = input("Enter the Characters: ")
    pinyinIn = input("Enter the Pinyin: ")
    searchPage = requests.get("https://www.trainchinese.com/v2/search.php?searchWord=" + pinyinIn +"&rAp=0&height=0&width=0&tcLanguage=en")
    try:
        url = re.findall('playAudio\("(.*?)"', searchPage.text)[0]
        number = re.findall('[0-9]*', url)[0]
        number = number[-3:]
        url = "https://www.trainchinese.com/v1/word_lists/tc_words/w_dirs/w" + number + "/" + url
        mp3 = requests.get(url)
    except:
        print("Error was unable to find the audio")
    with open("/home/halowens/Music/AnkiSourceFiles/" + pinyinIn + ".mp3", "wb") as file:
        file.write(mp3.content)
    pinyins = re.findall('(.*?[1-5])', pinyinIn)
    newStr = str()
    for pinyin in pinyins:
        tone = int(pinyin[-1])
        lastVowel = None
        vowelType = None
        for char in enumerate(pinyin):
            if str.isdigit(char[1]):
                break
            if char[1] == 'a':
                lastVowel = char[0]
                vowelType = 0
                break
            elif char[1] == 'e':
                lastVowel = char[0]
                vowelType = 1
                break
            elif char[1] == 'u' and pinyin[char[0] - 1] == 'o':
                lastVowel = char[0] - 1
                vowelType = 2
            elif char[1] == 'o':
                lastVowel = char[0]
                vowelType = 2
            elif char[1] == 'u':
                lastVowel = char[0]
                vowelType = 3
            elif char[1] == 'i':
                lastVowel = char[0]
                vowelType = 4
            elif char[1] == 'v':
                lastVowel = char[0]
                vowelType = 5
        if vowelType == 0:
            newStr += pinyin[:lastVowel] + a_tones[tone - 1] + pinyin[lastVowel + 1:-1]
        elif vowelType == 1:
            newStr += pinyin[:lastVowel] + e_tones[tone - 1] + pinyin[lastVowel + 1:-1]
        elif vowelType == 2:
            newStr += pinyin[:lastVowel] + o_tones[tone - 1] + pinyin[lastVowel + 1:-1]
        elif vowelType == 3:
            newStr += pinyin[:lastVowel] + u_tones[tone - 1] + pinyin[lastVowel + 1:-1]
        elif vowelType == 4:
            newStr += pinyin[:lastVowel] + i_tones[tone - 1] + pinyin[lastVowel + 1:-1]
        elif vowelType == 5:
            newStr += pinyin[:lastVowel] + v_tones[tone - 1] + pinyin[lastVowel + 1:-1]
    print("Correct Pinyin is " + newStr)
    audioStr = "[sound:" + pinyinIn + ".mp3]"
    print(audioStr)
    new_note = genanki.Note(model=mandarin_model, fields=[definition, newStr, characters, audioStr])
    my_deck.add_note(new_note)
    print("+=+=Next Word=+=+")

genanki.Package(my_deck).write_to_file('/home/halowens/Documents/Anki/output.apkg')
print("Succesfully generated new deck")
