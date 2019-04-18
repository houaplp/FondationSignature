# fftToTriangle
version 1.5.3 (LP)

## Programme python
### version 6.6
modifications des noms de fichiers avec dates qu'on puisse trier
avant : CloseToTheEdge_deb498000_t2500.aif_sr44100_deb0_t2480.txt
maintenant : CloseToTheEdge.wav_sr44100_deb00_07_50_t02_50_pas02_50.txt



## Programme python
### versions 6.4
#### Problème
Correction du programme python qui comportait un problème dans la ifft. La librairie librosa effectue un ifft par défaut qui est de taille différente par rapport au fichier original.

#### Correction
Préciser le champ length dans librosa.istft de la taille de la longueur d'onde original :
```python
librosa.istft(fft, length=len(waveform))
# fft est le tableau comportant la fft qui va être inversé
# waveform est la forme d'onde originale
```

Cette correction a apporté d'autre modification : dans la fonction de decomposition de moyenne 'decomposition_moyenne`, la convertion en np.array a du être enlevé.

Le programme python v6.4 a finalement été enlevé de l'application, passage à la version 6.5

### version 6.5
Reprend les travaux effectués effectué en 6.4. Changement de la fonction de conversion du temps en points, reprise de la même fonction qu'on retrouve dans les version antérieur à la 6.4.

#### Fonctionnalité
Cette version se distingue surtout par l'ajout d'une nouvelle fonctionnalité qui est l'obtention du graphe des températures générés par la matrice triangulaire.
