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
import socket
import texttable as tt
import pythonwhois
import re
import urllib.request
from bs4 import BeautifulSoup
from ipwhois import IPWhois
from time import ctime
from ntplib import NTPClient, NTPException


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
            ntp_time = ctime(response.tx_time)
            break
        except (NTPException, socket.gaierror):
            pass

    return ntp_time


def findservidor(dominio_analisado, dicsubdominios):
    """ Busca por subdomínios """
    subdominios = (
        'www',
        'mail',
        'ftp',
        'cpanel',
        'blog'
        'direct',
        'direct-connect',
        'admin',
        'pop',
        'imap',
        'forum',
        'portal',
        'smtp')
    for subs in subdominios:
        try:
            # print('{} : {}'.format(subs, socket.gethostbyname(
            #     subs + '.' + dominio_analisado)))
            dicsubdominios[subs] = socket.gethostbyname(
                subs + '.' + dominio_analisado)
        except socket.gaierror:
            pass
    return dicsubdominios


def d_whois(dominio_analisado):

    whois = pythonwhois.get_whois(dominio_analisado)
    rawwhois = whois.get('raw')
    return (rawwhois[0])


def ip_whois(dicsubdominios):
    result = {}
    for (k, v) in dicsubdominios.items():
        hosts = IPWhois(v)  # .lookup_rws()
        results = hosts.lookup_whois()
        tab_nets = tt.Texttable()

        contato_nets = [[]]  # The empty row will have the header

        for i in results['nets'][0].keys():
            contato_nets.append([i, results['nets'][0][i]])

        tab_nets.add_rows(contato_nets)
        tab_nets.set_cols_align(['c', 'c'])
        tab_nets.header(['Dados do Host', '  '])
        result[k] = (tab_nets.draw() + 2 * '\n')
    return result


def get_ids(dominio_analisado):
    req = urllib.request.Request(
        dominio_analisado,
        data=None,
        headers={
            # CloudFlare bloqueia Web Crawler
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'
        })
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f, "html.parser")
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

    ids = []
    try:
        ids.append('[BR] Google Site Verification Code: {}'.format(gcode['content']))
    except TypeError:
        pass
    try:
        ids.append('[BR] Microsoft Bing Verification Code:[]'.format(mscode['content']))
    except TypeError:
        pass
    try:
        ids.append('[CA] Juicy Ad Code - www.juicyads.com: {}'.format(juicyadcode['content']))
    except TypeError:
        pass
    ids.append('[BR] Google Analitycs ID: %s' % analitycs_id)
    ids.append('[BR] Google Analitycs ID OLD: %s' % analitycs_id_old)
    ids.append('[BR] Google Ad Sense ID: %s' % ad_sense_id)
    ids = "\n".join(ids)

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

