FROM python

WORKDIR /app

COPY . .

ENV FILENAME "input.txt"

CMD ["python", "main.py"]