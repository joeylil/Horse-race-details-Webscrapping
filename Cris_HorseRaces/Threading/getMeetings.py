import bs4
import requests

from Cris_HorseRaces.Threading import field, result


def getMeetings(queue, event, address):
    while not event.is_set():
        req = requests.get(address)
        meetingInfo = bs4.BeautifulSoup(req.content, "html.parser")
        table = meetingInfo.find("table", {"class": "tblcris"})
        linksField = ""
        linksResult = ""

        for row in table.findAll("tr"):
            racefield = False
            raceResult = False
            for cell in row.findAll("td"):  # lets see all the td's in each tr
                for link in cell.findAll('a'):
                    if link['href'].startswith("racefield"):
                        if link['href'] not in linksField:
                            racefield = True
                            linksField = link['href']
                    if link['href'].startswith("raceresults") and not link['href'].endswith("true"): #link is race result and not photo
                        if link['href'] not in linksResult:
                            raceResult = True
                            linksResult = link['href']
            if racefield and raceResult:
                fieldStats = field(linksField)
                resultStats = result(linksResult)
                queue.put((fieldStats, resultStats))