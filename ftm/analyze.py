#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bem Vindo ao F.T.M - Follow The Money - Versão 0.2 Beta
Escrito em Python 3
Autor: Thiago Oliveira Castro Vieira - thiago@thiagovieira.adv.br

O objetivo desse software é reunir informações disponíveis publicamente que
possam levar a identificação da autoria de um site.
Atualmente o software busca pelas seguintes informações: ÍP do servidores do
domínio e subdomínios (tentativa e erro); whois do domínio e dos servidores;
códigos de identificação do Google (Ad Sense, Analitycs e Sites), Bing,
Juicy AD (Propaganda em Sites Pornográficos - Canadá); e links
constantes no site.

Modo de Usar: python ftm-02-Beta.py domínio (Caso não informe o domínio na
linha de comando, o software perguntará qual o alvo)

RoadMap: a) melhorar o whois do domínio - não funciona com .br;
b) não ser bloqueado pelo CloudFlare;
c) Exportar um relatório em PDF.

"""
import os
import re
import socket
from concurrent.futures import ThreadPoolExecutor
from time import ctime

import texttable as tt
import pythonwhois
from bs4 import BeautifulSoup
from ipwhois import IPWhois
from ntplib import NTPClient, NTPException
import urllib.request
from urllib.error import URLError, HTTPError



def ntp_time(servers):
    """
    Retorna a hora oficial do Brasil (NTP.br)

    Returns the official time of Brazil (NTP.br).
    """
    ntp_time = None
    client = NTPClient()

    for host in servers:
        try:
            response = client.request(host)
            ntp_time = ctime(response.orig_time)
            break
        except (NTPException, socket.gaierror):
            pass

    return ntp_time


def findservidor(dominio_analisado, dicsubdominios):
    """Busca por subdomínios de forma concorrente"""
    wordlist = []
    wordlist_path = os.path.join(os.path.dirname(__file__), "data", "subdomains.txt")
    if os.path.exists(wordlist_path):
        with open(wordlist_path) as f:
            wordlist = [l.strip() for l in f if l.strip()]
    if not wordlist:
        wordlist = ["www"]

    def resolve(sub):
        try:
            return sub, socket.gethostbyname(f"{sub}.{dominio_analisado}")
        except socket.gaierror:
            return sub, None

    with ThreadPoolExecutor(max_workers=10) as exc:
        for sub, ip in exc.map(resolve, wordlist):
            if ip:
                dicsubdominios[sub] = ip

    return dicsubdominios


def d_whois(dominio_analisado):
    try:
        whois = pythonwhois.get_whois(dominio_analisado)
        raw = whois.get("raw")
        if raw:
            return raw[0]
    except UnicodeDecodeError:
        pass

    # Fallback for .br domains or when pythonwhois fails
    try:
        return os.popen(f"whois {dominio_analisado}").read()
    except Exception:
        return ""


def ip_whois(dicsubdominios):
    """Realiza consultas WHOIS dos IPs em paralelo"""
    result = {}

    def lookup(item):
        k, v = item
        try:
            hosts = IPWhois(v)
            results = hosts.lookup_whois()
            tab = tt.Texttable()
            contato = [[]]
            for i in results['nets'][0].keys():
                contato.append([i, results['nets'][0][i]])
            tab.add_rows(contato)
            tab.set_cols_align(['c', 'c'])
            tab.header(['Dados do Host', '  '])
            return k, tab.draw() + 2 * '\n'
        except Exception as e:
            return k, f"Lookup failed: {e}"

    with ThreadPoolExecutor(max_workers=5) as exc:
        for sub, val in exc.map(lookup, dicsubdominios.items()):
            result[sub] = val

    return result


def get_ids(dominio_analisado):
    req = urllib.request.Request(
        dominio_analisado,
        data=None,
        headers={
            # CloudFlare bloqueia Web Crawler
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'
        })
    try:
        f = urllib.request.urlopen(req, timeout=10)
    except (URLError, HTTPError):
        return "", ""

    soup = BeautifulSoup(f, "html.parser")
    try:
        script = soup.head.find_all('script')  # , {'src':False, 'type':False}
        script = str(script)
        script_old = soup.find_all('script')
        script_old = str(script_old)
        analitycs_id = re.findall(r'[\'\"](UA[\w-]+)[\'\"]', script)
        analitycs_id_old = re.findall(r'UA[\w-]+', script_old)
        ad_sense_id = re.findall(r'[\'\"]ca[\w-]pub[\w-]+[\'\"]', script)
        gcode = soup.find(
            "meta", {
                "name": 'google-site-verification'})  # ['content']
        mscode = soup.find("meta", {"name": 'msvalidate.01'})  # ['content']
        juicyadcode = soup.find(
            "meta", {
                "name": 'juicyads-site-verification'})  # ['content']
    except AttributeError:
        gcode = mscode = juicyadcode = None
    ids = []
    if gcode and gcode.get('content'):
        ids.append('[BR] Google Site Verification Code: {}'.format(gcode['content']))
    if mscode and mscode.get('content'):
        ids.append('[BR] Microsoft Bing Verification Code: {}'.format(mscode['content']))
    if juicyadcode and juicyadcode.get('content'):
        ids.append('[CA] Juicy Ad Code - www.juicyads.com: {}'.format(juicyadcode['content']))
    try:
        ids.append('[BR] Google Analitycs ID: %s' % analitycs_id)
        ids.append('[BR] Google Analitycs ID OLD: %s' % analitycs_id_old)
        ids.append('[BR] Google Ad Sense ID: %s' % ad_sense_id)
        ids = "\n".join(ids)
    except Exception:
        pass
    links_encontrados = "\n".join([link.get('href') for link in soup.find_all("a") if link.get('href')])

    return ids, links_encontrados


def analyze(dominio_analisado):
    ntpservs = ['a.st1.ntp.br',
                'b.st1.ntp.br',
                'c.st1.ntp.br',
                'd.st1.ntp.br']

    ntpbr_time = ntp_time(ntpservs)

    dicsubdominios = {}
    servidores = findservidor(dominio_analisado, dicsubdominios)

    whois = d_whois(dominio_analisado)

    whois_subdomains = ip_whois(dicsubdominios)
    ids, links_encontrados = get_ids("http://" + dominio_analisado)

    return {
        "dominio_analisado": dominio_analisado,
        "ntpbr_time": ntpbr_time,
        "servidores": [(k, v, whois_subdomains[k]) for k, v in servidores.items()],
        "whois": whois,
        "ids": ids,
        "links_encontrados": links_encontrados,
    }

