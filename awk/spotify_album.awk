/string  *"xesam:album/{
    while(1) {
        getline line
        if (line ~ /string "/) {
            sub(/.*string "/, "album:", line)
            sub(/".*$/, "", line)
            print line
            break
        }
    }
}
