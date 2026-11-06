#!/usr/bin/env bash
# ==============================================================================
# Bob Game Center - One-Line Online Installer for SteamOS / Arch Linux
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/vodacthe/bob_gaming_game_center_public/main/install.sh | bash
# ==============================================================================

set -euo pipefail

TAG="[Packaging/Deck/OnlineInstall]"
RAW_BASE="${BOB_UPDATE_RAW_BASE:-https://raw.githubusercontent.com/vodacthe/bob_gaming_game_center_public/main}"
PACKAGE_NAME="bob_game_center_deck.tar.gz"

log() {
    printf '[%s] %s [%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$TAG" "$1" "$2"
}

if [ "${EUID:-$(id -u)}" -eq 0 ]; then
    log "ERROR" "Do not run this installer with sudo or as root. Run directly as user 'deck'."
    exit 1
fi

for tool in curl tar python3; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        log "ERROR" "Required tool '$tool' is missing from PATH."
        exit 1
    fi
done

CACHE_BUST="$(date +%s)"
VERSION="$(curl -fsSL "${RAW_BASE}/version.MD?t=${CACHE_BUST}" 2>/dev/null | tr -d '\r\n ' || true)"
log "INFO" "Preparing to download Bob Game Center ${VERSION:+v${VERSION}} for SteamOS / Linux..."

TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/bob_gc_install.XXXXXX")"
cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

ARCHIVE_PATH="$TMP_DIR/$PACKAGE_NAME"
EXTRACT_DIR="$TMP_DIR/pkg"
mkdir -p "$EXTRACT_DIR"

START_TS="$(date +%s)"
if ! curl -fL --retry 3 --connect-timeout 20 "${RAW_BASE}/${PACKAGE_NAME}?t=${CACHE_BUST}" -o "$ARCHIVE_PATH"; then
    log "ERROR" "Failed to download ${RAW_BASE}/${PACKAGE_NAME}"
    exit 1
fi
DL_DUR="$(($(date +%s) - START_TS))"
DL_BYTES="$(stat -c%s "$ARCHIVE_PATH" 2>/dev/null || wc -c <"$ARCHIVE_PATH")"
log "INFO" "Downloaded $PACKAGE_NAME (${DL_BYTES} bytes) in ${DL_DUR}s."

if ! tar -tzf "$ARCHIVE_PATH" main.py >/dev/null 2>&1; then
    log "ERROR" "Downloaded archive failed integrity check (main.py missing)."
    exit 1
fi

tar -xzf "$ARCHIVE_PATH" -C "$EXTRACT_DIR"
chmod 755 "$EXTRACT_DIR/scripts/deck/install_deck.sh"

log "INFO" "Handing off to user-space installer..."
bash "$EXTRACT_DIR/scripts/deck/install_deck.sh" </dev/null
log "INFO" "Bob Game Center ${VERSION:+v${VERSION}} installation finished successfully."
