import datetime
import json
import os

import requests
import bs4

IFMO_PROGRAMS_URL = "https://abitlk.itmo.ru/api/v1/rating/directions?degree=master"
IFMO_PROGRAM_URL = "https://abit.itmo.ru/rating/master/budget/{program_id}"


def cast_diploma_score(text: str) -> float:
    filtered = ""
    for char in text:
        if char.isdigit() or char == ".":
            filtered += char
    return float(filtered)

def cast_are_originals_passed(text: str) -> bool:
    text = text.lower().strip()

    return text == "да"


significant_info = {
    "Приоритет": "priority",
    "Вид испытания": "challenge_type",
    "Балл ВИ+ИД": "score",
    "Средний балл": "diploma_score",
    "Оригиналы документов": "are_originals_passed",
}
significant_info_casts = {
    "priority": int,
    "challenge_type": str,
    "score": float,
    "diploma_score": cast_diploma_score,
    "are_originals_passed": cast_are_originals_passed,
}


def get_program_abits(program_id: int) -> list[dict]:

    result = []

    response = requests.get(IFMO_PROGRAM_URL.format(program_id=program_id))
    if response.status_code != 200:
        return None

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    items = soup.select('div[class*="RatingPage_table__item"]')
    for item in items:
        position_item = item.find("p")
        rating, uid = position_item.get_text().split("№")
        rating = int(rating)

        data = {
            "uid": uid,
            "rating": rating,
        } | {
            key: None for key in significant_info.values()
        }

        mb_significant_values = item.find_all("p")
        for mb_significant in mb_significant_values:
            txt = mb_significant.get_text()
            try:
                mb_key, mb_value = txt.split(":")
                mb_key, mb_value = mb_key.strip(), mb_value.strip()
            except:
                continue

            if key := significant_info.get(mb_key):
                cast = significant_info_casts.get(key, str)
                value = cast(mb_value)
                data[key] = value

        result.append(data)

    return result


def get_programs() -> list[dict]:
    response = requests.get(IFMO_PROGRAMS_URL)
    if response.status_code != 200:
        raise ValueError(f"Could not fetch programs from {IFMO_PROGRAMS_URL}")

    data = json.loads(response.text)
    return data["result"]["items"]


def make_new_db(db_name: str):
    print(f"Making new database... {db_name}")
    os.mkdir(db_name)
    known_programs = get_programs()
    with open(f"{db_name}/programs.json", "w") as programs_file:
        json.dump(known_programs, programs_file)

    print(f"Found {len(known_programs)} programs.")
    n = 0
    for program in known_programs:
        n+= 1
        uid = program["competitive_group_id"]
        print(f"Fetching {uid}..., {n}/{len(known_programs)}")
        program_abits = get_program_abits(uid)
        with open(f"{db_name}/{uid}.json", "w") as abits_file:
            json.dump(program_abits, abits_file)


if __name__ == "__main__":
    now = int(datetime.datetime.utcnow().timestamp())
    db_name = f"database__{now}.json"
    make_new_db(db_name)