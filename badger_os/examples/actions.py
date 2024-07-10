import gc
import badger_os
import badger2040
from badger2040 import WIDTH, HEIGHT
import urequests as requests
from GITHUB_CONFIG import TOKEN, REPOSITORIES

REQUEST_PER_PAGE = 5
NAVIGATION = ["(A) prev", "(B) refresh", "(C) next", "(UP / DOWN) change repo"]

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
}

badger_os.state_load("actions", state)


def truncatestring(text, text_size, width):
    if badger.measure_text(text, text_size) <= width:
        return text

    ellipsis = "..."
    while badger.measure_text(text + ellipsis, text_size) > width:
        text = text[:-1]

    return text + ellipsis


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
    cols = [40, 120, 35, 95]
    for i, line in enumerate(lines):
        for j, col in enumerate(line):
            if badger.measure_text(col, 0.5) > cols[j]:
                col = truncatestring(col, 0.5, cols[j])
            badger.text(col, sum(cols[:j]) + 5, 30 + (i * 15), WIDTH, 1)

    badger.set_pen(0)
    badger.rectangle(0, HEIGHT - 16, WIDTH, 16)
    badger.set_pen(15)
    nav = " | ".join(NAVIGATION)
    badger.text(nav, 3, HEIGHT - 12, WIDTH, 1)

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

        parts = [conclusion, name, run_number, run_started_at]
        lines.append(parts)

    return lines


def get_data(lines=[]):
    gc.collect()
    params = {
        "per_page": 1,
        "page": state["current_page"] + state["current_sub_page"],
    }
    repo_index = state["current_repo"]
    if repo_index < 0 or repo_index >= len(REPOSITORIES):
        print(f"Invalid Repo Index: {repo_index}")
        reset()
        draw_view(f"Invalid Repo Index: {repo_index}", "Press (B) to refresh", [])
        return
    repo = REPOSITORIES[repo_index]
    # Documentation: https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28#list-workflow-runs-for-a-repository
    url = f"https://api.github.com/repos/{repo['owner']}/{repo['repo']}/actions/runs?{build_params(params)}"
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
        reset()
        draw_view(f"Error: {e}", "Press (B) to refresh", [])
    finally:
        r.close()

    state["current_sub_page"] += 1
    if state["current_sub_page"] < REQUEST_PER_PAGE:
        get_data(lines)
    else:
        print("Done fetching data")
        badger.led(0)

    gc.collect()


def reset():
    state["current_repo"] = 0
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
        state["current_sub_page"] = 0
        changed = True
    if badger.pressed(badger2040.BUTTON_C):
        update_page(1)
        changed = True

    if changed:
        get_data([])
