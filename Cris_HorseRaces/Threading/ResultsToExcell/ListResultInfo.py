import bs4
import requests


def result(webAddress):
    res = requests.get("https://cris.rwwa.com.au/{}".format(webAddress))
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))

    racenoSoup = bs4.BeautifulSoup(res.text)

    rows = []

    rows.append(racenoSoup.h3.text.strip()[0:racenoSoup.h3.text.find("(")-1])


    table = racenoSoup.find("table", {"class": "tblcris tbldata"})
    for row in table.findAll("tr"):
        currentRow = []
        for td_txt in row.findAll('td'):
            currentRow.append(td_txt.text.strip())
        if len(currentRow) == 15:
            rows.append((currentRow[0], currentRow[1], currentRow[4], currentRow[7], currentRow[8]))
        if len(currentRow) == 10:
            rows.append((currentRow[0], "N/A", "N/A", currentRow[7], currentRow[8]))
    return rows
