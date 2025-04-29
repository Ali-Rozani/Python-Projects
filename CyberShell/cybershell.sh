#!/bin/bash

# Set colors
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Loading Animation
echo -e "${GREEN}Initializing CyberShell...${NC}"
for i in {1..20}; do
    echo -ne "${GREEN}[====================] ($((i*5))%)\r${NC}"
    sleep 0.1
done
echo -e "\n${GREEN}CyberShell Ready!${NC}"

# Function to detect installed apps
detect_apps() {
    echo -e "${GREEN}Scanning for installed applications...${NC}"
    declare -A app_paths

    # Search common Windows directories for .exe files
    search_dirs=(
        "/mnt/c/Program Files"
        "/mnt/c/Program Files (x86)"
        "/mnt/c/Users/$USER/AppData/Local"
        "/mnt/c/Windows/System32"
    )

    for dir in "${search_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            while IFS= read -r app; do
                app_name=$(basename "$app")
                app_paths["$app_name"]="$app"
            done < <(find "$dir" -type f -iname "*.exe" 2>/dev/null)
        fi
    done

    # Store results in an indexed array
    app_list=("${!app_paths[@]}")
    app_paths_list=("${app_paths[@]}")

    # Display detected apps
    echo -e "${GREEN}Detected Applications:${NC}"
    for i in "${!app_list[@]}"; do
        printf "${GREEN}%d. %s${NC}\n" "$((i + 1))" "${app_list[$i]}"
    done
}

# Detect installed applications
detect_apps

# Let the user choose an app
while true; do
    echo -ne "${GREEN}Enter number to open (q to quit): ${NC}"
    read choice
    if [[ "$choice" == "q" ]]; then
        echo -e "${GREEN}Exiting CyberShell.${NC}"
        exit 0
    elif [[ "$choice" =~ ^[0-9]+$ ]] && (( choice > 0 && choice <= ${#app_list[@]} )); then
        app_to_run="${app_paths_list[$((choice - 1))]}"
        echo -e "${GREEN}Launching ${app_list[$((choice - 1))]}...${NC}"
        nohup "$app_to_run" >/dev/null 2>&1 &
    else
        echo -e "${GREEN}Invalid choice. Try again.${NC}"
    fi
done