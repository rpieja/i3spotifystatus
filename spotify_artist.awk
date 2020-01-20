/string  *"xesam:artist/{
    while (1) {
        getline line
        if (line ~ /string "/) {
            sub(/.*string "/, "artist:", line)
            sub(/".*$/, "", line)
            print line
            break
        }
    }
}
