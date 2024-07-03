import gc
import badger_os
import badger2040
import time
from badger2040 import WIDTH
import urequests as requests
from GITHUB_CONFIG import TOKEN, REPOSITORIES

REQUEST_PER_PAGE = 5
NAVIGATION = "(A) prev | (B) only failures | (C) next | (UP / DOWN) change repo"

HEADERS = {
    "User-Agent": "Badger2040-Actions-Display/0.1",
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}

state = {
    "current_page": 1,
    "current_sub_page": 0,  # 0-4 because REQUEST_PER_PAGE = 5
    "current_repo": 0,
    "failures_only": False,
}

badger_os.state_load("actions", state)


def draw_view(repo_owner_name, pagination, lines):
    # Clear to white
    badger.set_pen(15)
    badger.clear()

    badger.set_font("bitmap8")
    badger.set_pen(0)
    badger.rectangle(0, 0, WIDTH, 16)
    badger.set_pen(15)
    badger.text(repo_owner_name, 3, 4, WIDTH, 1)
    badger.text(
        pagination, WIDTH - badger.measure_text(pagination, 0.4) - 4, 4, WIDTH, 1
    )

    badger.set_pen(0)
    for i, line in enumerate(lines):
        badger.text(line, 5, 16 + (15 // 2) + (i * 15), WIDTH, 1)
    badger.update()


def build_params(params):
    return "&".join([f"{k}={v}" for k, v in params.items()])


def process_workflow_runs(j):
    lines = []

    for item in j.get("workflow_runs", []):
        conclusion = (
            item.get("conclusion").upper() if item.get("conclusion") else "None"
        )
        name = item.get("name", "")
        run_number = f"#{item.get('run_number', 'None')}"
        run_started_at = item.get("run_started_at", "None")

        if len(name) > 20:
            name = name[:17] + "..."

        formatted_line = " | ".join([conclusion, name, run_number, run_started_at])
        lines.append(formatted_line)

    return lines


def get_data(lines=[]):
    gc.collect()
    PARAMS = {
        "per_page": 1,
        "page": state["current_page"] + state["current_sub_page"],
    }
    if state["failures_only"]:
        PARAMS["status"] = "failure"
    repo = REPOSITORIES[state["current_repo"]]
    # Documentation: https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28#list-workflow-runs-for-a-repository
    url = f"https://api.github.com/repos/{repo['owner']}/{repo['repo']}/actions/runs?{build_params(PARAMS)}"
    print(f"Requesting URL: {url}")

    try:
        gc.collect()
        badger.led(128)
        r = requests.get(url, headers=HEADERS)
        j = r.json()
        total_pages = j["total_count"] // REQUEST_PER_PAGE

        lines.extend(process_workflow_runs(j))
        draw_view(
            f"{repo['owner']}/{repo['repo']}",
            f"Page {state['current_page'] // REQUEST_PER_PAGE + 1}/{total_pages}",
            lines,
        )
        gc.collect()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        r.close()

    state["current_sub_page"] += 1
    if state["current_sub_page"] < REQUEST_PER_PAGE:
        time.sleep(1)
        get_data(lines)
    else:
        lines.extend(["", NAVIGATION])
        draw_view(
            f"{repo['owner']}/{repo['repo']}",
            f"Page {state['current_page'] // REQUEST_PER_PAGE + 1}/{total_pages}",
            lines,
        )
        print("Done fetching data")
        badger.led(0)

    gc.collect()


def toggle_failures():
    state["failures_only"] = not state["failures_only"]
    state["current_page"] = 1
    state["current_sub_page"] = 0
    badger_os.state_save("actions", state)


def update_page(increment):
    state["current_page"] = max(1, state["current_page"] + increment * REQUEST_PER_PAGE)
    state["current_sub_page"] = 0
    badger_os.state_save("actions", state)


def update_repo(increment):
    state["current_repo"] = (state["current_repo"] + increment) % len(REPOSITORIES)
    state["current_page"] = 1
    state["current_sub_page"] = 0
    badger_os.state_save("actions", state)


print("Initialized")
# Display Setup
badger = badger2040.Badger2040()
badger.set_update_speed(2)

badger.connect()

# Get the latest data
get_data([])

while True:
    changed = False

    if badger.pressed(badger2040.BUTTON_UP):
        update_repo(-1)
        changed = True
    if badger.pressed(badger2040.BUTTON_DOWN):
        update_repo(1)
        changed = True
    if badger.pressed(badger2040.BUTTON_A):
        update_page(-1)
        changed = True
    if badger.pressed(badger2040.BUTTON_B):
        toggle_failures()
        changed = True
    if badger.pressed(badger2040.BUTTON_C):
        update_page(1)
        changed = True

    if changed:
        get_data([])