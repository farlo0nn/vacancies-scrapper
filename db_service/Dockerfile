FROM python3.12-slim 

WORKDIR /app 

RUN pip install uv 
COPY . .
RUN uv sync --system 

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
