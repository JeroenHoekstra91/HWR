from util.character_map import hebrew_to_phonetic

transcript_file = "transcript.txt"
output_file = "transcript_in_phonetics.txt"

file = open(transcript_file, "rb")
text = file.read()
file.close()

output = ""
for line in text.split("\n"):
    for word in line.split(" "):
        output += "_".join(hebrew_to_phonetic(word).split(" ")) + " "
    output.strip()
    output += "\n"

file = open(output_file, "wb")
file.write(output)
file.close()