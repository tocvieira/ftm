#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exemplo de uso do FTM - Follow the Money v2.0
Demonstra as funcionalidades melhoradas do módulo analyze.py

Autor: Thiago Oliveira Castro Vieira
Versão: 2.0
"""

import logging
from ftm.analyze import analyze

# Configurar logging para ver o progresso detalhado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def demonstrar_melhorias():
    """
    Demonstra as principais melhorias implementadas na versão 2.0
    """
    print("🚀 FTM - Follow the Money v2.0")
    print("=" * 50)
    print("Demonstração das melhorias implementadas:\n")
    
    print("✅ Paralelização na busca de subdomínios")
    print("✅ Biblioteca requests para maior robustez")
    print("✅ Retry automático para falhas temporárias")
    print("✅ Verificação segura de certificados SSL")
    print("✅ Consultas DNS otimizadas")
    print("✅ Sistema de logging profissional")
    print("✅ Tratamento correto de timezone brasileiro")
    print("✅ Documentação completa com docstrings")
    print("✅ Correções de bugs e melhor tratamento de erros\n")

def analisar_dominio_completo(dominio):
    """
    Realiza análise completa de um domínio e exibe os resultados formatados.
    
    Args:
        dominio (str): O domínio a ser analisado
    """
    print(f"🔍 Iniciando análise completa de: {dominio}")
    print("-" * 60)
    
    try:
        # Executar análise
        resultados = analyze(dominio)
        
        # Desempacotar resultados
        horario, whois, ssl, dns, subdominios, ids, links, tecnologias, contatos = resultados
        
        # Exibir resultados formatados
        print("\n📊 RELATÓRIO DE ANÁLISE")
        print("=" * 60)
        
        print(f"\n🕐 Horário Oficial (NTP Brasil):")
        print(f"   {horario}")
        
        print(f"\n📋 Informações WHOIS:")
        whois_lines = whois.split('\n')[:5]  # Primeiras 5 linhas
        for line in whois_lines:
            if line.strip():
                print(f"   {line}")
        if len(whois.split('\n')) > 5:
            print("   ... (mais informações disponíveis)")
        
        print(f"\n🔒 Certificado SSL:")
        ssl_lines = ssl.split('\n')[:3]  # Primeiras 3 linhas
        for line in ssl_lines:
            if line.strip():
                print(f"   {line}")
        
        print(f"\n🌐 Registros DNS:")
        dns_lines = dns.split('\n')[:6]  # Primeiros 6 registros
        for line in dns_lines:
            if line.strip():
                print(f"   {line}")
        
        print(f"\n🔍 Subdomínios Encontrados:")
        if subdominios and len(subdominios.strip()) > 0:
            subdominios_list = subdominios.split('\n')[:5]
            for subdominio in subdominios_list:
                if subdominio.strip():
                    print(f"   {subdominio}")
            if len(subdominios.split('\n')) > 5:
                print("   ... (mais subdomínios encontrados)")
        else:
            print("   Nenhum subdomínio adicional encontrado")
        
        print(f"\n🆔 IDs de Rastreamento:")
        if ids and len(ids.strip()) > 0:
            ids_lines = ids.split('\n')[:3]
            for line in ids_lines:
                if line.strip():
                    print(f"   {line}")
        else:
            print("   Nenhum ID de rastreamento encontrado")
        
        print(f"\n⚙️ Tecnologias Detectadas:")
        if tecnologias and len(tecnologias.strip()) > 0:
            tech_lines = tecnologias.split('\n')[:5]
            for line in tech_lines:
                if line.strip():
                    print(f"   {line}")
        else:
            print("   Nenhuma tecnologia específica detectada")
        
        print(f"\n📞 Informações de Contato:")
        if contatos and len(contatos.strip()) > 0:
            contact_lines = contatos.split('\n')[:3]
            for line in contact_lines:
                if line.strip():
                    print(f"   {line}")
        else:
            print("   Nenhuma informação de contato encontrada")
        
        print("\n✅ Análise concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante a análise: {e}")
        logging.error(f"Erro na análise de {dominio}: {e}")

def exemplo_uso_basico():
    """
    Exemplo básico de uso da função analyze
    """
    print("\n📝 EXEMPLO DE USO BÁSICO")
    print("=" * 40)
    
    codigo_exemplo = '''
# Importar a função
from ftm.analyze import analyze

# Analisar um domínio
resultados = analyze('exemplo.com')

# Desempacotar os resultados
horario, whois, ssl, dns, subdominios, ids, links, tecnologias, contatos = resultados

# Usar as informações
print(f"Horário: {horario}")
print(f"WHOIS: {whois[:100]}...")  # Primeiros 100 caracteres
print(f"SSL: {ssl[:100]}...")     # Primeiros 100 caracteres
'''
    
    print(codigo_exemplo)

def main():
    """
    Função principal - demonstra o uso do FTM v2.0
    """
    demonstrar_melhorias()
    
    # Solicitar domínio para análise
    print("\n" + "=" * 60)
    dominio = input("Digite um domínio para análise (ex: example.com): ").strip()
    
    if dominio:
        analisar_dominio_completo(dominio)
    else:
        print("\n🔍 Executando análise de exemplo com 'example.com'...")
        analisar_dominio_completo('example.com')
    
    exemplo_uso_basico()
    
    print("\n" + "=" * 60)
    print("📚 Para mais informações, consulte o README.md")
    print("🐛 Para reportar bugs ou sugestões, abra uma issue no GitHub")
    print("⚖️  Lembre-se: use apenas em domínios próprios ou com autorização!")

if __name__ == "__main__":
    main()