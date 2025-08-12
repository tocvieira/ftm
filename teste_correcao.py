#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste das Correções Implementadas
Verifica se o ChromeDriver foi corrigido e testa com sites menos protegidos
"""

import sys
sys.path.append('ftm')

from ftm.get_ids_optimized import get_ids

def teste_correcoes():
    print("🔧 TESTE DAS CORREÇÕES IMPLEMENTADAS")
    print("=" * 50)
    
    # Lista de sites para teste (do menos para o mais protegido)
    sites_teste = [
        "https://httpbin.org/html",  # Site simples para teste
        "https://example.com",       # Site básico
        "https://www.google.com",    # Site com proteções moderadas
        "https://oantagonista.com"   # Site altamente protegido
    ]
    
    resultados = []
    
    for i, url in enumerate(sites_teste, 1):
        print(f"\n🌐 Teste {i}/4: {url}")
        print("-" * 40)
        
        try:
            resultado = get_ids(url)
            
            if resultado:
                ids = resultado.get('tracking_ids', 0)
                links = resultado.get('links', 0)
                techs = resultado.get('technologies', 0)
                contacts = resultado.get('contacts', 0)
                
                sucesso = ids > 0 or links > 0 or techs > 0 or contacts > 0
                
                print(f"✅ Sucesso: {sucesso}")
                print(f"📊 IDs: {ids} | Links: {links} | Techs: {techs} | Contatos: {contacts}")
                
                resultados.append({
                    'url': url,
                    'sucesso': sucesso,
                    'dados': {'ids': ids, 'links': links, 'techs': techs, 'contacts': contacts}
                })
            else:
                print("❌ Falha: Nenhum resultado retornado")
                resultados.append({'url': url, 'sucesso': False, 'dados': None})
                
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            resultados.append({'url': url, 'sucesso': False, 'erro': str(e)})
    
    # Relatório final
    print("\n" + "=" * 50)
    print("📋 RELATÓRIO FINAL DAS CORREÇÕES")
    print("=" * 50)
    
    sucessos = sum(1 for r in resultados if r['sucesso'])
    total = len(resultados)
    
    print(f"\n🎯 Taxa de Sucesso: {sucessos}/{total} ({sucessos/total*100:.1f}%)")
    
    print("\n📊 Detalhes por Site:")
    for resultado in resultados:
        status = "✅" if resultado['sucesso'] else "❌"
        print(f"  {status} {resultado['url']}")
        if resultado['sucesso'] and resultado.get('dados'):
            dados = resultado['dados']
            print(f"      📈 IDs: {dados['ids']} | Links: {dados['links']} | Techs: {dados['techs']} | Contatos: {dados['contacts']}")
    
    # Avaliação das correções
    print("\n🔧 Avaliação das Correções:")
    if sucessos >= 2:
        print("✅ CORREÇÕES FUNCIONANDO - ChromeDriver compatível")
        print("✅ Sistema otimizado operacional")
        if sucessos == total:
            print("🏆 PERFEITO - Todos os sites funcionaram!")
        else:
            print(f"⚠️  Sites altamente protegidos ainda desafiadores ({total-sucessos} falharam)")
    else:
        print("❌ CORREÇÕES INSUFICIENTES - Problemas persistem")
        print("🔧 Recomenda-se investigação adicional")
    
    print("\n" + "=" * 50)
    print("✅ TESTE DE CORREÇÕES CONCLUÍDO!")
    print("=" * 50)

if __name__ == "__main__":
    teste_correcoes()