import os
import requests
import re


def get_all_topic_urls(top_level_url, number_of_pages):
    """top_level_url should look like:
    https://community.fantasyflightgames.com/forum/518-star-wars-armada-battle-reports/page/
    """

    all_thread_urls = []
    all_page_urls = []
    number_of_pages_str = str(number_of_pages)

    top_level_url.strip()
    print(f"Getting subforum name from top_level_url:\n\t==\t{top_level_url}\t==\t\n")
    subforum = top_level_url.split("/")[-3]

    for page_number in range(1, number_of_pages + 1):
        page_number_str = str(page_number)
        print("[+] Page {} / {}".format(page_number_str, number_of_pages_str))
        topic_re = re.compile(
            r"<a href='(https://community.fantasyflightgames.com/topic/.*?/)' class='' title='"
        )

        url = top_level_url + page_number_str + "/"
        r = requests.get(url)

        topics = re.findall(topic_re, r.text)
        all_thread_urls.extend([topic.strip() for topic in topics])

    for thread_url in all_thread_urls:
        print(f"  [.] Downloading thread: {thread_url}")
        all_page_urls.extend(download_thread(thread_url, subforum))

    return [url for url in all_page_urls]


def number_of_pages_in_thread(thread_base_url):
    """Find the header and from it parse the number of pages in the thread."""

    print(f"      - Finding count from {thread_base_url}")

    header_re = re.compile(
        r"<li class='ipsPagination_last'><a href=.* rel=\"last\" data-page='(.*)' data-ipsTooltip"
    )

    r = requests.get(thread_base_url)

    header_matches = re.findall(header_re, r.text)
    if header_matches:
        return int(header_matches[0])
    return 1


def get_all_page_urls_in_thread(thread_base_url):
    """Get the URL for every page in a thread."""

    page_count = number_of_pages_in_thread(thread_base_url)

    page_urls = []

    for page_number in range(1, page_count + 1):
        page_urls.append(thread_base_url + "page/" + str(page_number) + "/")

    return page_urls


def download_thread(thread_url, subforum):
    """Download all pages of a thread into the thread's folder"""

    download_path = subforum
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    download_path = "{}/{}/".format(subforum,thread_url.split("/")[-2])
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    target_urls = get_all_page_urls_in_thread(thread_url)

    for url in target_urls:
        try:
            file_path = download_path + "_".join(url.split("/")[-3:-1]) + ".html"
            r = requests.get(url)
            with open(file_path, "wb") as download_path_file:
                download_path_file.write(r.content)
        except Exception as err:
            target_urls.remove(url)

    return target_urls  # successfully downloaded


if __name__ == "__main__":

    all_urls = []

    main_urls = get_all_topic_urls(
        "https://community.fantasyflightgames.com/forum/402-star-wars-armada/page/", 401
    )
    with open("./forum/main_urls.lst", "w+") as open_file:
        [open_file.write(u + "\n") for u in main_urls]

    print("[[ BAT REPS ]]")
    bat_rep_urls = get_all_topic_urls(
        "https://community.fantasyflightgames.com/forum/518-star-wars-armada-battle-reports/page/",
        23,
    )
    with open("./bat_rep_urls.lst", "w+") as open_file:
        [open_file.write(u + "\n") for u in bat_rep_urls]

    print("[[ FLEET BUILDS ]]")
    fleet_build_urls = get_all_topic_urls(
        "https://community.fantasyflightgames.com/forum/441-star-wars-armada-fleet-builds/page/",
        173,
    )
    with open("./forum/fleet_build_urls.lst", "w+") as open_file:
        [open_file.write(u + "\n") for u in fleet_build_urls]

    print("[[ PAINTING ]]")
    painting_urls = get_all_topic_urls(
        "https://community.fantasyflightgames.com/forum/501-star-wars-armada-painting-and-modification/page/",
        23,
    )
    with open("./forum/painting_urls.lst", "w+") as open_file:
        [open_file.write(u + "\n") for u in painting_urls]

    print("[[ OP ]]")
    organized_play_urls = get_all_topic_urls(
        "https://community.fantasyflightgames.com/forum/442-star-wars-armada-organized-play/page/",
        41,
    )
    with open("./forum/organized_play_urls.lst", "w+") as open_file:
        [open_file.write(u + "\n") for u in organized_play_urls]

    print("[[ RULES ]]")
    rules_urls = get_all_topic_urls(
        "https://community.fantasyflightgames.com/forum/440-star-wars-armada-rules-questions/page/",
        96,
    )
    with open("./forum/rules_urls.lst", "w+") as open_file:
        [open_file.write(u + "\n") for u in rules_urls]

    print("[[ OFF TOPIC ]]")
    off_topic_urls = get_all_topic_urls(
        "https://community.fantasyflightgames.com/forum/444-star-wars-armada-off-topic/page/",
        29,
    )
    with open("./forum/off_topic_urls.lst", "w+") as open_file:
        [open_file.write(u + "\n") for u in off_topic_urls]

    for listy in [
        # main_urls,
        bat_rep_urls,
        fleet_build_urls,
        painting_urls,
        organized_play_urls,
        rules_urls,
        off_topic_urls,
    ]:
        all_urls.extend[listy]

    with open("./forum/all_urls.lst", "w+") as open_file:
        [open_file.write(u + "\n") for u in all_urls]
