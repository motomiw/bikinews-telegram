"""Замена только news.php с резервной копией, сохранением ключа и откатом."""
import datetime as dt
import ftplib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import urllib.request
import urllib.parse

ROOT=Path(__file__).resolve().parent
REMOTE='public_html/news.php'

def connect():
    protocol=os.environ.get('FTP_PROTOCOL','ftp').lower()
    ftp=ftplib.FTP_TLS() if protocol=='ftps' else ftplib.FTP()
    ftp.connect(os.environ['FTP_SERVER'],timeout=45)
    ftp.login(os.environ['FTP_USERNAME'],os.environ['FTP_PASSWORD'])
    if isinstance(ftp,ftplib.FTP_TLS):ftp.prot_p()
    return ftp

def get(ftp,path):
    data=io.BytesIO();ftp.retrbinary('RETR '+path,data.write);return data.getvalue()

def put(ftp,path,data):ftp.storbinary('STOR '+path,io.BytesIO(data))

def main():
    ftp=connect()
    previous=get(ftp,REMOTE)
    text=previous.decode('utf-8-sig').replace('\r\n','\n').strip()
    baseline=(ROOT/'news-baseline.sha256').read_text().strip()
    # Первый запуск сверяем с файлом владельца; повторный — с нашей установленной версией.
    installed=(ROOT/'news.php').read_bytes()
    if hashlib.sha256(text.encode()).hexdigest()!=baseline and previous!=installed:
        raise RuntimeError('Рабочий news.php отличается от проверенного файла. Замена отменена.')
    match=re.search(r"define\('SECRET',\s*'([^']+)'\)",text)
    if match:
        key=match[1]
        secret_file="<?php\nreturn '"+key.replace('\\','\\\\').replace("'","\\'")+"';\n"
        put(ftp,'public_html/data/news-secret.php',secret_file.encode())
    else:
        secret=get(ftp,'public_html/data/news-secret.php').decode()
        found=re.search(r"return\s+'([^']+)'",secret)
        if not found:raise RuntimeError('Не найден ключ запуска; замена отменена.')
        key=found[1]
    try:ftp.mkd('news-backups')
    except ftplib.error_perm as exc:
        if not str(exc).startswith('550'):raise
    backup='news-backups/news-'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d-%H%M%S')+'.php'
    put(ftp,backup,previous)
    if get(ftp,backup)!=previous:raise RuntimeError('Резервная копия не прошла проверку')
    put(ftp,'public_html/news.php.upload',installed)
    if get(ftp,'public_html/news.php.upload')!=installed:raise RuntimeError('Загруженный файл не прошёл проверку')
    ftp.rename('public_html/news.php.upload',REMOTE)
    try:
        request=urllib.request.Request('https://bikinews.ru/news.php',data=urllib.parse.urlencode({'key':key,'collect_only':'1'}).encode())
        with urllib.request.urlopen(request,timeout=100) as response:log=response.read().decode('utf-8')
        if 'Готово. В ленте:' not in log:raise RuntimeError('Проверочный сбор не завершился успешно')
        with urllib.request.urlopen('https://bikinews.ru/data/news.json?audit='+dt.datetime.now(dt.timezone.utc).strftime('%H%M%S'),timeout=30) as response:result=json.load(response)
        if not isinstance(result.get('items'),list) or len(result.get('sources',[]))!=11:
            raise RuntimeError('Новая лента не прошла проверку формата')
        print('Проверено источников:',len(result['sources']))
        for status in result['sources']:
            print(status['source'],':', 'ok, новостей '+str(status.get('matched',0)) if status['ok'] else status.get('error','недоступен'))
        print('Новостей в ленте:',len(result['items']))
        print('Резервная копия вне каталога сайта:',backup)
        print('news.php обновлён; проверочный запуск не отправлял сообщений в Telegram.')
    except Exception:
        # Ошибка проверки не оставляет непроверенную версию на рабочем сайте.
        put(ftp,'public_html/news.php.rollback',previous)
        ftp.rename('public_html/news.php.rollback',REMOTE)
        print('Проверка не пройдена: прежний news.php восстановлен.')
        raise
    finally:ftp.quit()

if __name__=='__main__':main()
