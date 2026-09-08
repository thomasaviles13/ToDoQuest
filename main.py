import flet as ft
import pandas as pd
import os
import time
import random
import threading

def main(page: ft.Page):
    # 📱 Configuration
    page.title = "To-Do Quest"
    page.window_width = 550
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F4F7FE"
    page.scroll = "adaptive"

    xp_totale = 0
    palier_niveau = 15
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fichier_excel = os.path.join(base_dir, "grimoire.xlsx")

    # Messages d'encouragement festifs
    messages_encouragement = [
        "🎉 Fantastique ! +{pts} XP ! 🚀",
        "🌟 Super travail ! +{pts} XP ! 💪",
        "🔥 En plein vol ! +{pts} XP ! ✨",
        "👑 Légendaire ! +{pts} XP ! 💎",
        "⚡ Boost d'énergie ! +{pts} XP ! 🏆",
        "🎯 Objectif atomisé ! +{pts} XP ! 🌈",
        "🌿 Tu gères la fougère ! +{pts} XP ! ⭐",
        "🚀 Vers l'infini et au-delà ! +{pts} XP ! 🎈"
    ]

    # ✨ Interface animée (En-tête & Barre XP)
    texte_niveau = ft.Text(
        "🌟 Niveau 1 | 0 XP", 
        size=22, 
        weight=ft.FontWeight.BOLD, 
        color="#FFA000"
    )

    badge_niveau = ft.Container(
        content=texte_niveau,
        padding=ft.padding.Padding(22, 10, 22, 10),
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=8, color="#D0D9E8", offset=ft.Offset(0, 4)),
        animate_scale=ft.Animation(350, ft.AnimationCurve.BOUNCE_OUT)
    )

    barre_xp = ft.ProgressBar(width=350, value=0.0, color="#FFC107", bgcolor="#FFE082", height=16)

    liste_quetes = ft.Column(spacing=15)

    # 🎁 Pop-up Cadeau
    dialogue_cadeau = ft.AlertDialog(
        title=ft.Text("🎊 PALIER ATTEINT ! 🎊", size=24, color="#E91E63", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        content=ft.Text("Bravo, tu peux te faire un cadeau ! 🎁", size=18, text_align=ft.TextAlign.CENTER),
        actions=[ft.TextButton("J'y vais de ce pas !", on_click=lambda e: setattr(dialogue_cadeau, 'open', False) or page.update())],
        actions_alignment=ft.MainAxisAlignment.CENTER
    )

    # 🏆 Pop-up Level Up
    dialogue_levelup = ft.AlertDialog(
        title=ft.Text("🏆 NIVEAU SUPÉRIEUR ! 🏆", size=24, color="#FF9800", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        content=ft.Column([
            ft.Text("✨ LEVEL UP ! ✨", size=20, weight=ft.FontWeight.BOLD, color="#4CAF50", text_align=ft.TextAlign.CENTER),
            ft.Text("Félicitations ! Tu as franchi un nouveau niveau ! 🚀", size=16, text_align=ft.TextAlign.CENTER),
        ], tight=True, alignment=ft.MainAxisAlignment.CENTER),
        actions=[ft.ElevatedButton("Continuer l'aventure !", on_click=lambda e: setattr(dialogue_levelup, 'open', False) or page.update(), bgcolor="#FF9800", color="white")],
        actions_alignment=ft.MainAxisAlignment.CENTER
    )

    # 💾 Sauvegarde dans Excel & Client Storage (Mobile/Web)
    def sauvegarder_donnees():
        donnees = [{"Tâches": c.data["nom"], "Durée": c.data["duree"], "Scoring 1/2/3": c.data["points"], "Récurrence": c.data["recurrence"], "Statut": c.data["statut"]} for c in liste_quetes.controls if hasattr(c, 'data') and c.data is not None]
        try:
            page.client_storage.set("todoquest_tasks", donnees)
        except Exception:
            pass
        try:
            pd.DataFrame(donnees).to_excel(fichier_excel, index=False)
        except Exception:
            pass

    # 🎆 Animation de confettis / particules
    def animer_confettis():
        def run():
            emojis = ["🎉", "✨", "⭐", "💎", "🌟", "🎈", "🚀", "🏆", "💥", "⚡"]
            particules = []
            for i in range(12):
                emoji = random.choice(emojis)
                start_left = random.randint(60, 440)
                start_top = random.randint(120, 280)
                
                particule = ft.Container(
                    content=ft.Text(emoji, size=random.randint(20, 30)),
                    left=start_left,
                    top=start_top,
                    opacity=1.0,
                    scale=0.4,
                    animate_opacity=ft.Animation(650, ft.AnimationCurve.EASE_OUT),
                    animate_position=ft.Animation(650, ft.AnimationCurve.EASE_OUT),
                    animate_scale=ft.Animation(650, ft.AnimationCurve.BOUNCE_OUT)
                )
                particules.append(particule)
                page.overlay.append(particule)
            
            page.update()
            time.sleep(0.05)

            for p in particules:
                p.top -= random.randint(50, 110)
                p.left += random.randint(-70, 70)
                p.scale = random.uniform(1.2, 1.8)
                p.opacity = 0.0
            
            page.update()
            time.sleep(0.7)

            for p in particules:
                if p in page.overlay:
                    page.overlay.remove(p)
            page.update()

        threading.Thread(target=run, daemon=True).start()

    # 🚀 Animation Badge XP Flottant
    def animer_badge_xp(points):
        def run():
            badge = ft.Container(
                content=ft.Row([
                    ft.Text(f"+{points} XP", size=18, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text("✨", size=18)
                ], tight=True, alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.Padding(16, 8, 16, 8),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.Alignment(-1, -1),
                    end=ft.alignment.Alignment(1, 1),
                    colors=["#FFD700", "#FF8C00"]
                ),
                border_radius=20,
                shadow=ft.BoxShadow(spread_radius=2, blur_radius=10, color="#FFB300", offset=ft.Offset(0, 4)),
                left=210,
                top=180,
                scale=0.2,
                opacity=0.0,
                animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_IN_OUT),
                animate_position=ft.Animation(700, ft.AnimationCurve.EASE_OUT),
                animate_scale=ft.Animation(400, ft.AnimationCurve.BOUNCE_OUT)
            )
            page.overlay.append(badge)
            page.update()
            time.sleep(0.05)

            badge.opacity = 1.0
            badge.scale = 1.25
            badge.top = 100
            page.update()
            time.sleep(0.45)

            badge.top = 40
            badge.opacity = 0.0
            badge.scale = 0.8
            page.update()
            time.sleep(0.35)

            if badge in page.overlay:
                page.overlay.remove(badge)
            page.update()

        threading.Thread(target=run, daemon=True).start()

    def maj_xp(delta_points):
        nonlocal xp_totale
        ancien_xp = xp_totale
        ancien_niveau = (ancien_xp // palier_niveau) + 1
        
        xp_totale = max(0, xp_totale + delta_points)
        niveau_actuel = (xp_totale // palier_niveau) + 1
        
        texte_niveau.value = f"🌟 Niveau {niveau_actuel} | {xp_totale} XP"
        barre_xp.value = (xp_totale % palier_niveau) / palier_niveau
        
        if delta_points > 0:
            # Rebond du badge de niveau
            badge_niveau.scale = 1.25
            texte_niveau.color = "#E91E63"
            page.update()

            def reset_badge():
                time.sleep(0.35)
                badge_niveau.scale = 1.0
                texte_niveau.color = "#FFA000"
                page.update()

            threading.Thread(target=reset_badge, daemon=True).start()

            # Lancer les particules et le badge flottant
            animer_badge_xp(delta_points)
            animer_confettis()

            # Détection de Level Up
            if niveau_actuel > ancien_niveau:
                def popup_levelup():
                    time.sleep(0.4)
                    if dialogue_levelup not in page.overlay:
                        page.overlay.append(dialogue_levelup)
                    dialogue_levelup.open = True
                    page.update()
                threading.Thread(target=popup_levelup, daemon=True).start()

            # Vérification du palier de 10 points pour le cadeau
            if (xp_totale // 10) > (ancien_xp // 10):
                def popup_cadeau():
                    time.sleep(0.6)
                    if dialogue_cadeau not in page.overlay:
                        page.overlay.append(dialogue_cadeau)
                    dialogue_cadeau.open = True
                    page.update()
                threading.Thread(target=popup_cadeau, daemon=True).start()
                
        page.update()

    # 🔄 Logique de la Boucle d'état
    def changer_statut(e):
        carte = e.control.data_carte
        b = e.control
        if carte.data["statut"] == 0:
            carte.data["statut"], b.content.value, b.bgcolor = 1, "⏳", "#FFA726"
        elif carte.data["statut"] == 1:
            carte.data["statut"], b.content.value, b.bgcolor = 2, "✅", "#4CAF50"
            
            # Animation sur la carte (Léger rebond)
            carte.scale = 1.04
            page.update()

            def reset_carte():
                time.sleep(0.2)
                carte.scale = 1.0
                page.update()
            threading.Thread(target=reset_carte, daemon=True).start()

            pts = carte.data["points"]
            maj_xp(pts)

            msg = random.choice(messages_encouragement).format(pts=pts)
            page.snack_bar = ft.SnackBar(
                ft.Text(msg, weight=ft.FontWeight.BOLD, size=15, color="white"),
                bgcolor="#2E7D32",
                behavior=ft.SnackBarBehavior.FLOATING,
                margin=15,
                shape=ft.RoundedRectangleBorder(radius=10)
            )
            page.snack_bar.open = True
        elif carte.data["statut"] == 2:
            carte.data["statut"], b.content.value, b.bgcolor = 0, "⚪", "#E0E0E0"
            maj_xp(-carte.data["points"])
        sauvegarder_donnees()
        page.update()

    def supprimer_carte(e):
        carte = e.control.data_carte
        if carte.data["statut"] == 2:
            maj_xp(-carte.data["points"])
        liste_quetes.controls.remove(carte)
        sauvegarder_donnees()
        page.update()

    # 🌙 Fonction Nouvelle Journée
    def nouvelle_journee(e):
        habitudes_restaurees = 0
        for carte in liste_quetes.controls:
            if hasattr(carte, 'data') and carte.data and carte.data.get("recurrence") and carte.data.get("statut") == 2:
                carte.data["statut"] = 0
                bouton_statut = carte.content.controls[3]
                bouton_statut.content.value = "⚪"
                bouton_statut.bgcolor = "#E0E0E0"
                habitudes_restaurees += 1
                
        if habitudes_restaurees > 0:
            sauvegarder_donnees()
            page.snack_bar = ft.SnackBar(
                ft.Text(f"🌙 Repos terminé ! {habitudes_restaurees} habitude(s) réinitialisée(s).", weight=ft.FontWeight.BOLD),
                bgcolor="#3F51B5", behavior=ft.SnackBarBehavior.FLOATING, margin=15, shape=ft.RoundedRectangleBorder(radius=10)
            )
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Aucune habitude terminée à réinitialiser."),
                bgcolor="#757575", behavior=ft.SnackBarBehavior.FLOATING, margin=15, shape=ft.RoundedRectangleBorder(radius=10)
            )
        page.snack_bar.open = True
        page.update()

    bouton_repos = ft.ElevatedButton(
        content=ft.Text("🌙 Terminer la journée (Reset Habitudes)", size=14, weight=ft.FontWeight.BOLD),
        bgcolor="#3F51B5", color="white", on_click=nouvelle_journee,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), padding=15)
    )

    # ✏️ Fenêtre de Modification
    carte_en_edition = [None]
    champ_edit_nom = ft.TextField(label="Nom de la quête")
    champ_edit_duree = ft.TextField(label="Durée estimée")
    champ_edit_xp = ft.Dropdown(options=[ft.dropdown.Option("1"), ft.dropdown.Option("2"), ft.dropdown.Option("3")])
    switch_edit_rec = ft.Switch(label="Habitude récurrente")

    def valider_edition(e):
        c = carte_en_edition[0]
        if c and champ_edit_nom.value:
            nouv_pts = int(champ_edit_xp.value)
            if c.data["statut"] == 2 and c.data["points"] != nouv_pts:
                maj_xp(nouv_pts - c.data["points"])
            c.data.update({"nom": champ_edit_nom.value, "duree": champ_edit_duree.value, "points": nouv_pts, "recurrence": switch_edit_rec.value})
            c.content.controls[0].controls[0].value = c.data["nom"]
            icone = "🔄" if c.data["recurrence"] else "🎯"
            c.content.controls[0].controls[1].value = f"{icone} {c.data['duree']} | 💎 {nouv_pts} XP"
            sauvegarder_donnees()
            dialogue_edit.open = False
            page.update()

    dialogue_edit = ft.AlertDialog(
        title=ft.Text("✏️ Modifier la Quête"),
        content=ft.Column([champ_edit_nom, champ_edit_duree, champ_edit_xp, switch_edit_rec], tight=True),
        actions=[ft.TextButton("Annuler", on_click=lambda e: setattr(dialogue_edit, 'open', False) or page.update()), ft.ElevatedButton("Sauvegarder", on_click=valider_edition, bgcolor="#2196F3", color="white")]
    )

    def ouvrir_edition(e):
        c = e.control.data_carte
        carte_en_edition[0] = c
        champ_edit_nom.value, champ_edit_duree.value = c.data["nom"], c.data["duree"]
        champ_edit_xp.value, switch_edit_rec.value = str(c.data["points"]), c.data["recurrence"]
        if dialogue_edit not in page.overlay:
            page.overlay.append(dialogue_edit)
        dialogue_edit.open = True
        page.update()

    # 🛠️ Usine à Quêtes
    def creer_carte(nom, duree, points, recurrence, statut=0):
        icones, couleurs = {0: "⚪", 1: "⏳", 2: "✅"}, {0: "#E0E0E0", 1: "#FFA726", 2: "#4CAF50"}
        bouton_statut = ft.ElevatedButton(content=ft.Text(icones[statut], size=20), bgcolor=couleurs[statut], on_click=changer_statut, style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=15))
        bouton_edit = ft.ElevatedButton(content=ft.Text("✏️", size=16), bgcolor="#E3F2FD", on_click=ouvrir_edition, style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=10))
        bouton_suppr = ft.ElevatedButton(content=ft.Text("🗑️", size=16), bgcolor="#FFEBEE", on_click=supprimer_carte, style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=10))
        
        carte = ft.Container(
            data={"nom": nom, "duree": duree, "points": points, "recurrence": recurrence, "statut": statut},
            content=ft.Row([
                ft.Column([ft.Text(nom, weight=ft.FontWeight.BOLD, size=16, color="#333333"), ft.Text(f"{'🔄' if recurrence else '🎯'} {duree} | 💎 {points} XP", color="#00796B", size=13)], expand=True),
                bouton_edit, bouton_suppr, bouton_statut
            ]),
            padding=15, bgcolor="white", border_radius=15, shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="#D3D3D3"),
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        )
        bouton_statut.data_carte = bouton_edit.data_carte = bouton_suppr.data_carte = carte 
        return carte

    # 📖 Lecture Initiale Robuste (Excel ou Client Storage)
    donnees_chargees = []
    if os.path.exists(fichier_excel):
        try:
            df = pd.read_excel(fichier_excel)
            if 'Statut' not in df.columns: df['Statut'] = 0
            if 'Scoring 1/2/3' not in df.columns: df['Scoring 1/2/3'] = 1
            df['Statut'] = df['Statut'].fillna(0).astype(int)
            df['Scoring 1/2/3'] = df['Scoring 1/2/3'].fillna(1).astype(int)
            for _, row in df.iterrows():
                donnees_chargees.append({
                    "nom": str(row.get('Tâches', 'Nouvelle quête')),
                    "duree": str(row.get('Durée', '15min')),
                    "points": int(row['Scoring 1/2/3']),
                    "recurrence": bool(row.get('Récurrence', False)),
                    "statut": int(row['Statut'])
                })
        except Exception:
            pass

    if not donnees_chargees:
        try:
            if page.client_storage.contains_key("todoquest_tasks"):
                donnees_chargees = page.client_storage.get("todoquest_tasks") or []
        except Exception:
            pass

    for d in donnees_chargees:
        liste_quetes.controls.append(creer_carte(d["nom"], d["duree"], d["points"], d["recurrence"], d["statut"]))
            
    points_initiaux = sum([c.data["points"] for c in liste_quetes.controls if c.data is not None and c.data.get("statut") == 2])
    # On initialise silencieusement pour ne pas déclencher le pop-up au démarrage
    xp_totale = points_initiaux
    texte_niveau.value = f"🌟 Niveau {(xp_totale // palier_niveau) + 1} | {xp_totale} XP"
    barre_xp.value = (xp_totale % palier_niveau) / palier_niveau

    # ➕ Ajout
    champ_ajout_nom = ft.TextField(label="Que vas-tu accomplir ?")
    champ_ajout_duree = ft.TextField(label="Durée estimée (ex: 30min)")
    champ_ajout_xp = ft.Dropdown(options=[ft.dropdown.Option("1"), ft.dropdown.Option("2"), ft.dropdown.Option("3")], value="1")
    switch_ajout_rec = ft.Switch(label="Habitude récurrente", value=False)

    dialogue_ajout = ft.AlertDialog(
        title=ft.Text("✨ Nouvelle Quête"),
        content=ft.Column([champ_ajout_nom, champ_ajout_duree, champ_ajout_xp, switch_ajout_rec], tight=True),
        actions=[
            ft.TextButton("Annuler", on_click=lambda e: setattr(dialogue_ajout, 'open', False) or page.update()),
            ft.ElevatedButton("Ajouter", on_click=lambda e: [liste_quetes.controls.insert(0, creer_carte(champ_ajout_nom.value, champ_ajout_duree.value or "Action rapide", int(champ_ajout_xp.value), switch_ajout_rec.value)), sauvegarder_donnees(), setattr(dialogue_ajout, 'open', False), page.update()] if champ_ajout_nom.value else None, bgcolor="#4CAF50", color="white")
        ]
    )

    page.floating_action_button = ft.FloatingActionButton(
        content=ft.Text("+", size=30, color="white"),
        bgcolor="#FF6B6B",
        on_click=lambda e: (page.overlay.append(dialogue_ajout) if dialogue_ajout not in page.overlay else None) or setattr(dialogue_ajout, 'open', True) or page.update()
    )

    page.add(
        ft.Container(height=10),
        ft.Column([badge_niveau, barre_xp, bouton_repos], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
        ft.Divider(color="#E0E0E0"),
        liste_quetes
    )

if __name__ == "__main__":
    ft.app(target=main)