# https://genius.com/api/artists/29743/songs?page=1&sort=popularity
import collections
import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup


def is_valid(word):
    #if "[" in word and "]" in word:
    #    return False
    return "[" not in word and "]" not in word


def extract_lyrics(url):
    print(f"Fetching lyrics {url} ...")
    r = requests.get(url)
    if r.status_code != 200:
        return []

    soup = BeautifulSoup(r.content, 'html.parser')                                                                          #r.content (renvoie le contenu de al page au format HTML)
    lyrics = soup.find("div", class_="Lyrics__Container-sc-1ynbvzw-6 YYrds")                                                #"Lyrics__Container-sc-1ynbvzw-6 YYrds"
    if not lyrics:                                                                                                          # on créer une boucle récursive, car a la première requête les element peuvent ne pas s'afficher correctement, et donc il y a rien à récuperer.
        return []
        #return extract_lyrics(url)

    # ici on va récupérer les lyrics nettoyé des éléments HTML (ex: <div class=...>)
    all_words = []
    for sentence in lyrics.stripped_strings:                                                                                # ".stripped_strings" --> generator: itérable (avec les même propriété qu'une liste, sur laquelle on peut passer)
        #print(sentence.split())                                                                                            # Par défaut on recoit une liste de listes
        # on créer une liste pour chaque phrase/liste en enlevant les mots insignifiants, ainsi que la ponctuation et tout en miniscule ainsi que les mots refrain entre crochet
        sentence_words = [word.strip(",").strip(".").lower() for word in sentence.split() if is_valid(word)]
        all_words.extend(sentence_words)                                                                                    # Ici on concatene toutes les liste les une avec les autres. Pour éviter les listes de liste

    return all_words
    #pprint(all_words)


def get_all_urls():
    page_nb = 1
    links = []
    while True:
        r = requests.get(f"https://genius.com/api/artists/41749/songs?page={page_nb}&sort=popularity")                      # Patrick bruel: 29743
        if r.status_code == 200: #renvoi un code 200 = requête correctement effectuée.
            #print(r.status_code)
            #pprint(r.json().get("response")) #--> permet d'avoir un affichage plus lisible
            print(f"Fetching page {page_nb}")
            response = r.json().get("response", {}) # l'ajout du dictionnaire permet d'éviter d'être bloquer avec la requête suivant dans le cas ou la requête renvoie un None
            next_page = response.get("next_page")
            #print(next_page)

            songs = response.get("songs")
            all_song_links = [song.get("url") for song in songs]
            links.extend(all_song_links) # Extend va nous permettre au fur que l'on avance dans les pages de ne pas avoir des liste de listes.
            # or can be replace by
            #links.extend([song.get("url") for song in songs])
            page_nb += 1

            if not next_page:
                print("No more pages to fetch.")
                break

    #pprint(links)
    #print(len(links))
    return links


def extract_and_get_all_words():
    urls = get_all_urls()
    words = []
    for url in urls:
        lyrics = extract_lyrics(url=url)
        words.extend(lyrics)
    #pprint(words)

    # on enregistre le contenu dans un fichier json que l'on créer à la racine
    with open("data_michel_sardou.json", "w") as f:
        json.dump(words, f, indent=4)

    counter = collections.Counter([w for w in words if len(w) > 5])
    most_common_words = counter.most_common(15)
    pprint(most_common_words)                                                                                               # méthode propre à Collection


def get_all_words():
    with open("data_michel_sardou.json", "r") as f:
        liste = json.load(f)
        counter = collections.Counter([w for w in liste if len(w) > 7])
        most_common_words = counter.most_common(15)
        pprint(most_common_words)

extract_and_get_all_words()
#get_all_words()