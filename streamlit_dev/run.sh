docker run --rm \
 -v "$(pwd):/home/app"\
 -e PORT=8501\
 -p 4001:8501\
 streamlit
