import requests
import re
import click
from progress.bar import Bar
from pynotifier import Notification




def search(location, max_page):
    res = []
    """
    Cherche sur Doctolib les rendez-vous disponibles pour les +18 ans sans comorbidités dans les 24 heures à venir.
    """
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
    for id in ids:
        data = requests.get(
            "https://www.doctolib.fr/search_results/{}.json?force_max_limit=2&ref_visit_motive_ids[]=6970&ref_visit_motive_ids[]=7005".format(id)
        ).json()
        if data['total'] > 0:
            click.echo("\nVaccin covid trouvé à {} : https://www.doctolib.fr{}".format(
                data['search_result']['name_with_title'],
                data['search_result']['link']
            ))
            res.append("\nVaccin covid trouvé à {} : https://www.doctolib.fr{}".format(
                data['search_result']['name_with_title'],
                data['search_result']['link']
            ))
        bar.next()
    bar.finish()
    return res


@click.command()
@click.option('--location', default='paris', help="La ville autour de laquelle rechercher")
@click.option('--max-page', default=2, help="Nombre de page à scanner sur Doctolib")
def main(location, max_page):
    res = search(location, max_page)
    new_res = []
    while 1==1:
        new_res = search(location, max_page)
        for i in new_res:
            if i not in res:
                Notification(
                    title="Nouvelles doses disponibles !",
                    description="Vite ! Allez sur doctolib",
                    duration=5,
                    urgency='normal'
                ).send()
                break
        res = new_res[::]


if __name__ == "__main__":
    main()
