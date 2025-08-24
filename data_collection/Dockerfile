FROM python3.12-slim 

WORKDIR /app 

RUN pip install uv 
COPY . .
RUN uv sync --system 

CMD ["uv", "run", "python", "main.py"]
