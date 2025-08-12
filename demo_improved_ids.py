#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Demonstração das melhorias na detecção de códigos de identificação
"""

from ftm.analyze import analyze

def demo_improved_detection():
    print("=" * 70)
    print("DEMONSTRAÇÃO: CÓDIGOS DE IDENTIFICAÇÃO MELHORADOS")
    print("=" * 70)
    
    # Teste com GitHub
    print("\n🔍 Testando GitHub...")
    try:
        result = analyze('https://github.com')
        ids = result[5]  # IDs estão na posição 5
        technologies = result[7]  # Tecnologias na posição 7
        
        print(f"\n📊 IDs detectados ({len(ids)}):")
        for id_item in ids:
            print(f"  • {id_item}")
            
        print(f"\n🛠️ Tecnologias detectadas ({len(technologies)}):")
        for tech in technologies:
            print(f"  • {tech}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n" + "=" * 70)
    print("PIXELS MODERNOS SUPORTADOS:")
    print("=" * 70)
    
    modern_pixels = {
        "TikTok Pixel": ["ttq.load()", "IDs de 20 caracteres"],
        "LinkedIn Insight Tag": ["_linkedin_partner_id", "Partner IDs 6-8 dígitos"],
        "Twitter Pixel (X)": ["twq('init')", "IDs alfanuméricos 5-10 chars"],
        "Pinterest Tag": ["pintrk('load')", "IDs de 13 dígitos"],
        "Snapchat Pixel": ["snaptr('init')", "UUIDs de 36 caracteres"],
        "Facebook Pixel (Meta)": ["fbq('init')", "IDs de 15-16 dígitos"],
        "YouTube Analytics": ["youtube.com/embed", "Channel IDs"],
        "Criteo Pixel": ["criteo_q.push", "Account IDs"],
        "Reddit Pixel": ["rdt('init')", "IDs de 6-8 caracteres"],
        "Quora Pixel": ["qp('init')", "IDs de 32 caracteres"]
    }
    
    for pixel, details in modern_pixels.items():
        print(f"✅ {pixel}:")
        print(f"   - Padrão: {details[0]}")
        print(f"   - Formato: {details[1]}")
        print()
    
    print("🚀 MELHORIAS IMPLEMENTADAS:")
    improvements = [
        "• Múltiplos padrões regex por plataforma",
        "• Validação específica de formato de ID", 
        "• Suporte a plataformas sociais modernas",
        "• Detecção robusta com fallbacks",
        "• Compatibilidade com versões atuais dos pixels"
    ]
    
    for improvement in improvements:
        print(improvement)

if __name__ == "__main__":
    demo_improved_detection()