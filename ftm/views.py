from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import JsonResponse
import validators
import json

from .analyze import analyze
from .get_ids_fixed import get_ids
from bs4 import BeautifulSoup
import re


def domain_validator(value):
    if not validators.domain(value):
        raise ValidationError("A sintax do domínio informado é inválida")


class MainForm(forms.Form):
    domain_name = forms.CharField(label="Dominio Analisado", validators=[domain_validator])


class ManualSourceForm(forms.Form):
    domain_name = forms.CharField(widget=forms.HiddenInput())
    source_code = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 15,
            'placeholder': 'Cole aqui o código fonte HTML da página...',
            'class': 'form-control'
        }),
        label="Código Fonte HTML"
    )


def analyze_manual_source(domain_name, source_code):
    """Analisa o código fonte fornecido manualmente pelo usuário com análise completa"""
    try:
        # Importa as funções de análise completa
        from .analyze import ntp_time, findservidor, d_whois, ip_whois, check_ssl, check_dns_records
        
        # Processa o HTML fornecido
        soup = BeautifulSoup(source_code, 'html.parser')
        html = source_code
        
        # === ANÁLISE COMPLETA (igual à função analyze) ===
        
        # 1. Hora NTP
        ntpservs = ['a.st1.ntp.br', 'b.st1.ntp.br', 'c.st1.ntp.br', 'd.st1.ntp.br']
        ntpbr_time = ntp_time(ntpservs)
        
        # 2. Servidores e subdomínios
        dicsubdominios = {}
        servidores = findservidor(domain_name, dicsubdominios)
        
        # 3. WHOIS
        whois = d_whois(domain_name)
        whois_subdomains = ip_whois(dicsubdominios)
        
        # 4. SSL e DNS
        ssl_info = check_ssl(domain_name)
        dns_info = check_dns_records(domain_name)
        
        # === EXTRAÇÃO DE IDs DO CÓDIGO FONTE ===
        
        # Extrai IDs únicos de diferentes plataformas
        unique_ids = []
        
        # Google Analytics (UA e GA4)
        ua_pattern = re.compile(r'UA-[\w-]+', re.IGNORECASE)
        ua_matches = ua_pattern.findall(html)
        for match in set(ua_matches):  # Remove duplicatas
            unique_ids.append(f'Google Analytics UA: {match}')
        
        ga4_pattern = re.compile(r'G-[A-Z0-9]{10}', re.IGNORECASE)
        ga4_matches = ga4_pattern.findall(html)
        for match in set(ga4_matches):  # Remove duplicatas
            unique_ids.append(f'Google Analytics GA4: {match}')
        
        # Google Tag Manager
        gtm_pattern = re.compile(r'GTM-[A-Z0-9]{6,8}', re.IGNORECASE)
        gtm_matches = gtm_pattern.findall(html)
        for match in set(gtm_matches):  # Remove duplicatas
            unique_ids.append(f'Google Tag Manager: {match}')
        
        # Facebook Pixel
        fb_pattern = re.compile(r'fbq\([^)]*["\']([0-9]{15,16})["\']', re.IGNORECASE)
        fb_matches = fb_pattern.findall(html)
        for match in set(fb_matches):  # Remove duplicatas
            unique_ids.append(f'Facebook Pixel: {match}')
        
        # Google AdSense
        adsense_pattern = re.compile(r'ca-pub-[0-9]{16}', re.IGNORECASE)
        adsense_matches = adsense_pattern.findall(html)
        for match in set(adsense_matches):  # Remove duplicatas
            unique_ids.append(f'Google AdSense: {match}')
        
        # Hotjar
        hotjar_pattern = re.compile(r'hjid["\']?:\s*["\']?([0-9]{6,8})', re.IGNORECASE)
        hotjar_matches = hotjar_pattern.findall(html)
        for match in set(hotjar_matches):  # Remove duplicatas
            unique_ids.append(f'Hotjar: {match}')
        
        # Google Site Verification
        gsv_pattern = re.compile(r'google-site-verification["\']?\s*content\s*=\s*["\']([^"\'>]+)', re.IGNORECASE)
        gsv_matches = gsv_pattern.findall(html)
        for match in set(gsv_matches):  # Remove duplicatas
            unique_ids.append(f'Google Site Verification: {match}')
        
        # Microsoft Bing Verification
        bing_pattern = re.compile(r'msvalidate\.01["\']?\s*content\s*=\s*["\']([^"\'>]+)', re.IGNORECASE)
        bing_matches = bing_pattern.findall(html)
        for match in set(bing_matches):  # Remove duplicatas
            unique_ids.append(f'Microsoft Bing Verification: {match}')
        
        # === EXTRAÇÃO DE LINKS ===
        
        links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href and href.startswith(('http://', 'https://')):
                links.append(href)
        
        # Remove duplicatas
        links = list(set(links))
        
        # === DETECÇÃO DE TECNOLOGIAS ===
        
        technologies = []
        
        # WordPress
        if 'wp-content' in html or 'wordpress' in html.lower():
            technologies.append('WordPress')
        
        # Joomla
        if 'joomla' in html.lower() or '/components/com_' in html:
            technologies.append('Joomla')
        
        # Drupal
        if 'drupal' in html.lower() or 'sites/default/files' in html:
            technologies.append('Drupal')
        
        # Bootstrap
        if 'bootstrap' in html.lower():
            technologies.append('Bootstrap')
        
        # jQuery
        if 'jquery' in html.lower():
            technologies.append('jQuery')
        
        # === FORMATAÇÃO DOS RESULTADOS (igual à função analyze) ===
        
        # Converte listas para strings formatadas
        ids_formatted = "\n".join(unique_ids) if unique_ids else "Nenhum ID encontrado"
        links_formatted = "\n".join(links) if links else "Nenhum link encontrado"
        
        # Retorna no mesmo formato da função analyze
        return {
            "dominio_analisado": domain_name,
            "ntpbr_time": ntpbr_time,
            "servidores": [(k, v, whois_subdomains[k]) for k, v in servidores.items()],
            "whois": whois,
            "ids": ids_formatted,
            "links_encontrados": links_formatted,
            "ssl_info": ssl_info,
            "dns_info": dns_info,
            "technologies": technologies,
            "source": "manual"
        }
        
    except Exception as e:
        return {
            "dominio_analisado": domain_name,
            "ntpbr_time": "Erro ao obter hora NTP",
            "servidores": [],
            "whois": f"Erro ao obter WHOIS: {str(e)}",
            "ids": f"Erro ao processar código fonte: {str(e)}",
            "links_encontrados": "Erro ao extrair links",
            "ssl_info": "Erro ao verificar SSL",
            "dns_info": "Erro ao verificar DNS",
            "technologies": [],
            "source": "manual"
        }


def index(request):
    form = MainForm()
    if request.method == "POST":
        form = MainForm(request.POST)
        if form.is_valid():
            domain_name = form.cleaned_data["domain_name"]
            
            # Chama a função analyze para obter todos os dados necessários
            try:
                result = analyze(domain_name)
                
                # A função analyze retorna 9 valores:
                # ntpbr_time, whois, ssl_info, dns_info, server_info, ids_list, links_list, technologies, contact_info
                ntpbr_time, whois, ssl_info, dns_info, server_info, ids_list, links_list, technologies, contact_info = result
                
                # Verifica se é necessária análise manual (Cloudflare/403 detectado)
                if isinstance(ids_list, str) and 'MANUAL_ANALYSIS_REQUIRED' in ids_list:
                    # Remove o indicador da string de IDs
                    ids_lines = ids_list.split('\n')
                    ids_list = '\n'.join([line for line in ids_lines if line != 'MANUAL_ANALYSIS_REQUIRED'])
                    
                    # Cria o formulário para entrada manual
                    manual_form = ManualSourceForm(initial={'domain_name': domain_name})
                    
                    # Renderiza o template de análise manual
                    return render(request, 'manual_source.html', {
                        'domain': domain_name,
                        'manual_form': manual_form,
                        'failed_result': {
                            'ids': ids_list.split('\n') if ids_list else [],
                            'links': links_list,
                            'technologies': technologies,
                            'contact_info': contact_info
                        }
                    })
                
                # Prepara os dados para o template
                context = {
                    'dominio_analisado': domain_name,
                    'ntpbr_time': ntpbr_time,
                    'whois': whois,
                    'ssl_info': ssl_info,
                    'dns_info': dns_info,
                    'servidores': server_info,  # Lista de tuplas (servidor, ip, whois)
                    'ids': ids_list,
                    'links_encontrados': links_list,
                    'technologies': technologies,
                    'contact_info': contact_info
                }
                
                # Renderiza o template normal com os resultados
                return render(request, 'result/index.html', context)
                
            except Exception as e:
                # Em caso de erro, mostra uma mensagem de erro
                return render(request, 'result/index.html', {
                    'dominio_analisado': domain_name,
                    'ntpbr_time': f'Erro: {str(e)}',
                    'whois': f'Erro na análise: {str(e)}',
                    'ssl_info': 'Erro ao obter informações SSL',
                    'dns_info': 'Erro ao obter informações DNS',
                    'servidores': [],
                    'ids': 'Erro ao extrair IDs',
                    'links_encontrados': 'Erro ao extrair links',
                    'technologies': [],
                    'contact_info': []
                })

    return render(request, "index.html", {"form": form})


def manual_analysis(request):
    """View para processar análise manual do código fonte"""
    if request.method == "POST":
        form = ManualSourceForm(request.POST)
        if form.is_valid():
            domain = form.cleaned_data['domain_name']
            source_code = form.cleaned_data['source_code']
            
            # Analisa o código fonte fornecido
            result = analyze_manual_source(domain, source_code)
            
            return render(request, "result/index.html", result)
    
    # Se não for POST, redireciona para a página inicial
    return render(request, "index.html", {"form": MainForm()})
