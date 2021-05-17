#!/usr/bin/env python3

import requests
import re
import click
from progress.bar import Bar
from pynotifier import Notification
import time


def get_availabilities(location, max_page):
    ids = []
    bar = Bar('1/2 - Chargement des identifiants', max=max_page)
    for page in range(1, max_page+1):
        s = requests.get(
            "https://www.doctolib.fr/vaccination-covid-19/{}?force_max_limit=2&ref_visit_motive_ids[]=6970&ref_visit_motive_ids[]=7005&page={}".format(location,page)
        )
        ids_raw = re.findall(r'id="search-result-\d+', s.text)
        ids.extend([int(id.replace('id="search-result-', "")) for id in ids_raw])
        bar.next()
    bar.finish()

    bar = Bar('2/2 - Verification des disponibilités', max=len(ids))
    availables = []
    for id in ids:
        data = requests.get(
            "https://www.doctolib.fr/search_results/{}.json?force_max_limit=2&ref_visit_motive_ids[]=6970&ref_visit_motive_ids[]=7005".format(id)
        ).json()
        if data['total'] > 0:
            availables.append(data)
        bar.next()
    bar.finish()
    return availables


def output_data(availabilities, type_ouput):
    if 'notification' in type_ouput:
        if len(availabilities) > 0:
            Notification(
                title="Nouvelles doses disponibles !",
                description="Vite ! Allez sur doctolib",
                duration=5,
                urgency='normal'
            ).send()

    if 'logging' in type_ouput:
        if len(availabilities) > 0:
            click.echo('\nVaccin covid trouvé(s) à:')
            for availability in availabilities:
                click.echo("- {} : https://www.doctolib.fr{}".format(
                    availability['search_result']['name_with_title'],
                    availability['search_result']['link']
                ))


@click.command()
@click.option('--location', default='paris', help="La ville autour de laquelle rechercher")
@click.option('--max-page', default=2, help="Nombre de page à scanner sur Doctolib")
@click.option('--quiet/--no-quiet', default=False, help="Désactive le logging. Défaut : Faux")
@click.option('--forever/--no-forever', default=False, help="Si le programme doit s'executer indéfiniment ou chercher une seule fois. Défaut : Vrai")
@click.option('--interval', default=5, help="Intervalle en minutes entre chaque rafraichissements si --forever est utilisé. Attention de ne pas mettre trop court, on ne sait pas si doctolib fait des bans. Défaut : 5.")
@click.option('--notify/--no-notify', default=True, help="Si le programme doit afficher une notification si un créneau est trouvé. Défaut : Vrai")
def main(location, max_page, quiet, forever, interval, notify):
    """
    Cherche sur Doctolib les rendez-vous disponibles pour les +18 ans sans comorbidités dans les 24 heures à venir.
    """
    type_ouput = []
    if notify: type_ouput.append('notification')
    if not quiet: type_ouput.append('logging')

    if forever:
        while True:
            availabilities = get_availabilities(location, max_page)
            output_data(availabilities, type_ouput)
            time.sleep(interval*60)
    else:
        availabilities = get_availabilities(location, max_page)
        output_data(availabilities, type_ouput)

    return availabilities

if __name__ == "__main__":
    main()
