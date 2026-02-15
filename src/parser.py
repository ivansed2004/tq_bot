import os
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from models import Discipline
from applog import LOGGER


START_DATE = datetime(2026, 2, 8).date()


def get_url(week_start_date: str) -> str:
    return f"https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya?group=55210&date={week_start_date}"


async def download(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html_content = await response.text()
            os.makedirs("pages", exist_ok=True)
            filename = url.split(sep="=")[-1] + ".html"
            filepath = os.path.join("pages", filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)


async def preprocess() -> str:
    global START_DATE
    now = datetime.now().date()
    while ( not (START_DATE <= now <= START_DATE+timedelta(days=6)) ):
        START_DATE = START_DATE + timedelta(weeks=1)
    try:
        filepath = f"pages/{(START_DATE+timedelta(days=1)).strftime('%Y-%m-%d')}.html"
        if (os.path.exists(filepath) == False):
            url = get_url((START_DATE+timedelta(days=1)).strftime('%Y-%m-%d'))
            await download(url)
        return filepath
    except Exception as e:
        pass


def parse(filepath) -> list[Discipline] | None:
    with open(filepath, "r", encoding="utf-8") as f:
        disciplines: list[Discipline] = []

        html_content = f.read()
        root = BeautifulSoup(html_content).select_one("div.vt236")
        vt244 = root.find("div", class_="vt244 vt244a")
        week_days_date = [ vt244.find("div", attrs={"data-i": f"{num}"}).contents[0] for num in range(1, 7) ]
        week_days_name = [ vt244.find("div", attrs={"data-i": f"{num}"}).contents[1] for num in range(1, 7) ]
        vt244_list = root.find_all("div", class_ = "vt244")
        for i, vt244 in enumerate(vt244_list):
            if (i == 0):
                continue
            number = vt244.find("div", class_ = "vt239").find("div", class_ = "vt283").get_text(strip=True)
            time = vt244.find("div", class_ = "vt239").get_text(separator=" ", strip=True).split(" ")[1:]
            time = [ datetime.strptime(st, "%H:%M") for st in time ]
            vt239_rasp_lists = [ vt244.find("div", class_ = f"vt239 rasp-day rasp-day{num}") for num in range(1, 7) ]
            for i, vt239_rasp_list in enumerate(vt239_rasp_lists):
                if ( len(vt239_rasp_list) == 0 ):
                    continue
                date = week_days_date[i].get_text(strip=True); date = datetime.strptime(date, "%d.%m")
                week_day = week_days_name[i].get_text(strip=True)
                for disc in vt239_rasp_list:
                    name = disc.find("div", class_ = "vt240").get_text(strip=True)
                    teacher = disc.find("div", class_ = "vt241").find("span", class_ = "teacher"); teacher = teacher.get_text(strip=True) if teacher != None else None
                    location = disc.find("div", class_ = "vt242"); location = location.get_text(strip=True) if location != None else None
                    type =  disc.find("div", class_ = "vt243 vt243a") or \
                            disc.find("div", class_ = "vt243 vt243b") or \
                            disc.find("div", class_ = "vt243"); type = type.get_text(strip=True) if type != None else None
                    discipline = Discipline(number=number, 
                                            start_time=time[0], 
                                            end_time=time[1],
                                            date=date, 
                                            week_day=week_day, 
                                            name=name, 
                                            teacher=teacher, 
                                            location=location, 
                                            type=type)
                    disciplines.append(discipline)
        return disciplines