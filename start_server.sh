inotifywait -m /home/omar/workspace/M2/hypermedia/google/google_api/text_files/ -e create -e moved_to |
    while read dir action file; do
        echo "The file '$file' appeared in directory '$dir' via '$action'"
        python3 manage.py runserver
    done
