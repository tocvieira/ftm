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
import sys
import texttable as tt
import pythonwhois
import re
import validators
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


def check_dominio_analisado(dominio_analisado):
    """
    Verifica se a string informada é valida como nome de domínio

    """
    if validators.domain(dominio_analisado):
        pass
    else:
        print('\n\nA sintax do domínio informado é inválida\n\n')
        exit()


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
    print(rawwhois[0])


def ip_whois(dicsubdominios):
    for (k, v) in dicsubdominios.items():
        hosts = IPWhois(v)  # .lookup_rws()
        results = hosts.lookup_whois()
        print('Host - %s: %s' % (k, v))

        tab_nets = tt.Texttable()

        contato_nets = [[]]  # The empty row will have the header

        for i in results['nets'][0].keys():
            contato_nets.append([i, results['nets'][0][i]])

        tab_nets.add_rows(contato_nets)
        tab_nets.set_cols_align(['c', 'c'])
        tab_nets.header(['Dados do Host', '  '])
        print(tab_nets.draw() + 2 * '\n')


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
    print ('########################################\n')
    print ('# Códigos de Identificação Localizados #\n')
    print ('########################################\n')
    #asterisco = len(str_codigo_ident_localizado) + len(gcode['content'])
    #print(asterisco * '#')
    #print(str_codigo_ident_localizado)
    #print(asterisco * '#')
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
    print('[BR] Google Analitycs ID: %s' % analitycs_id)
    print('[BR] Google Analitycs ID OLD: %s' % analitycs_id_old)
    print('[BR] Google Ad Sense ID: %s' % ad_sense_id)
    #print(asterisco * '#' + '\n\n')

    str_links_encontrados = '# Links Encontrados #'
    print(len(str_links_encontrados) * '#')
    print(str_links_encontrados)
    print(len(str_links_encontrados) * '#' + '\n')

    links = soup.find_all("a")
    for link in links:
        print("{}".format(link.get("href")))
    print('#####################')
    print(2 * '\n')


if __name__ == '__main__':

    ntpservs = ['a.st1.ntp.br', ' b.st1.ntp.br',
                ' c.st1.ntp.br', 'd.st1.ntp.br']

    '''
    Verifica se o argumento essencial, o nome de domínio, foi informado na
    execução. Caso contrário solicita ao usuário que informe
    '''

    if len(sys.argv) > 1:
        dominio_analisado = sys.argv[1]
    else:
        dominio_analisado = input('Digite a raiz do dominio: ')

    # Melhorando o quadro de título do relatório
    str_titulo = '# RELATÓRIO - ANALISE DO DOMÍNIO:'
    espacos = 60 - 37 - len(dominio_analisado)
    print(60 * '#')
    print('%s %s %s #' % (str_titulo, dominio_analisado, espacos * ' '))
    print('# FTM - Version 0.1 %s #' % (38 * ' '))
    print(60 * '#')

    print('\n\nVerificação das Informações existentes e publicamente disponíveis acerca do\n'
          'domínio {}, com a finalidade de identificar elementos que possam\n'
          'levar a identificação da autoria, tais como: responsável pelo registro do nome\n'
          'de domínio, empresa responsável pela hospedagem e códigos de identificação únicos\n '
          'de serviços agregados ao site. Relatório gerado pelo software Follow to The Money - FTM,\n'
          'com informações publicamente disponíveis na rede mundial de computadores acerca\n'
          'do domínio analisado. O FTM é um software livre, licenciado em GPL 3 e desenvolvido\n'
          'em Python 3.5, com código fonte disponível em http://github.com/tocvieira/ftm'. format(dominio_analisado))

    # print('\n')
    # check_dominio_analisado(dominio_analisado)
    # print('\n')

    ntpbr_time = ntp_time(ntpservs)
    print('\n\nHorário da Execução - NTP.br: {}'.format(ntpbr_time))

    dicsubdominios = {}
    # ipsubdominios = {}

    print("\n\nServidores Identificados:\n")
    servidores = findservidor(dominio_analisado, dicsubdominios)
    for k, v in servidores.items():
        print(k, v)

    print('\n\nInformações do nome do domínio %s: \n' % dominio_analisado)
    if d_whois(dominio_analisado):
        print('\n\nATENÇÃO! O NAME SERVER indica a utilização de uma Rede de Fornecimento de Conteúdo (Content Delivery Network – CDN)')
    else:
        pass

    print(2 * '\n')
    ip_whois(dicsubdominios)
    print(2 * '\n')
    get_ids("http://" + dominio_analisado)
