cat << 'EOF' > create_shortcut.sh
#!/bin/bash
set -e

# Pull the latest Docker image
docker pull ghcr.io/agreene90/mortyrag:latest

# Create Desktop Entry for all users
DESKTOP_ENTRY="/usr/share/applications/MortyRAG.desktop"
echo "[Desktop Entry]" > "$DESKTOP_ENTRY"
echo "Version=1.0" >> "$DESKTOP_ENTRY"
echo "Name=MortyRAG" >> "$DESKTOP_ENTRY"
echo "Comment=Start MortyRAG Docker Container" >> "$DESKTOP_ENTRY"
echo "Exec=docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ghcr.io/agreene90/mortyrag:latest" >> "$DESKTOP_ENTRY"
echo "Icon=docker" >> "$DESKTOP_ENTRY"
echo "Terminal=false" >> "$DESKTOP_ENTRY"
echo "Type=Application" >> "$DESKTOP_ENTRY"
echo "Categories=Development;" >> "$DESKTOP_ENTRY"
echo "StartupNotify=true" >> "$DESKTOP_ENTRY"

# Create a symlink to the user's desktop
ln -s "$DESKTOP_ENTRY" "$HOME/Desktop/MortyRAG.desktop"
chmod +x "$HOME/Desktop/MortyRAG.desktop"

echo "MortyRAG has been successfully installed and a shortcut has been added to your desktop."
EOF
