#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demonstração do Sistema Avançado de Bypass do Cloudflare - F.T.M Otimizado

Este script demonstra as capacidades avançadas do novo sistema de bypass
que inclui múltiplas estratégias para contornar proteções anti-bot modernas.

Autor: F.T.M Team
Versão: 2.0 - Otimizada
Data: 2024
"""

import sys
import time
import logging
from ftm.get_ids_optimized import (
    get_ids, 
    advanced_cloudflare_bypass, 
    AdvancedCloudflareBypass,
    ProtectionType,
    BypassMethod
)

# Configuração de logging para demonstração
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def demonstrar_bypass_basico():
    """
    Demonstra o uso básico da função get_ids otimizada
    """
    print("\n" + "="*80)
    print("🚀 DEMONSTRAÇÃO: Bypass Básico com get_ids()")
    print("="*80)
    
    # URLs de teste com diferentes níveis de proteção
    urls_teste = [
        "https://httpbin.org",  # Sem proteção
        "https://example.com",   # Básico
        "https://www.google.com", # Proteção moderada
    ]
    
    for url in urls_teste:
        print(f"\n🎯 Testando: {url}")
        print("-" * 50)
        
        start_time = time.time()
        
        try:
            ids, links, technologies, contacts = get_ids(url)
            
            elapsed_time = time.time() - start_time
            
            print(f"✅ Análise concluída em {elapsed_time:.2f}s")
            print(f"📊 Resultados:")
            print(f"   • IDs de Rastreamento: {len(ids)}")
            print(f"   • Links Encontrados: {len(links)}")
            print(f"   • Tecnologias: {len(technologies)}")
            print(f"   • Contatos: {len(contacts)}")
            
            if ids:
                print(f"\n🔍 IDs Detectados:")
                for i, id_found in enumerate(ids[:5], 1):  # Mostra apenas os primeiros 5
                    print(f"   {i}. {id_found}")
                if len(ids) > 5:
                    print(f"   ... e mais {len(ids) - 5} IDs")
            
            if technologies:
                print(f"\n🔧 Tecnologias Detectadas:")
                for tech in technologies:
                    print(f"   • {tech}")
            
            if contacts:
                print(f"\n📧 Contatos Encontrados:")
                for contact in contacts[:3]:  # Mostra apenas os primeiros 3
                    print(f"   • {contact}")
                if len(contacts) > 3:
                    print(f"   ... e mais {len(contacts) - 3} contatos")
                    
        except Exception as e:
            print(f"❌ Erro na análise: {str(e)}")
        
        print("\n" + "="*50)

def demonstrar_bypass_avancado():
    """
    Demonstra o uso avançado do sistema de bypass
    """
    print("\n" + "="*80)
    print("🛡️ DEMONSTRAÇÃO: Sistema Avançado de Bypass")
    print("="*80)
    
    # Cria instância do bypass avançado
    bypass_system = AdvancedCloudflareBypass()
    
    # URLs com diferentes tipos de proteção (para demonstração)
    urls_protegidas = [
        "https://httpbin.org/status/403",  # Simula bloqueio
        "https://httpbin.org/delay/2",     # Simula delay
        "https://httpbin.org/redirect/3",  # Simula redirecionamentos
    ]
    
    print("\n📋 Testando diferentes cenários de proteção...")
    
    for i, url in enumerate(urls_protegidas, 1):
        print(f"\n🎯 Teste {i}: {url}")
        print("-" * 60)
        
        start_time = time.time()
        
        try:
            # Usa o bypass avançado diretamente
            html = bypass_system.advanced_cloudflare_bypass(url, max_retries=2)
            
            elapsed_time = time.time() - start_time
            
            if html:
                print(f"✅ Bypass bem-sucedido em {elapsed_time:.2f}s")
                print(f"📄 Conteúdo obtido: {len(html)} caracteres")
                
                # Mostra estatísticas do bypass
                print("\n📈 Estatísticas de Métodos:")
                for method, stats in bypass_system.bypass_stats.items():
                    if stats['attempts'] > 0:
                        success_rate = (stats['successes'] / stats['attempts']) * 100
                        print(f"   • {method.value}: {success_rate:.1f}% ({stats['successes']}/{stats['attempts']})")
            else:
                print(f"❌ Bypass falhou após {elapsed_time:.2f}s")
                
        except Exception as e:
            print(f"💥 Erro no bypass: {str(e)}")

def demonstrar_deteccao_protecoes():
    """
    Demonstra a detecção de diferentes tipos de proteção
    """
    print("\n" + "="*80)
    print("🔍 DEMONSTRAÇÃO: Detecção de Proteções Anti-Bot")
    print("="*80)
    
    # Simula diferentes tipos de conteúdo com proteções
    exemplos_protecao = {
        "Cloudflare Challenge": """
        <html>
        <head><title>Just a moment...</title></head>
        <body>
        <div>Checking your browser before accessing the website.</div>
        <div id="cf-challenge-running">Please wait...</div>
        </body>
        </html>
        """,
        
        "Cloudflare Under Attack": """
        <html>
        <head><title>Under Attack Mode</title></head>
        <body>
        <div>This website is under attack and using Cloudflare protection.</div>
        <script>var cf_challenge_response = true;</script>
        </body>
        </html>
        """,
        
        "Incapsula Protection": """
        <html>
        <head><title>Access Denied</title></head>
        <body>
        <div>Access denied by Incapsula security policy.</div>
        <div>Incident ID: 12345</div>
        </body>
        </html>
        """,
        
        "Site Normal": """
        <html>
        <head><title>Welcome</title></head>
        <body>
        <h1>Welcome to our website</h1>
        <p>This is a normal website without protection.</p>
        </body>
        </html>
        """
    }
    
    bypass_system = AdvancedCloudflareBypass()
    detector = bypass_system.protection_detector
    
    print("\n🔍 Testando detecção de proteções...")
    
    for nome, html_exemplo in exemplos_protecao.items():
        print(f"\n📋 Testando: {nome}")
        print("-" * 40)
        
        # Detecta o tipo de proteção
        protecao_detectada = detector.detect_protection(
            html_exemplo, 
            {}, 
            200
        )
        
        print(f"🛡️ Proteção detectada: {protecao_detectada.value}")
        
        # Sugere estratégia baseada na proteção
        if protecao_detectada == ProtectionType.CLOUDFLARE:
            print("💡 Estratégia sugerida: Cloudscraper → Undetected Chrome → TLS Client")
        elif protecao_detectada == ProtectionType.INCAPSULA:
            print("💡 Estratégia sugerida: TLS Client → curl_cffi → Requests avançado")
        elif protecao_detectada == ProtectionType.NONE:
            print("💡 Estratégia sugerida: Requests padrão (mais rápido)")
        else:
            print("💡 Estratégia sugerida: Fallback completo (todos os métodos)")

def demonstrar_rotacao_user_agents():
    """
    Demonstra o sistema de rotação inteligente de User-Agents
    """
    print("\n" + "="*80)
    print("🔄 DEMONSTRAÇÃO: Rotação Inteligente de User-Agents")
    print("="*80)
    
    bypass_system = AdvancedCloudflareBypass()
    ua_rotator = bypass_system.ua_rotator
    
    print("\n🎭 Gerando User-Agents baseados em estatísticas reais...")
    
    navegadores = ['chrome', 'firefox', 'safari', 'edge']
    
    for navegador in navegadores:
        print(f"\n🌐 {navegador.title()}:")
        print("-" * 30)
        
        for i in range(3):
            user_agent = ua_rotator.get_random_agent(navegador)
            headers = ua_rotator.get_matching_headers(user_agent)
            
            print(f"  {i+1}. {user_agent[:80]}...")
            print(f"     Headers compatíveis: {len(headers)} headers")
    
    print("\n🎲 User-Agents aleatórios (baseados em estatísticas de mercado):")
    print("-" * 60)
    
    for i in range(5):
        user_agent = ua_rotator.get_random_agent()
        print(f"  {i+1}. {user_agent}")

def menu_principal():
    """
    Menu principal da demonstração
    """
    print("\n" + "="*80)
    print("🚀 F.T.M - SISTEMA AVANÇADO DE BYPASS DO CLOUDFLARE")
    print("="*80)
    print("\n🎯 Capacidades do Sistema Otimizado:")
    print("   • Bypass inteligente com 6 métodos diferentes")
    print("   • Detecção automática de proteções (Cloudflare, Incapsula, etc.)")
    print("   • Rotação avançada de User-Agents baseada em estatísticas reais")
    print("   • Sistema de fallback hierárquico")
    print("   • Delays adaptativos e simulação de comportamento humano")
    print("   • Gerenciamento avançado de cookies e sessões")
    print("   • Suporte para JA3 fingerprint spoofing")
    print("   • Compatibilidade com TLS moderno e HTTP/2")
    
    print("\n📋 Escolha uma demonstração:")
    print("   1. 🎯 Bypass Básico (get_ids otimizado)")
    print("   2. 🛡️ Sistema Avançado de Bypass")
    print("   3. 🔍 Detecção de Proteções")
    print("   4. 🔄 Rotação de User-Agents")
    print("   5. 🚀 Executar Todas as Demonstrações")
    print("   0. ❌ Sair")
    
    while True:
        try:
            escolha = input("\n👉 Digite sua escolha (0-5): ").strip()
            
            if escolha == '0':
                print("\n👋 Obrigado por usar o F.T.M otimizado!")
                sys.exit(0)
            elif escolha == '1':
                demonstrar_bypass_basico()
            elif escolha == '2':
                demonstrar_bypass_avancado()
            elif escolha == '3':
                demonstrar_deteccao_protecoes()
            elif escolha == '4':
                demonstrar_rotacao_user_agents()
            elif escolha == '5':
                print("\n🚀 Executando todas as demonstrações...")
                demonstrar_bypass_basico()
                demonstrar_bypass_avancado()
                demonstrar_deteccao_protecoes()
                demonstrar_rotacao_user_agents()
                print("\n✅ Todas as demonstrações concluídas!")
            else:
                print("❌ Escolha inválida. Digite um número de 0 a 5.")
                continue
            
            input("\n⏸️ Pressione Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Demonstração interrompida pelo usuário.")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Erro: {str(e)}")
            input("\n⏸️ Pressione Enter para continuar...")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Programa encerrado pelo usuário.")
    except Exception as e:
        print(f"\n💥 Erro fatal: {str(e)}")
        sys.exit(1)