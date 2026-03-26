#!/usr/bin/env bash

set -euo pipefail

REPO_DIR="${REPO_DIR:-/workspace}"
RUNS_PER_DAY="${RUNS_PER_DAY:-15}"
INTERVAL_SECONDS="${INTERVAL_SECONDS:-60}"
DAY_SECONDS="${DAY_SECONDS:-86400}"
AUTO_FOLDER_ROOT="${AUTO_FOLDER_ROOT:-auto-random-folders}"
GIT_USER_NAME="${GIT_USER_NAME:-leetcode-sync-bot}"
GIT_USER_EMAIL="${GIT_USER_EMAIL:-leetcode-sync-bot@users.noreply.github.com}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
export GIT_CONFIG_GLOBAL="${GIT_CONFIG_GLOBAL:-/tmp/gitconfig}"

cd "$REPO_DIR"

if [ ! -f "./sync.sh" ]; then
    echo "sync.sh not found in $REPO_DIR"
    exit 1
fi

chmod +x ./sync.sh

setup_git_config() {
    git config --global user.name "$GIT_USER_NAME"
    git config --global user.email "$GIT_USER_EMAIL"
    git config --global --add safe.directory "$REPO_DIR"
}

setup_github_auth() {
    if [ -n "$GITHUB_TOKEN" ]; then
        gh auth login --with-token <<<"$GITHUB_TOKEN" >/dev/null 2>&1 || true
        git config --global url."https://x-access-token:${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"
    fi
}

random_token() {
    LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 8
}

ensure_folder_pool() {
    mkdir -p "$AUTO_FOLDER_ROOT/a" "$AUTO_FOLDER_ROOT/b" "$AUTO_FOLDER_ROOT/c"
}

choose_random_folder() {
    mapfile -t dirs < <(find . -type d \
        -not -path './.git*' \
        -not -path './.github*' \
        -not -path './docker*' \
        -not -path './node_modules*')

    local filtered=()
    local dir
    for dir in "${dirs[@]}"; do
        if [ "$dir" != "." ]; then
            filtered+=("$dir")
        fi
    done

    if [ "${#filtered[@]}" -eq 0 ]; then
        ensure_folder_pool
        mapfile -t filtered < <(find "./$AUTO_FOLDER_ROOT" -type d)
    fi

    local idx=$((RANDOM % ${#filtered[@]}))
    printf '%s\n' "${filtered[$idx]}"
}

create_random_text_file() {
    local target_dir
    target_dir="$(choose_random_folder)"
    mkdir -p "$target_dir"

    local file_name="random-$(date +%Y%m%d-%H%M%S)-$(random_token).txt"
    local file_path="$target_dir/$file_name"

    {
        echo "Random note: $(random_token)"
        echo "Created at: $(date -Iseconds)"
        echo "Payload: $(random_token)"
    } >"$file_path"

    printf '%s\n' "${file_path#./}"
}

run_once() {
    local rel_path
    rel_path="$(create_random_text_file)"

    local commit_msg="auto-sync: add ${rel_path}"
    echo "Running sync.sh for ${rel_path}"
    if ! SYNC_COMMIT_MESSAGE="$commit_msg" ./sync.sh; then
        echo "sync.sh failed for ${rel_path}. Will retry in next interval."
        return 1
    fi
}

echo "Automation started at $(date -Iseconds)"
setup_git_config
setup_github_auth

while true; do
    echo "Starting daily cycle at $(date -Iseconds)"
    for ((i = 1; i <= RUNS_PER_DAY; i++)); do
        echo "Cycle run $i/$RUNS_PER_DAY"
        run_once || true

        if [ "$i" -lt "$RUNS_PER_DAY" ]; then
            sleep "$INTERVAL_SECONDS"
        fi
    done

    active_window=$((RUNS_PER_DAY * INTERVAL_SECONDS))
    remaining_sleep=$((DAY_SECONDS - active_window))

    if [ "$remaining_sleep" -lt 0 ]; then
        remaining_sleep=0
    fi

    echo "Daily cycle complete. Sleeping ${remaining_sleep}s"
    sleep "$remaining_sleep"
done