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
                            return "\n".join(ids), "\n".join(links)
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