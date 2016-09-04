#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bem Vindo ao F.T.M - Follow The Money - Versão 0.2 Beta
Escrito em Python 3
Autor: Thiago Oliveira Castro Vieira - thiago@thiagovieira.adv.br

O objetivo desse software é reunir informações disponíveis publicamente que possam levar a identificação da autoria de um site.
Atualmente o software busca pelas seguintes informações: ÍP do servidores do domínio e subdomínios (tentativa e erro); whois do domínio e dos servidores;
códigos de identificação do Google (Ad Sense, Analitycs e Sites), Bing, Juicy AD (Propaganda em Sites Pornográficos - Canadá); e links
constantes no site.

Modo de Usar: python ftm-02-Beta.py domínio (Caso não informe o domínio na linha de comando, o software perguntará qual o alvo)

RoadMap: a) melhorar o whois do domínio - não funciona com .br; b) não ser bloqueado pelo CloudFlare; c) Exportar um relatório em PDF.

"""
import socket
import sys
import pythonwhois
import re
import validators
import pprintpp
import urllib.request
from bs4 import BeautifulSoup
from ipwhois import IPWhois



def check_dominio_analisado(dominio_analisado):
    if validators.domain(dominio_analisado):
        print('\n\nA sintax do domínio informado é valida\n\n')
    else:
        print('\n\nA sintax do domínio informado é inválida\n\n')
        exit()


def findservidor(dominio_analisado, dicsubdominios):
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
        'portal')
    for subs in subdominios:
        try:
            print('{} : {}'.format (subs, socket.gethostbyname(subs + '.' + dominio_analisado)))
            #print(subs) + (": ") +  socket.gethostbyname(subs + '.' + dominio_analisado)
            dicsubdominios[subs] = socket.gethostbyname(subs + '.' + dominio_analisado)
        except socket.gaierror:
            pass
            print("Erro: " + subs + '.' + dominio_analisado + " não responde")
    return dicsubdominios


def d_whois(dominio_analisado):
    w = pythonwhois.get_whois(dominio_analisado)
    pprintpp.pprint(w)


def ip_whois(dicsubdominios):
    for (k, v) in dicsubdominios.items():
        hosts = IPWhois(v)  # .lookup_rws()
        results = hosts.lookup_whois()
        print('Host: ', v)
        pprintpp.pprint(results)
        print('\n\n')


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

    print('########################################')
    print('# Códigos de Identificação Localizados #')
    print('########################################')
    try:
        print('[BR] Google Site Verification Code: {}'.format(gcode['content']))
    except TypeError:
        pass
    try:
        print(
            '[BR] Microsoft Bing Verification Code:[]'.format(mscode['content']))
    except TypeError:
        pass
    try:
        print('[CA] Juicy Ad Code - www.juicyads.com: {}'.format(juicyadcode['content']))
    except TypeError:
        pass
    print('[BR] Google Analitycs ID: {}'.format(analitycs_id))
    print('[BR] Google Analitycs ID OLD: {}'.format(analitycs_id_old))
    print('[BR] Google Ad Sense ID: {}'.format(ad_sense_id))
    print('################ FIM ###################\n\n')
    print('#####################')
    print('# Links Encontrados #')
    print('#####################\n')
    links = soup.find_all("a")
    for link in links:
        print ("{}".format(link.get("href")))
    print('#####################')


# Programa Principal

def main():
    dicsubdominios = {}
    ipsuddominios = {}

    if len(sys.argv) > 1:
        dominio_analisado = sys.argv[1]
    else:
        dominio_analisado = input('Digite a raiz do dominio: ')

    check_dominio_analisado(dominio_analisado)
    findservidor(dominio_analisado, dicsubdominios)
    print("\n \n Servidores Identificados:\n\n")
    print(dicsubdominios)
    print('\n\nInformações do nome do domínio %s: \n' % dominio_analisado)
    d_whois(dominio_analisado)
    print('\n\n')
    ip_whois(dicsubdominios)
    print('\n\n')
    get_ids("http://" + dominio_analisado)

if __name__ == '__main__':
    main()
