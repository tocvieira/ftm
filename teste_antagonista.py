#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do Sistema Otimizado F.T.M com oantagonista.com
"""

import sys
sys.path.append('.')

from ftm.get_ids_optimized import get_ids

def main():
    print('TESTE COM OANTAGONISTA.COM - SISTEMA OTIMIZADO')
    print('=' * 60)
    
    url = 'https://oantagonista.com'
    print(f'Testando: {url}')
    print('Iniciando bypass avançado...')
    
    try:
        result = get_ids(url)
        
        print(f'\nResultado:')
        print(f'  • IDs de Rastreamento: {result["tracking_ids"]}')
        print(f'  • Links: {result["links"]}')
        print(f'  • Tecnologias: {result["technologies"]}')
        print(f'  • Contatos: {result["contacts"]}')
        
        if result['ids_list']:
            print('\nIDs encontrados:')
            for id_found in result['ids_list']:
                print(f'  - {id_found}')
        
        if result['technologies_list']:
            print('\nTecnologias detectadas:')
            for tech in result['technologies_list']:
                print(f'  - {tech}')
        
        if result['contacts_list']:
            print('\nContatos encontrados:')
            for contact in result['contacts_list'][:5]:  # Mostra apenas os primeiros 5
                print(f'  - {contact}')
            if len(result['contacts_list']) > 5:
                print(f'  ... e mais {len(result["contacts_list"]) - 5} contatos')
        
        print('\n' + '=' * 60)
        print('✅ TESTE CONCLUÍDO COM SUCESSO!')
        
    except Exception as e:
        print(f'\n❌ ERRO: {str(e)}')
        print('=' * 60)
        raise

if __name__ == '__main__':
    main()