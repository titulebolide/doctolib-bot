import requests
import re
import conf

ids = []
for page in range(1, conf.MAX_PAGE+1):
    s = requests.get(
    "https://www.doctolib.fr/vaccination-covid-19/{}?force_max_limit=2&ref_visit_motive_ids[]=6970&ref_visit_motive_ids[]=7005&page={}".format(conf.LOCATION,page)
    )
    ids_raw = re.findall(r'id="search-result-\d+', s.text)
    ids.extend([int(id.replace('id="search-result-', "")) for id in ids_raw])

for id in ids:
    data = requests.get(
        "https://www.doctolib.fr/search_results/{}.json?force_max_limit=2&ref_visit_motive_ids[]=6970&ref_visit_motive_ids[]=7005".format(id)
    ).json()
    print(data['search_result']['name_with_title'])

    if data['total'] > 0:
        msg = """
### Créneau vaccin trouvé 💉 !
Vaccin covid trouvé à [**{}**](https://www.doctolib.fr{})
        """.format(
            data['search_result']['name_with_title'],
            data['search_result']['link']
        )
        try:
            requests.post("http://127.0.0.1:"+str(conf.BOT_PORT), data={"msg":msg})
        except requests.exceptions.ConnectionError:
            print(msg)
