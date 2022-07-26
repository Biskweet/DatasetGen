# Rapport

Ce projet a pour objectif de pouvoir générer la représentation en image de la description JSON d'un page en HTML.

## Besoins
* Le package Linux [WKHTMLtoPDF](https://wkhtmltopdf.org/)
* Une distribution Linux compatible
* Un environnement Python récent
* Les packages préinstallés et `numpy` et `Pillow`


## Modèle de données à l'entrée
```json
"data": [
    {
        "name": "name",
        "type": "type",
        "coordinates": { "x": "x-pos", "y": "y-pos", "w": "width", "h": "height" },
        "content": "content"
    },
    {
        "etc": "..."
    }
]
```
Note: aucun élément ne doit se superposer avec un autre.


## Attendues à la sortie
Image (n'importe quel format).

## Types d'éléments
A été sélectionné la liste d'éléments suivante, dans l'ordre :
- `button`
- `checkbox`
- `header`
- `image`
- `label`
- `link`
- `paragraph`
- `radio`
- `select`
- `textarea`
- `textbox`

Les types suivants ont été considérés puis retirés :
- `carousel` : trop complexe à produire pour une utilité incertaine ;
- `pagination` idem ;
- `table` : complexe à produire, informations manquantes (lignes, colonnes).

## Méthode
Les données contenues dans les fichiers JSON seront lues et incorporées dans une page HTML/CSS, puis cette page HTML sera convertie en image avec le package `wkhtmltoimage`.

## Difficultés
- Impossible de définir la taille d'une image au pixel près sans conserver son ration hauteur/largeur.
	- Solution : utiliser un SVG, définir sa taille à 1px et utiliser la propriété CSS `transform: scale(w, h);` pour étirer l'image à volonté.

Malheureusement, les images ne sont toujours pas parfaitement bien encadrées (légèrement décalées vers le bas). Ce ne sera probablement pas un problème très grave lors de l'entraînement du modèle.

- Impossible de définir la taille d'un texte au pixel près, même avec la propriété CSS `font-size`.
	- Solution temporaire : Utilisation d'une police mono, définition de tous les types textuels avec un contenu préenregistré pour pouvoir prédire la taille de l'élément et l'encadrer convenablement.
- Impossible de déterminer quelle taille de police utiliser dans un paragraphe en l'absence de retours à la ligne fournis.
