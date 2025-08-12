#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de Integração do Sistema Otimizado F.T.M

Este arquivo demonstra como integrar o novo sistema de bypass avançado
com o código existente do F.T.M, mantendo compatibilidade total.

Autor: F.T.M Team
Versão: 2.0 - Otimizada
Data: 2024
"""

import json
import time
from datetime import datetime
from ftm.get_ids_optimized import get_ids, advanced_cloudflare_bypass, AdvancedCloudflareBypass

def exemplo_uso_basico():
    """
    Exemplo de uso básico - compatível com versão anterior
    """
    print("\n🎯 EXEMPLO 1: Uso Básico (Compatível com versão anterior)")
    print("=" * 60)
    
    url = "https://httpbin.org"
    print(f"Analisando: {url}")
    
    # Uso idêntico à versão anterior
    ids, links, technologies, contacts = get_ids(url)
    
    print(f"\n📊 Resultados:")
    print(f"   • IDs de Rastreamento: {len(ids)}")
    print(f"   • Links: {len(links)}")
    print(f"   • Tecnologias: {len(technologies)}")
    print(f"   • Contatos: {len(contacts)}")
    
    if ids:
        print(f"\n🔍 IDs Encontrados:")
        for id_found in ids:
            print(f"   • {id_found}")
    
    if technologies:
        print(f"\n🔧 Tecnologias:")
        for tech in technologies:
            print(f"   • {tech}")
    
    return ids, links, technologies, contacts

def exemplo_bypass_avancado():
    """
    Exemplo usando o sistema de bypass avançado diretamente
    """
    print("\n🛡️ EXEMPLO 2: Sistema de Bypass Avançado")
    print("=" * 60)
    
    # URLs com diferentes níveis de proteção
    urls_teste = [
        "https://httpbin.org",
        "https://example.com",
        "https://www.google.com"
    ]
    
    bypass_system = AdvancedCloudflareBypass()
    
    resultados = []
    
    for url in urls_teste:
        print(f"\n🎯 Testando: {url}")
        
        start_time = time.time()
        
        # Usa bypass avançado
        html = bypass_system.advanced_cloudflare_bypass(url, max_retries=2)
        
        elapsed_time = time.time() - start_time
        
        if html:
            print(f"✅ Sucesso em {elapsed_time:.2f}s - {len(html)} caracteres")
            resultados.append({
                'url': url,
                'success': True,
                'time': elapsed_time,
                'content_length': len(html)
            })
        else:
            print(f"❌ Falha após {elapsed_time:.2f}s")
            resultados.append({
                'url': url,
                'success': False,
                'time': elapsed_time,
                'content_length': 0
            })
    
    # Mostra estatísticas finais
    print(f"\n📈 Estatísticas Finais:")
    sucessos = sum(1 for r in resultados if r['success'])
    print(f"   • Taxa de Sucesso: {sucessos}/{len(resultados)} ({sucessos/len(resultados)*100:.1f}%)")
    
    tempo_medio = sum(r['time'] for r in resultados) / len(resultados)
    print(f"   • Tempo Médio: {tempo_medio:.2f}s")
    
    return resultados

def exemplo_analise_multipla():
    """
    Exemplo de análise de múltiplos sites com relatório JSON
    """
    print("\n📊 EXEMPLO 3: Análise Múltipla com Relatório")
    print("=" * 60)
    
    sites_para_analisar = [
        "https://httpbin.org",
        "https://example.com",
        "https://www.github.com"
    ]
    
    relatorio = {
        'timestamp': datetime.now().isoformat(),
        'total_sites': len(sites_para_analisar),
        'resultados': []
    }
    
    for i, url in enumerate(sites_para_analisar, 1):
        print(f"\n🔍 Analisando {i}/{len(sites_para_analisar)}: {url}")
        
        start_time = time.time()
        
        try:
            ids, links, technologies, contacts = get_ids(url)
            
            elapsed_time = time.time() - start_time
            
            resultado = {
                'url': url,
                'success': True,
                'analysis_time': round(elapsed_time, 2),
                'ids_found': len(ids),
                'links_found': len(links),
                'technologies': technologies,
                'contacts_found': len(contacts),
                'tracking_ids': ids,
                'error': None
            }
            
            print(f"   ✅ Concluído: {len(ids)} IDs, {len(technologies)} tecnologias")
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            
            resultado = {
                'url': url,
                'success': False,
                'analysis_time': round(elapsed_time, 2),
                'ids_found': 0,
                'links_found': 0,
                'technologies': [],
                'contacts_found': 0,
                'tracking_ids': [],
                'error': str(e)
            }
            
            print(f"   ❌ Erro: {str(e)}")
        
        relatorio['resultados'].append(resultado)
    
    # Salva relatório em JSON
    nome_arquivo = f"relatorio_ftm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Relatório salvo em: {nome_arquivo}")
    
    # Mostra resumo
    sucessos = sum(1 for r in relatorio['resultados'] if r['success'])
    total_ids = sum(r['ids_found'] for r in relatorio['resultados'])
    total_tecnologias = set()
    
    for resultado in relatorio['resultados']:
        total_tecnologias.update(resultado['technologies'])
    
    print(f"\n📈 Resumo da Análise:")
    print(f"   • Sites Analisados: {relatorio['total_sites']}")
    print(f"   • Taxa de Sucesso: {sucessos}/{relatorio['total_sites']} ({sucessos/relatorio['total_sites']*100:.1f}%)")
    print(f"   • Total de IDs Encontrados: {total_ids}")
    print(f"   • Tecnologias Únicas: {len(total_tecnologias)}")
    
    if total_tecnologias:
        print(f"   • Tecnologias Detectadas: {', '.join(sorted(total_tecnologias))}")
    
    return relatorio

def exemplo_monitoramento_continuo():
    """
    Exemplo de monitoramento contínuo de um site
    """
    print("\n⏰ EXEMPLO 4: Monitoramento Contínuo")
    print("=" * 60)
    
    url_monitorar = "https://httpbin.org"
    intervalo_segundos = 30  # Monitora a cada 30 segundos
    max_iteracoes = 3  # Para demonstração, apenas 3 iterações
    
    print(f"Monitorando: {url_monitorar}")
    print(f"Intervalo: {intervalo_segundos}s")
    print(f"Iterações: {max_iteracoes}")
    
    historico = []
    
    for i in range(max_iteracoes):
        print(f"\n🔄 Iteração {i+1}/{max_iteracoes}")
        
        timestamp = datetime.now()
        
        try:
            ids, links, technologies, contacts = get_ids(url_monitorar)
            
            registro = {
                'timestamp': timestamp.isoformat(),
                'ids_count': len(ids),
                'technologies': technologies,
                'links_count': len(links),
                'contacts_count': len(contacts),
                'success': True
            }
            
            print(f"   ✅ {timestamp.strftime('%H:%M:%S')}: {len(ids)} IDs, {len(technologies)} tecnologias")
            
        except Exception as e:
            registro = {
                'timestamp': timestamp.isoformat(),
                'error': str(e),
                'success': False
            }
            
            print(f"   ❌ {timestamp.strftime('%H:%M:%S')}: Erro - {str(e)}")
        
        historico.append(registro)
        
        # Aguarda próxima iteração (exceto na última)
        if i < max_iteracoes - 1:
            print(f"   ⏳ Aguardando {intervalo_segundos}s...")
            time.sleep(intervalo_segundos)
    
    # Análise do histórico
    print(f"\n📊 Análise do Monitoramento:")
    sucessos = sum(1 for r in historico if r.get('success', False))
    print(f"   • Taxa de Sucesso: {sucessos}/{len(historico)} ({sucessos/len(historico)*100:.1f}%)")
    
    if sucessos > 0:
        ids_medio = sum(r.get('ids_count', 0) for r in historico if r.get('success')) / sucessos
        print(f"   • Média de IDs por análise: {ids_medio:.1f}")
        
        todas_tecnologias = set()
        for registro in historico:
            if registro.get('success') and 'technologies' in registro:
                todas_tecnologias.update(registro['technologies'])
        
        if todas_tecnologias:
            print(f"   • Tecnologias detectadas: {', '.join(sorted(todas_tecnologias))}")
    
    return historico

def exemplo_comparacao_performance():
    """
    Exemplo comparando performance entre métodos
    """
    print("\n⚡ EXEMPLO 5: Comparação de Performance")
    print("=" * 60)
    
    url_teste = "https://httpbin.org"
    
    # Teste com função otimizada
    print("\n🚀 Testando versão otimizada...")
    start_time = time.time()
    ids_otimizado, links_otimizado, techs_otimizado, contacts_otimizado = get_ids(url_teste)
    tempo_otimizado = time.time() - start_time
    
    print(f"   ✅ Concluído em {tempo_otimizado:.2f}s")
    print(f"   📊 Resultados: {len(ids_otimizado)} IDs, {len(techs_otimizado)} tecnologias")
    
    # Teste com bypass direto
    print("\n🛡️ Testando bypass direto...")
    start_time = time.time()
    html_direto = advanced_cloudflare_bypass(url_teste)
    tempo_direto = time.time() - start_time
    
    if html_direto:
        print(f"   ✅ Bypass concluído em {tempo_direto:.2f}s")
        print(f"   📄 Conteúdo: {len(html_direto)} caracteres")
    else:
        print(f"   ❌ Bypass falhou após {tempo_direto:.2f}s")
    
    # Comparação
    print(f"\n📈 Comparação de Performance:")
    print(f"   • Análise Completa: {tempo_otimizado:.2f}s")
    print(f"   • Bypass Direto: {tempo_direto:.2f}s")
    
    if tempo_direto > 0:
        eficiencia = (tempo_direto / tempo_otimizado) * 100
        print(f"   • Eficiência da Análise Completa: {eficiencia:.1f}% do tempo do bypass direto")

def main():
    """
    Função principal que executa todos os exemplos
    """
    print("🚀 F.T.M - EXEMPLOS DE INTEGRAÇÃO DO SISTEMA OTIMIZADO")
    print("=" * 80)
    
    try:
        # Executa todos os exemplos
        exemplo_uso_basico()
        exemplo_bypass_avancado()
        exemplo_analise_multipla()
        exemplo_monitoramento_continuo()
        exemplo_comparacao_performance()
        
        print("\n" + "=" * 80)
        print("🎉 TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!")
        print("=" * 80)
        
        print("\n💡 Próximos Passos:")
        print("   1. Integre o código otimizado em seus projetos")
        print("   2. Customize os parâmetros conforme necessário")
        print("   3. Monitore as métricas de performance")
        print("   4. Reporte bugs ou sugestões")
        
        print("\n📚 Documentação Completa:")
        print("   • Leia o arquivo BYPASS_AVANCADO_README.md")
        print("   • Execute demo_bypass_avancado.py para demonstrações interativas")
        print("   • Consulte get_ids_optimized.py para detalhes técnicos")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Execução interrompida pelo usuário.")
    except Exception as e:
        print(f"\n💥 Erro durante execução: {str(e)}")
        raise

if __name__ == "__main__":
    main()