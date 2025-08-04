#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import scrape_books as sb

def main():
    print("=" * 70)
    print("SCRAPER DE LIVRES - books.toscrape.com")
    print("=" * 70)

    try:
        confirmation = input("\nVoulez-vous continuer ? (oui/non) [oui]: ").strip().lower()
        if confirmation and confirmation not in ['oui', 'o', 'yes', 'y']:
            print("❌ Opération annulée par l'utilisateur")
            return
    except KeyboardInterrupt:
        print("\n❌ Opération annulée par l'utilisateur")
        return

    try:
        if not os.path.exists('images'):
            os.makedirs('images')
            print("Dossier 'images' créé")

        sb.scrape_all_categories()

        print("SCRAPING TERMINÉ AVEC SUCCÈS!")

    except KeyboardInterrupt:
        print("\n\nInterruption détectée (Ctrl+C)")
        print("Arrêt du scraping en cours...")
        return

    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        print("Vérifiez votre connexion internet et réessayez")
        return 1

if __name__ == "__main__":
    sys.exit(main())
