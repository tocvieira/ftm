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
    if validators.domain(dominio_analisado):
        pass
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
        'portal',
        'smtp')
    for subs in subdominios:
        try:
            print('{} : {}'.format(subs, socket.gethostbyname(
                subs + '.' + dominio_analisado)))
            dicsubdominios[subs] = socket.gethostbyname(
                subs + '.' + dominio_analisado)
        except socket.gaierror:
            pass
    return dicsubdominios


def d_whois(dominio_analisado):
    whois = pythonwhois.get_whois(dominio_analisado)

    tab_contato = tt.Texttable()

    contato_list = [[]]  # The empty row will have the header

    for i in whois['contacts']['admin'].keys():
        contato_list.append([i, whois['contacts']['admin'][i]])

    tab_contato.add_rows(contato_list)
    tab_contato.set_cols_align(['c', 'c'])
    tab_contato.header(['Contato', dominio_analisado])
    print(tab_contato.draw() + '\n')

    tab_billing = tt.Texttable()

    contato_billing = [[]]  # The empty row will have the header

    for i in whois['contacts']['registrant'].keys():
        contato_billing.append([i, whois['contacts']['registrant'][i]])

    tab_billing.add_rows(contato_billing)
    tab_billing.set_cols_align(['c', 'c'])
    tab_billing.header(['Resp. Pagamento', dominio_analisado])
    print(tab_billing.draw() + '\n')

    tab_tech = tt.Texttable()

    contato_tech = [[]]  # The empty row will have the header

    for i in whois['contacts']['tech'].keys():
        contato_tech.append([i, whois['contacts']['tech'][i]])

    tab_tech.add_rows(contato_tech)
    tab_tech.set_cols_align(['c', 'c'])
    tab_tech.header(['Resp. Técnico', dominio_analisado])
    print(tab_tech.draw())

    print('\nOutras Informações \nData de Criação: {}'.format(
        whois['creation_date']))
    print('Data de Expiração: {}'.format(whois['expiration_date']))
    print('Name Servers: {}'.format(whois['nameservers']))
    print('Registrar: {}'.format(whois['registrar']))
    print('Status: {}'.format(whois['status']))
    print('Servidor de WHOIS: {}'.format(whois['whois_server']))

    if 'CLOUDFLARE' in whois['nameservers'][0]:
        cdn = True
    else:
        cdn = False
    return cdn


def ip_whois(dicsubdominios):
    for (k, v) in dicsubdominios.items():
        hosts = IPWhois(v)  # .lookup_rws()
        results = hosts.lookup_whois()
        print('Host - {}: {}'.format(k, v))

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
    str_codigo_ident_localizado = '# Códigos de Identificação Localizados #'
    print(len(str_codigo_ident_localizado) * '#')
    print(str_codigo_ident_localizado)
    print(len(str_codigo_ident_localizado) * '#')
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

    str_links_encontrados = '# Links Encontrados #'
    print(len(str_links_encontrados) * '#')
    print(str_links_encontrados)
    print(len(str_links_encontrados) * '#' + '\n')

    links = soup.find_all("a")
    for link in links:
        print("{}".format(link.get("href")))
    print('#####################')


def main():

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

    print(57 * '#')
    print('# RELATÓRIO - ANALISE DO DOMÍNIO: {}                    #'.format(dominio_analisado))
    print('# FTM - Version 0.1                                     #')
    print(57 * '#')

    print('\n\nVerificação das Informações existentes e publicamente disponíveis acerca do\n'
          'domínio {}, com a finalidade de identificar elementos que possam\n'
          'levar a identificação da autoria, tais como: responsável pelo registro do nome\n'
          'de domínio, empresa responsável pela hospedagem e códigos de identificação únicos\n '
          'de serviços agregados ao site. Relatório gerado pelo software Follow to The Money - FTM,\n'
          'com informações publicamente disponíveis na rede mundial de computadores acerca\n'
          'do domínio analisado. O FTM é um software livre, licenciado em GPL 3 e desenvolvido\n'
          'em Python 3.5, com código fonte disponível em http://github.com/XXXXXX'. format(dominio_analisado))

    print('\n')
    check_dominio_analisado(dominio_analisado)
    print('\n')

    ntpbr_time = ntp_time(ntpservs)
    print('Horário da Execução - NTP.br: {}'.format(ntpbr_time))

    dicsubdominios = {}
    ipsuddominios = {}

    print("\n \n Servidores Identificados:\n\n")
    findservidor(dominio_analisado, dicsubdominios)

    print('\n\nInformações do nome do domínio {}: \n'.format(dominio_analisado))
    cdn = d_whois(dominio_analisado)
    if cdn == True:
        print('\n\nATENÇÃO! O NAME SERVER indica a utilização de uma Rede de Fornecimento de Conteúdo (Content Delivery Network – CDN)')
    else:
        pass
    print('\n\n')
    ip_whois(dicsubdominios)
    print('\n\n')
    get_ids("http://" + dominio_analisado)


if __name__ == '__main__':
    main()
