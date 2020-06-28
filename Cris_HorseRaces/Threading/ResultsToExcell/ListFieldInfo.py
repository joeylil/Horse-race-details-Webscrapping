import unicodedata
import bs4
import requests


def field(webAddress):
    res = requests.get("https://cris.rwwa.com.au/{}".format(webAddress))
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    racenoSoup = bs4.BeautifulSoup(res.text)

    table = racenoSoup.find("table", {"class": "tblcris raceField"})
    rows = []
    rows.append(racenoSoup.h3.text.strip()[0:racenoSoup.h3.text.find("(") - 1])

    result = racenoSoup.find("img", {"title": "Race Results"})

    if result is not None:
        for row in table.findAll("tr"):
            currentRow = []
            for td_txt in row.findAll('td'):  # lets see all the td's in each tr
                currentRow.append(td_txt.text)
            if len(currentRow) == 12 or len(currentRow) == 11:
                if currentRow[4].strip() == "SC":
                    currentRow[3] = unicodedata.normalize("NFKD", currentRow[3])
                    rows.append((currentRow[1], currentRow[2], "N/A", "SCRATCHED", "SCRATCHED", "SC"))
                else:
                    currentRow[3] = unicodedata.normalize("NFKD", currentRow[3])
                    result = currentRow[10][1:currentRow[10][1:].find('$') + 1]
                    rows.append((currentRow[1], currentRow[2], currentRow[5], currentRow[8][1:-1],
                                 currentRow[9][1:-1], result))
        return rows
