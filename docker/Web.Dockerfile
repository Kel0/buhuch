FROM python:3.7-slim

EXPOSE 3010

COPY ./ /app
WORKDIR app

RUN apt-get update \
    && apt-get install -y xvfb wget fontconfig libfreetype6 libjpeg62-turbo libpng16-16 \
    libx11-6 libxcb1 libxext6 libxrender1 xfonts-75dpi xfonts-base libfontconfig1 \
    fontconfig-config libx11-data libxau6 libxdmcp6 xfonts-utils ucf fonts-dejavu-core \
    ttf-bitstream-vera fonts-liberation libbsd0 libfontenc1 libxfont2 \
    x11-common xfonts-encodings \
    && wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb \
    && dpkg -i wkhtmltox_0.12.5-1.buster_amd64.deb
RUN ls -l
RUN pip install --upgrade pip && pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:3010", "web.app:app"]