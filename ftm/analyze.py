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
import sys
import os
# Importa python-whois (biblioteca mais estável)
try:
    import whois
    WHOIS_AVAILABLE = True
    print("✓ Python-whois disponível - funcionalidade WHOIS ativada")
except ImportError:
    WHOIS_AVAILABLE = False
    print("⚠ Python-whois não instalado. Para funcionalidade WHOIS, instale com: pip install python-whois")
import re
import urllib.request
from bs4 import BeautifulSoup
from ipwhois import IPWhois
from time import ctime
from ntplib import NTPClient, NTPException
import ssl
import dns.resolver
import datetime
import requests
import pytz
import random
import time
import gzip



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
        'smtp',
        'm',
        'www2',
        'dev',
        'remote',
        'server',
        'webmail',
        'ns1',
        'ns2',
        'secure',
        'vpn',
        'shop',
        'mail2',
        'teste',
        'ns',
        'host',
        '1',
        '2',
        'mx1',
        'exchange',
        'api',
        'news',
        'vps',
        'gov',
        'owa',
        'cloud',
    )
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
    if not WHOIS_AVAILABLE:
        return f"WHOIS para {dominio_analisado}:\nFuncionalidade WHOIS não disponível. Instale python-whois: pip install python-whois"
    
    try:
        # Limpa o domínio para consulta
        dominio_limpo = dominio_analisado
        if dominio_limpo.startswith(('http://', 'https://')):
            dominio_limpo = dominio_limpo.split('://')[1]
        if dominio_limpo.startswith('www.'):
            dominio_limpo = dominio_limpo[4:]
        if '/' in dominio_limpo:
            dominio_limpo = dominio_limpo.split('/')[0]
        
        print(f"Consultando WHOIS para: {dominio_limpo}")
        
        # Consulta WHOIS
        domain_info = whois.whois(dominio_limpo)
        
        if not domain_info:
            return f"WHOIS para {dominio_analisado}:\nNenhuma informação WHOIS encontrada."
        
        # Função auxiliar para formatar dados
        def format_data(data):
            if not data:
                return "Não informado"
            if isinstance(data, list):
                return ', '.join(str(item) for item in data if item)
            return str(data)
        
        def format_date(date_data):
            if not date_data:
                return "Não informado"
            if isinstance(date_data, list):
                return str(date_data[0]) if date_data else "Não informado"
            return str(date_data)
        
        # Monta informações organizadas
        whois_info = []
        whois_info.append(f"📋 INFORMAÇÕES WHOIS - {dominio_analisado.upper()}")
        whois_info.append("═" * 60)
        
        # 🏢 INFORMAÇÕES BÁSICAS DO DOMÍNIO
        whois_info.append("\n🏢 INFORMAÇÕES BÁSICAS")
        whois_info.append("─" * 30)
        
        domain_name = format_data(domain_info.domain_name)
        if domain_name != "Não informado":
            whois_info.append(f"• Domínio: {domain_name.upper()}")
        
        registrar = format_data(domain_info.registrar)
        whois_info.append(f"• Registrador: {registrar}")
        
        if hasattr(domain_info, 'registrar_url') and domain_info.registrar_url:
            whois_info.append(f"• URL do Registrador: {domain_info.registrar_url}")
        
        whois_server = getattr(domain_info, 'whois_server', None)
        if whois_server:
            whois_info.append(f"• Servidor WHOIS: {whois_server}")
        
        # 📅 DATAS IMPORTANTES
        whois_info.append("\n📅 DATAS IMPORTANTES")
        whois_info.append("─" * 30)
        
        creation_date = format_date(domain_info.creation_date)
        whois_info.append(f"• Data de Criação: {creation_date}")
        
        expiration_date = format_date(domain_info.expiration_date)
        whois_info.append(f"• Data de Expiração: {expiration_date}")
        
        updated_date = format_date(domain_info.updated_date)
        whois_info.append(f"• Última Atualização: {updated_date}")
        
        # 🔒 STATUS E CONFIGURAÇÕES
        whois_info.append("\n🔒 STATUS E CONFIGURAÇÕES")
        whois_info.append("─" * 30)
        
        status = format_data(domain_info.status)
        whois_info.append(f"• Status: {status}")
        
        name_servers = format_data(domain_info.name_servers)
        if name_servers != "Não informado":
            whois_info.append(f"• Servidores DNS: {name_servers.upper()}")
        
        dnssec = getattr(domain_info, 'dnssec', None)
        if dnssec:
            whois_info.append(f"• DNSSEC: {dnssec}")
        
        # 👤 INFORMAÇÕES DO REGISTRANTE
        registrant_info = []
        
        # Nome do registrante
        registrant_name = getattr(domain_info, 'registrant_name', None) or getattr(domain_info, 'name', None)
        if registrant_name:
            registrant_info.append(f"• Nome: {registrant_name}")
        
        # Organização
        org = getattr(domain_info, 'org', None)
        if org:
            registrant_info.append(f"• Organização: {org}")
        
        # Endereço
        address = getattr(domain_info, 'address', None)
        if address:
            addr_formatted = format_data(address)
            registrant_info.append(f"• Endereço: {addr_formatted}")
        
        # Cidade, Estado, CEP
        city = getattr(domain_info, 'city', None)
        if city:
            registrant_info.append(f"• Cidade: {city}")
        
        state = getattr(domain_info, 'state', None)
        if state:
            registrant_info.append(f"• Estado: {state}")
        
        zipcode = getattr(domain_info, 'zipcode', None)
        if zipcode:
            registrant_info.append(f"• CEP: {zipcode}")
        
        country = getattr(domain_info, 'country', None)
        if country:
            registrant_info.append(f"• País: {country}")
        
        if registrant_info:
            whois_info.append("\n👤 INFORMAÇÕES DO REGISTRANTE")
            whois_info.append("─" * 30)
            whois_info.extend(registrant_info)
        
        # 📞 INFORMAÇÕES DE CONTATO
        contact_info = []
        
        emails = getattr(domain_info, 'emails', None)
        if emails:
            emails_formatted = format_data(emails)
            contact_info.append(f"• E-mails: {emails_formatted}")
        
        phone = getattr(domain_info, 'phone', None)
        if phone:
            contact_info.append(f"• Telefone: {phone}")
        
        fax = getattr(domain_info, 'fax', None)
        if fax:
            contact_info.append(f"• Fax: {fax}")
        
        if contact_info:
            whois_info.append("\n📞 INFORMAÇÕES DE CONTATO")
            whois_info.append("─" * 30)
            whois_info.extend(contact_info)
        
        # 👨‍💼 CONTATO ADMINISTRATIVO
        admin_info = []
        admin_name = getattr(domain_info, 'admin_name', None)
        if admin_name:
            admin_info.append(f"• Nome: {admin_name}")
            
            admin_org = getattr(domain_info, 'admin_org', None)
            if admin_org:
                admin_info.append(f"• Organização: {admin_org}")
            
            admin_email = getattr(domain_info, 'admin_email', None)
            if admin_email:
                admin_info.append(f"• E-mail: {admin_email}")
            
            admin_phone = getattr(domain_info, 'admin_phone', None)
            if admin_phone:
                admin_info.append(f"• Telefone: {admin_phone}")
        
        if admin_info:
            whois_info.append("\n👨‍💼 CONTATO ADMINISTRATIVO")
            whois_info.append("─" * 30)
            whois_info.extend(admin_info)
        
        # 🔧 CONTATO TÉCNICO
        tech_info = []
        tech_name = getattr(domain_info, 'tech_name', None)
        if tech_name:
            tech_info.append(f"• Nome: {tech_name}")
            
            tech_org = getattr(domain_info, 'tech_org', None)
            if tech_org:
                tech_info.append(f"• Organização: {tech_org}")
            
            tech_email = getattr(domain_info, 'tech_email', None)
            if tech_email:
                tech_info.append(f"• E-mail: {tech_email}")
            
            tech_phone = getattr(domain_info, 'tech_phone', None)
            if tech_phone:
                tech_info.append(f"• Telefone: {tech_phone}")
        
        if tech_info:
            whois_info.append("\n🔧 CONTATO TÉCNICO")
            whois_info.append("─" * 30)
            whois_info.extend(tech_info)
        
        # 📄 INFORMAÇÕES TÉCNICAS DETALHADAS (apenas se necessário)
        if hasattr(domain_info, 'text') and domain_info.text and len(domain_info.text) > 0:
            whois_info.append("\n📄 INFORMAÇÕES TÉCNICAS DETALHADAS")
            whois_info.append("─" * 30)
            
            # domain_info.text pode ser uma lista de strings ou uma string única
            if isinstance(domain_info.text, list):
                # Se é uma lista, junta as strings
                raw_text = '\n'.join(str(item) for item in domain_info.text)
            else:
                # Se é uma string única
                raw_text = str(domain_info.text)
            
            # Processa as linhas do texto bruto
            lines = raw_text.split('\n')
            relevant_lines = []
            
            for line in lines:
                line = line.strip()
                # Filtra linhas vazias e comentários
                if line and not line.startswith('%') and not line.startswith('#'):
                    relevant_lines.append(f"  {line}")
            
            # Limita o número de linhas para melhor legibilidade
            if len(relevant_lines) > 40:
                whois_info.extend(relevant_lines[:40])
                whois_info.append("  ... (informações adicionais omitidas para melhor legibilidade)")
            else:
                whois_info.extend(relevant_lines)
        
        whois_info.append("\n" + "═" * 60)
        whois_info.append("✅ Consulta WHOIS concluída com sucesso")
        
        return '\n'.join(whois_info)
        
    except Exception as e:
        error_msg = str(e)
        if "No whois server" in error_msg:
            return f"❌ WHOIS para {dominio_analisado}:\n\n🚫 Servidor WHOIS não encontrado para este domínio.\n\nℹ️ Alguns domínios podem não ter informações WHOIS públicas disponíveis."
        elif "connection" in error_msg.lower():
            return f"❌ WHOIS para {dominio_analisado}:\n\n🌐 Erro de conexão com servidor WHOIS.\n\nℹ️ Verifique sua conexão com a internet e tente novamente."
        else:
            return f"❌ WHOIS para {dominio_analisado}:\n\n⚠️ Erro ao consultar WHOIS: {error_msg}\n\n🔧 Detalhes técnicos: {str(e)}"


def ip_whois(dicsubdominios):
    result = {}
    for (k, v) in dicsubdominios.items():
        try:
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
        except Exception as e:
            # Em caso de erro no WHOIS, adiciona uma mensagem informativa
            result[k] = f"Erro ao obter WHOIS para {v}: {str(e)}\n\n"
    return result


def get_ids(url):
    """Extrai códigos de identificação e links de uma página web"""
    ids = []
    links = []
    social_links = []
    external_links = []
    internal_links = []
    contact_info = []
    technologies = []
    
    try:
        # Tenta acessar a página - primeiro tenta com http://
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            
        # Lista de User-Agents para tentar contornar bloqueios
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'
        ]
        
        # Headers mais completos para simular um navegador real
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Pragma': 'no-cache'
        }
        
        # Função para tentar acessar a URL com diferentes configurações
        def try_access_url(current_url, current_headers, is_retry=False):
            try:
                # Adiciona um atraso aleatório para parecer mais humano
                if is_retry:
                    time.sleep(random.uniform(1, 3))
                    
                req = urllib.request.Request(current_url, data=None, headers=current_headers)
                
                # Configura um opener com suporte a cookies
                opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
                response = opener.open(req, timeout=15)
                
                # Lida com possível compressão gzip
                if response.info().get('Content-Encoding') == 'gzip':
                    html = gzip.decompress(response.read()).decode('utf-8', errors='ignore')
                else:
                    html = response.read().decode('utf-8', errors='ignore')
                    
                return html
            except Exception as e:
                if not is_retry:
                    # Tenta com outro User-Agent em caso de falha
                    current_headers['User-Agent'] = random.choice(user_agents)
                    return try_access_url(current_url, current_headers, True)
                raise e
        
        # Tenta acessar com HTTP primeiro
        try:
            html = try_access_url(url, headers)
            soup = BeautifulSoup(html, 'html.parser')
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            # Se for erro 403 (Forbidden), tenta com mais técnicas anti-bloqueio
            if isinstance(e, urllib.error.HTTPError) and e.code == 403:
                try:
                    # Tenta com um referrer de um grande site
                    headers['Referer'] = 'https://www.google.com/'
                    html = try_access_url(url, headers)
                    soup = BeautifulSoup(html, 'html.parser')
                except Exception:
                    # Tenta com HTTPS se HTTP falhar
                    if url.startswith('http://') and not url.startswith('https://'):
                        https_url = 'https://' + url[7:]
                        try:
                            html = try_access_url(https_url, headers)
                            soup = BeautifulSoup(html, 'html.parser')
                        except Exception as e2:
                            ids.append(f"Erro ao acessar o site (HTTPS): {str(e2)}")
                            return "\n".join(ids), "\n".join(links), technologies, technologies, technologies, technologies, technologies, technologies
                    else:
                        ids.append(f"Erro ao acessar o site: {str(e)}")
                        return "\n".join(ids), "\n".join(links)
            # Se não for 403, tenta com HTTPS
            elif url.startswith('http://') and not url.startswith('https://'):
                https_url = 'https://' + url[7:]
                try:
                    html = try_access_url(https_url, headers)
                    soup = BeautifulSoup(html, 'html.parser')
                except Exception as e2:
                    ids.append(f"Erro ao acessar o site (HTTPS): {str(e2)}")
                    return "\n".join(ids), "\n".join(links)
            else:
                ids.append(f"Erro ao acessar o site: {str(e)}")
                return "\n".join(ids), "\n".join(links)
        
        # Extrai o domínio base da URL para identificar links internos/externos
        base_domain = url.split('//')[-1].split('/')[0]
        
        # Google Analytics (formato antigo UA-XXXXX-X)
        ga_pattern = re.compile(r'UA-[0-9]+-[0-9]+', re.IGNORECASE)
        ga_matches = ga_pattern.findall(html)
        if ga_matches:
            ids.append(f"Google Analytics (UA): {', '.join(set(ga_matches))}")
        
        # Google Analytics 4 (formato G-XXXXXXX)
        ga4_pattern = re.compile(r'G-[A-Z0-9]{7,10}', re.IGNORECASE)
        ga4_matches = ga4_pattern.findall(html)
        if ga4_matches:
            ids.append(f"Google Analytics 4 (GA4): {', '.join(set(ga4_matches))}")
        
        # Google AdSense
        adsense_pattern = re.compile(r'pub-[0-9]+', re.IGNORECASE)
        adsense_matches = adsense_pattern.findall(html)
        if adsense_matches:
            ids.append(f"Google AdSense: {', '.join(set(adsense_matches))}")
        
        # Google Site Verification
        site_verification = soup.find('meta', attrs={'name': 'google-site-verification'})
        if site_verification:
            ids.append(f"Google Site Verification: {site_verification.get('content')}")
        
        # Microsoft Bing Verification
        msvalidate = soup.find('meta', attrs={'name': 'msvalidate.01'})
        if msvalidate:
            ids.append(f"Microsoft Bing Verification: {msvalidate.get('content')}")
        
        # Juicy Ad Code
        juicy_pattern = re.compile(r'juicy_code = \'([0-9]+)\'', re.IGNORECASE)
        juicy_matches = juicy_pattern.findall(html)
        if juicy_matches:
            ids.append(f"Juicy Ad Code: {', '.join(set(juicy_matches))}")
        
        # Facebook Pixel
        fb_pixel_pattern = re.compile(r'fbq\(\'init\', \'([0-9]+)\'\)', re.IGNORECASE)
        fb_pixel_matches = fb_pixel_pattern.findall(html)
        if fb_pixel_matches:
            ids.append(f"Facebook Pixel: {', '.join(set(fb_pixel_matches))}")
        
        # Google Tag Manager
        gtm_pattern = re.compile(r'GTM-[A-Z0-9]+', re.IGNORECASE)
        gtm_matches = gtm_pattern.findall(html)
        if gtm_matches:
            ids.append(f"Google Tag Manager: {', '.join(set(gtm_matches))}")
        
        # Hotjar
        hotjar_pattern = re.compile(r'hjid:([0-9]+)', re.IGNORECASE)
        hotjar_matches = hotjar_pattern.findall(html)
        if hotjar_matches:
            ids.append(f"Hotjar ID: {', '.join(set(hotjar_matches))}")
        
        # Tecnologias detectadas
        # WordPress
        if 'wp-content' in html or 'wp-includes' in html:
            technologies.append("WordPress")
        
        # Joomla
        if 'joomla' in html.lower():
            technologies.append("Joomla")
        
        # Drupal
        if 'drupal' in html.lower():
            technologies.append("Drupal")
        
        # Bootstrap
        if 'bootstrap' in html.lower():
            technologies.append("Bootstrap")
        
        # jQuery
        if 'jquery' in html.lower():
            technologies.append("jQuery")
        
        # React
        if 'react' in html.lower() or '_reactRootContainer' in html:
            technologies.append("React")
        
        # Angular
        if 'ng-' in html or 'angular' in html.lower():
            technologies.append("Angular")
        
        # Vue.js
        if 'vue' in html.lower() or 'v-' in html:
            technologies.append("Vue.js")
        
        if technologies:
            ids.append(f"Tecnologias detectadas: {', '.join(set(technologies))}")
        
        # Extração de informações de contato
        # E-mails
        email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', re.IGNORECASE)
        email_matches = email_pattern.findall(html)
        if email_matches:
            contact_info.append(f"E-mails: {', '.join(set(email_matches)[:5])}")
            if len(set(email_matches)) > 5:
                contact_info.append(f"... e mais {len(set(email_matches)) - 5} e-mails")
        
        # Telefones (formato brasileiro)
        phone_pattern = re.compile(r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}', re.IGNORECASE)
        phone_matches = phone_pattern.findall(html)
        if phone_matches:
            contact_info.append(f"Telefones: {', '.join(set(phone_matches)[:5])}")
            if len(set(phone_matches)) > 5:
                contact_info.append(f"... e mais {len(set(phone_matches)) - 5} telefones")
        
        if contact_info:
            ids.append("Informações de contato:")
            ids.extend(contact_info)
        
        # Extração de links
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href and not href.startswith('#') and not href.startswith('javascript:'):
                # Normaliza o link
                if href.startswith('/'):
                    href = url.rstrip('/') + href
                elif not href.startswith(('http://', 'https://', 'ftp://')):
                    href = url.rstrip('/') + '/' + href
                
                # Categoriza o link
                if any(social in href.lower() for social in ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com', 'youtube.com', 'pinterest.com', 'tiktok.com']):
                    social_links.append(href)
                elif base_domain in href:
                    internal_links.append(href)
                else:
                    external_links.append(href)
        
        # Adiciona links categorizados
        if social_links:
            links.append("Links de Redes Sociais:")
            links.extend(social_links[:10])
            if len(social_links) > 10:
                links.append(f"... e mais {len(social_links) - 10} links de redes sociais")
        
        if external_links:
            links.append("\nLinks Externos:")
            links.extend(external_links[:15])
            if len(external_links) > 15:
                links.append(f"... e mais {len(external_links) - 15} links externos")
        
        if internal_links:
            links.append("\nLinks Internos:")
            links.extend(internal_links[:10])
            if len(internal_links) > 10:
                links.append(f"... e mais {len(internal_links) - 10} links internos")
    
    except Exception as e:
        ids.append(f"Erro ao acessar o site: {str(e)}")
    
    return "\n".join(ids), "\n".join(links)


def check_ssl(dominio_analisado):
    """Verifica informações do certificado SSL do domínio"""
    try:
        # Primeiro, verificar se o domínio responde na porta 443
        try:
            # Tentar conectar com timeout de 5 segundos
            sock = socket.create_connection((dominio_analisado, 443), timeout=5)
            sock.close()
        except (socket.timeout, socket.error) as e:
            return f"Certificado SSL: Não disponível (o servidor não responde na porta 443)"
        
        # Configurar contexto SSL com opções mais permissivas
        context = ssl.create_default_context()
        context.check_hostname = False  # Não verificar o nome do host
        context.verify_mode = ssl.CERT_NONE  # Não verificar o certificado
        
        # Tentar obter o certificado
        with socket.create_connection((dominio_analisado, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=dominio_analisado) as ssock:
                cert = ssock.getpeercert(binary_form=False)
                if not cert:  # Se o certificado estiver em formato binário, tentar novamente
                    cert = ssock.getpeercert()
                
                # Extrair informações relevantes
                issued_to = cert.get('subject', [])
                issued_by = cert.get('issuer', [])
                valid_from = cert.get('notBefore', '')
                valid_until = cert.get('notAfter', '')
                
                # Formatar saída
                ssl_info = []
                ssl_info.append(f"Certificado SSL: Válido")
                
                # Emissor
                issuer_cn = None
                for item in issued_by:
                    if item[0][0] == 'commonName':
                        issuer_cn = item[0][1]
                if issuer_cn:
                    ssl_info.append(f"Emitido por: {issuer_cn}")
                
                # Validade
                if valid_from and valid_until:
                    ssl_info.append(f"Válido de: {valid_from}")
                    ssl_info.append(f"Válido até: {valid_until}")
                    
                    # Verificar se está próximo de expirar
                    try:
                        expiry_date = ssl.cert_time_to_seconds(valid_until)
                        current_time = datetime.datetime.now().timestamp()
                        days_remaining = int((expiry_date - current_time) / 86400)
                        ssl_info.append(f"Dias restantes: {days_remaining}")
                    except Exception as e:
                        ssl_info.append(f"Não foi possível calcular dias restantes: {str(e)}")
                
                # Domínios alternativos (SAN)
                alt_names = []
                for ext in cert.get('subjectAltName', []):
                    if ext[0].lower() == 'dns':
                        alt_names.append(ext[1])
                if alt_names:
                    ssl_info.append(f"Nomes alternativos: {', '.join(alt_names[:5])}")
                    if len(alt_names) > 5:
                        ssl_info.append(f"... e mais {len(alt_names) - 5} domínios")
                
                return "\n".join(ssl_info)
    except ssl.SSLError as e:
        return f"Certificado SSL: Erro SSL ({str(e)})"
    except socket.gaierror as e:
        return f"Certificado SSL: Erro de resolução de nome ({str(e)})"
    except socket.timeout as e:
        return f"Certificado SSL: Timeout na conexão ({str(e)})"
    except Exception as e:
        return f"Certificado SSL: Não disponível ou erro ({str(e)})"

def check_dns_records(dominio_analisado):
    """Verifica registros DNS do domínio"""
    dns_info = []
    
    # Tipos de registros a verificar
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
    
    # Configurar resolvedores DNS alternativos para melhorar a confiabilidade
    resolvers = [
        '8.8.8.8',        # Google DNS
        '1.1.1.1',        # Cloudflare DNS
        '208.67.222.222', # OpenDNS
        '200.160.0.10'    # DNS do Registro.br (para domínios .br)
    ]
    
    # Criar um resolvedor personalizado
    resolver = dns.resolver.Resolver()
    resolver.timeout = 5.0  # Timeout em segundos
    resolver.lifetime = 10.0  # Tempo máximo para uma consulta
    
    domain_exists = False
    connection_errors = 0
    total_attempts = 0
    
    # Tentar com diferentes servidores DNS
    for record_type in record_types:
        records_found = False
        
        for dns_server in resolvers:
            if records_found:
                break
                
            total_attempts += 1
            try:
                # Configurar o servidor DNS atual
                resolver.nameservers = [dns_server]
                
                # Tentar resolver
                answers = resolver.resolve(dominio_analisado, record_type)
                records = []
                
                for rdata in answers:
                    if record_type == 'MX':
                        records.append(f"{rdata.preference} {rdata.exchange}")
                    else:
                        records.append(str(rdata))
                
                if records:
                    dns_info.append(f"Registros {record_type}:")
                    for record in records:
                        dns_info.append(f"  {record}")
                    records_found = True
                    domain_exists = True
            except dns.resolver.NoAnswer:
                # Sem resposta para este tipo de registro, mas domínio existe
                domain_exists = True
                continue
            except dns.resolver.NXDOMAIN:
                # Domínio não existe - erro definitivo
                return f"Erro: O domínio '{dominio_analisado}' não existe ou não está registrado"
            except dns.resolver.NoNameservers:
                # Nenhum servidor de nomes disponível
                connection_errors += 1
                continue
            except Exception as e:
                # Outros erros, tentar com outro servidor DNS
                connection_errors += 1
                continue
    
    # Análise dos resultados
    if not dns_info:
        if not domain_exists:
            if connection_errors == total_attempts:
                return "Erro: Falha na conexão com servidores DNS. Verifique sua conexão com a internet"
            else:
                return f"Erro: Não foi possível obter registros DNS para '{dominio_analisado}'. O domínio pode estar com problemas de configuração DNS"
        else:
            return f"Aviso: O domínio '{dominio_analisado}' existe, mas não possui registros DNS públicos visíveis"
    
    return "\n".join(dns_info)


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
    
    # Importa a função corrigida
    from .get_ids_fixed import get_ids as get_ids_fixed
    
    # Tenta obter IDs, links, tecnologias e informações de contato
    # A função get_ids já adiciona http:// se necessário
    from .get_ids_fixed import get_ids
    ids_list, links_list, technologies, contact_info = get_ids(dominio_analisado)
    
    # Converte listas para strings formatadas
    ids = "\n".join(ids_list)
    links_encontrados = "\n".join(links_list)
    
    # Novas informações
    ssl_info = check_ssl(dominio_analisado)
    dns_info = check_dns_records(dominio_analisado)

    # Prepara a lista de servidores como tuplas (nome, ip, whois)
    servidores_list = [(k, v, whois_subdomains.get(k, "Informação não disponível")) for k, v in servidores.items()]
    
    # Retorna uma tupla com 9 valores na ordem esperada pela view
    return (
        ntpbr_time,           # 0
        whois,                # 1
        ssl_info,             # 2
        dns_info,             # 3
        servidores_list,      # 4
        ids,                  # 5
        links_encontrados,    # 6
        technologies,         # 7
        contact_info          # 8
    )

