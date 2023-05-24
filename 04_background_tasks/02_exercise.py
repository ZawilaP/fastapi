# Create an app with two endpoints:
# 1. Upload a file and calculate its checksum in the background, then save it to a simple text file
# (format: filename:checksum, one line per file, new ones appended at the end)
# 2. Access that file and return it (format: json with nested list, eg:
# {file: [file1:hash1, file2:hash2 ... ]} )
