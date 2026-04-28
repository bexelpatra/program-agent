#!/usr/bin/env bash
# projects/abc-english-app/scripts/setup.sh
#
# Flutter + Android SDK + JDK 17 installer for abc-english-app.
#
# Usage:
#   sudo bash projects/abc-english-app/scripts/setup.sh
#
# Idempotent: re-running skips already-installed components.
# Installs to /opt/{flutter,android-sdk}, appends PATH to invoking user's ~/.bashrc.
#
# Tunable via environment variables:
#   FLUTTER_CHANNEL          default: stable
#   FLUTTER_ROOT             default: /opt/flutter
#   ANDROID_SDK_ROOT         default: /opt/android-sdk
#   ANDROID_PLATFORM         default: android-34
#   ANDROID_BUILD_TOOLS      default: 34.0.0
#   CMDTOOLS_ZIP_URL         default: commandlinetools-linux-11076708_latest.zip
#
# Rollback:
#   sudo rm -rf /opt/flutter /opt/android-sdk
#   Remove the "# abc-english-app: flutter+android" block from ~/.bashrc

set -euo pipefail

FLUTTER_CHANNEL="${FLUTTER_CHANNEL:-stable}"
FLUTTER_ROOT="${FLUTTER_ROOT:-/opt/flutter}"
ANDROID_SDK_ROOT="${ANDROID_SDK_ROOT:-/opt/android-sdk}"
ANDROID_PLATFORM="${ANDROID_PLATFORM:-android-36}"
ANDROID_BUILD_TOOLS="${ANDROID_BUILD_TOOLS:-36.0.0}"
CMDTOOLS_ZIP_URL="${CMDTOOLS_ZIP_URL:-https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip}"

if [[ "${EUID}" -ne 0 ]]; then
  echo "ERROR: must run with sudo. Example: sudo bash $0" >&2
  exit 1
fi

REAL_USER="${SUDO_USER:-${USER}}"
REAL_HOME="$(getent passwd "${REAL_USER}" | cut -d: -f6)"

log() { echo "[setup] $*"; }

# 1. APT dependencies
log "Installing apt dependencies..."
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y \
  curl git unzip zip xz-utils \
  openjdk-17-jdk \
  libglu1-mesa \
  clang cmake ninja-build pkg-config libgtk-3-dev

# 2. Flutter SDK (git clone, stable channel)
if [[ ! -d "${FLUTTER_ROOT}/bin" ]]; then
  log "Cloning Flutter ${FLUTTER_CHANNEL} to ${FLUTTER_ROOT}..."
  mkdir -p "$(dirname "${FLUTTER_ROOT}")"
  git clone --depth 1 -b "${FLUTTER_CHANNEL}" \
    https://github.com/flutter/flutter.git "${FLUTTER_ROOT}"
else
  log "Flutter already present at ${FLUTTER_ROOT}; skipping clone."
fi

# 3. Android SDK cmdline-tools
if [[ ! -d "${ANDROID_SDK_ROOT}/cmdline-tools/latest" ]]; then
  log "Installing Android cmdline-tools..."
  mkdir -p "${ANDROID_SDK_ROOT}/cmdline-tools"
  TMP_ZIP="$(mktemp --suffix=.zip)"
  curl -fsSL -o "${TMP_ZIP}" "${CMDTOOLS_ZIP_URL}"
  unzip -q "${TMP_ZIP}" -d "${ANDROID_SDK_ROOT}/cmdline-tools"
  rm -f "${TMP_ZIP}"
  mv "${ANDROID_SDK_ROOT}/cmdline-tools/cmdline-tools" \
     "${ANDROID_SDK_ROOT}/cmdline-tools/latest"
else
  log "Android cmdline-tools already present; skipping."
fi

# 4. Ownership (user-writable for subsequent flutter/sdkmanager commands)
log "Setting ownership to ${REAL_USER}..."
chown -R "${REAL_USER}:${REAL_USER}" "${FLUTTER_ROOT}" "${ANDROID_SDK_ROOT}"

# 5. Android SDK packages + license (run as invoking user)
log "Accepting Android SDK licenses and installing packages..."
SDKMANAGER="${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin/sdkmanager"
sudo -u "${REAL_USER}" env ANDROID_SDK_ROOT="${ANDROID_SDK_ROOT}" \
  bash -c "yes | '${SDKMANAGER}' --licenses > /dev/null" || true
sudo -u "${REAL_USER}" env ANDROID_SDK_ROOT="${ANDROID_SDK_ROOT}" \
  "${SDKMANAGER}" \
    "platform-tools" \
    "platforms;${ANDROID_PLATFORM}" \
    "build-tools;${ANDROID_BUILD_TOOLS}"

# 6. Flutter configuration
log "Configuring Flutter..."
sudo -u "${REAL_USER}" "${FLUTTER_ROOT}/bin/flutter" config --no-analytics >/dev/null
sudo -u "${REAL_USER}" "${FLUTTER_ROOT}/bin/flutter" config \
  --android-sdk "${ANDROID_SDK_ROOT}" >/dev/null
sudo -u "${REAL_USER}" "${FLUTTER_ROOT}/bin/flutter" precache --android >/dev/null

# 7. PATH / env in ~/.bashrc of invoking user
PROFILE="${REAL_HOME}/.bashrc"
if ! grep -q "# abc-english-app: flutter+android" "${PROFILE}" 2>/dev/null; then
  log "Appending PATH block to ${PROFILE}..."
  cat >> "${PROFILE}" <<EOF

# abc-english-app: flutter+android (added by scripts/setup.sh)
export FLUTTER_ROOT="${FLUTTER_ROOT}"
export ANDROID_SDK_ROOT="${ANDROID_SDK_ROOT}"
export PATH="\$FLUTTER_ROOT/bin:\$ANDROID_SDK_ROOT/platform-tools:\$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:\$PATH"
EOF
  chown "${REAL_USER}:${REAL_USER}" "${PROFILE}"
fi

log "Installation complete."
log "Next steps (as regular user):"
log "  source ~/.bashrc"
log "  flutter doctor"
log "  flutter doctor --android-licenses   # if any remain"
