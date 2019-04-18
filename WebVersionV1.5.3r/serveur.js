var app = require('express')();
var express = require('express');
var serveur = require('http').Server(app);
var io = require('socket.io')(serveur);
var path = require('path');
var fs = require('fs');
var verification = require('./modules/verification.js');
var child_process = require('child_process');

app.use(express.static(path.join(__dirname, 'views')));

app.get('/', function (req, res) {
    res.render("index.ejs");
});

app.get('/Sorties/:id/', function (req, res) {
    res.download(__dirname + "/Sorties/" + req.params.id + "/archive.zip", "archive.zip");
});


// Gestion des sockets
io.sockets.on('connection', function (socket) {
    var parametres = [];
    var ext = "";
    var extSet = false;
    var bufTab = [];
    var buf = null;
    parametres['valide'] = false;

    // Connexion
    console.log("Connexion établie : " + socket.id);

    var pingPong = setInterval(function () {
        socket.emit('ping_serv', { balle: 1 });
    }, 5000);


    socket.on('pong_client', function (data) {
        console.log("Le serveur reçoit la balle du client");
    });

    socket.on('ant_param', function (infos) {
        deleteFile(socket.id);
        var message = verification.options(infos);
        if (message[0]) {
            parametres['valide'] = true;
            parametres['type'] = infos['type'];
            parametres['debut'] = infos['debut'];
            parametres['taille'] = infos['taille'];
            parametres['pas'] = infos['pas'];

            if (parametres['type'] == "ta_as") {
                parametres['type'] = "as";
            }
            else if (parametres['type'] == "ta_af") {
                parametres['type'] = "acf";
            }
            else if (parametres['type'] == "ta_ar") {
                parametres['type'] = "acr";
            }
            console.log(parametres['type']);
        }
        extSet = false;
        ext = "";
        bufTab = [];
        buf = null;
        socket.emit('validate_data', message);

    });

    socket.on('televersement_fichier', function (data) {
        if ((data['octet'].byteLength != 0) && parametres['valide']) {
            // Si l'extension du fichier est vide
            // Cela signifie que c'est la première fois qu'on reçoit l'ordre de transfert
            if (!extSet) {
                console.log("init");
                deleteFile(socket.id);
                ext = verification.getExtension(data['file']);
                if ((ext != ".zip") && (parametres['type'] == "acr")) {
                    ext = "";
                }
                console.log("CREATION DE " + "Upload/" + socket.id)
                fs.mkdirSync("Upload/" + socket.id);
                extSet = true;
            }
            // Si l'extension du fichier a été initialisée
            if (ext.length != 0) {
                bufTab.push(data['octet']);
                if (bufTab.length >= 5242880) {
                    buf = Buffer.concat(bufTab);
                    i++;
                    console.log("Acces disque 1");
                    fs.appendFile("Upload/" + socket.id + "/" + data['file'], buf, function (err) {
                        if (err) {
                            console.log("erreur");
                        }
                    });
                    bufTab = [];
                    buf = null;
                }
                socket.emit('televersement_fichier_serv', { is_ok: true });
            }
            else {// Extension du fichier initialisé, mais le fichier n'a pas d'extension
                socket.emit('televersement_fichier_serv', { is_ok: false });
            }
        }
        else if (bufTab.length > 0) {
            buf = Buffer.concat(bufTab);
            fs.appendFile("Upload/" + socket.id + "/" + data['file'], buf, function (err) {
                if (err) {
                    console.log("erreur");
                } else {
                    lancementAnalyse(parametres, socket.id, data['file'], socket);
                }
            });
            buf = null;
            bufTab = [];
        }
    });


    // Déconnexion
    socket.on('disconnect', function () {
        clearInterval(pingPong);
        socket.removeAllListeners();
        deleteFile(socket.id);
        buff = null;
        console.log('Déconnexion : ' + socket.id)
        socket = null;
    });
});


// Supprime le fichier s'il existe
function deleteFile(id) {
    try {
        child_process.execSync("rm -rf Upload/" + id);
        child_process.execSync("rm -rf Sorties/" + id);
        console.log("SUPPRIME")
    }
    catch (err) {
        console.log("Probleme de suppression");
    }
}


function lancementAnalyse(parametres, id, filename, socket) {
    // Nom du répertoire de sortie
    var nom_rep_sortie = filename.replace('.', '_');
    var rout = "Sorties/" + id + "/";
    var cmd = "";
    var cmd_r = "";
    var no_error = true;

    var commande = ["prog/fftToTriangleV6_6.py",
        parametres['type'],
        "deb=" + parametres['debut'],
        "t=" + parametres['taille']]


    if (parametres['type'] == "acr") {
        // Le pas
        commande.push("pas=" + parametres['pas']);
        // Permet de vérifier s'il existe au moins une analyse valide
        var is_analyse_valide = false;
        // Le répertoire à analyser
        var r = "Upload/" + id + "/"
        commande.push("r=" + r);
        // Le répertoire de sortie
        rout += "archive"
        commande.push("rout=" + rout);
        // Décompression du fichier
        cmd = "cd Upload/" + id + " && " + "unzip " + filename;
        console.log(cmd);


        cmd = child_process.exec(cmd);

        cmd.stderr.on('data', function (data) {
            console.log(data.toString());
        });

        cmd.on('close', function () {
            // Message pour indiquer que le programme commence
            socket.emit('lancement_analyse', "Lancement de l'analyse");

            // L'exécution du programme
            cmd_r = child_process.spawn('python3', commande);

            cmd_r.stdout.on('data', function (data) {
                is_analyse_valide = true;
                socket.emit('console_message', data.toString());
            });

            cmd_r.stderr.on('data', function (data) {
                socket.emit('console_message', data.toString());
            })

            cmd_r.on('close', function (code) {
                try {
                    socket.emit('preparation_archive', "Préparation de l'archive zip");
                    if ((code != null)) {
                        // La compression de l'archive
                        cmd = "cd Sorties/" + id + " && " + "zip -r archive.zip archive"
                        cmd = child_process.spawn(cmd, {
                            shell: true
                        });
    
                        cmd.stdout.on('data', function (data) {
                            console.log(data.toString());
                        });
    
                        cmd.stderr.on('data', function (data) {
                            console.log(data);
                        });
    
                        cmd.on('close', function (code) {
                            // Envoie de l'URL de téléchargement
                            if (code != null) {
                                archiveLinkdownload(socket, id);
                            }
                        });
                    }
                    else {
                        socket.emit('erreur_analyse', "Erreur rencontrée");
                    }
                }
                catch (err) {
                    console.log(err);
                }
            });
        });
    }
    else {
        // Le fichier source
        var fichier = "Upload/" + id + "/" + filename;
        commande.push("f=" + fichier);
        // La destination de sortie
        var nom_rep_sortie = filename.replace('.', '_');

        if (parametres['type'] == 'as') {
            rout += nom_rep_sortie;
        }
        else {
            // Le pas
            commande.push("pas=" + parametres['pas']);
        }

        commande.push("rout=" + rout);

        // Message pour indiquer que le programme commence
        socket.emit('lancement_analyse', "Lancement de l'analyse");

        // L'éxécution du programme
        cmd = child_process.spawn('python3', commande);
        // Récupération des messages 'normaux'
        cmd.stdout.on('data', function (data) {
            socket.emit('console_message', data.toString());
        });
        // Récupération des erreurs
        cmd.stderr.on('data', function (data) {
            no_error = false;
            socket.emit('console_message', data.toString());
        });

        cmd.on('close', function (code) {
            try {
                socket.emit('preparation_archive', "Préparation de l'archive zip");
                if ((code != null) && no_error) {
                    // Création de l'archive zip
                    cmd = "cd Sorties/" + id + "/" + " && " + "zip -r " + nom_rep_sortie + ".zip" + " " + nom_rep_sortie;
                    cmd = cmd + " && " + " mv " + nom_rep_sortie + ".zip" + " " + "archive.zip"

                    cmd = child_process.spawn(cmd, {
                        shell: true
                    });

                    cmd.stdout.on('data', function (data) {
                        console.log(data.toString());
                    });

                    cmd.stderr.on('data', function (data) {
                        console.log(data);
                    });

                    cmd.on('close', function (code) {
                        // Envoie de l'URL de téléchargement
                        if (code != null) {
                            archiveLinkdownload(socket, id);
                        }
                    });
                }
                else {
                    socket.emit('erreur_analyse', "Erreur rencontrée");
                }
            }
            catch (err) {
                console.log(err);
            }
        });
    }
}

// Crée le lien de téléchargement
// L'envoie au client
function archiveLinkdownload(socket, id) {
    var fichier = "./Sorties/" + id;

    socket.emit('lien_telechargement', fichier);
}

// Capture du signal de timeout du serveur
// Le signal est capturé pour ne pas quitter la connxion (sinon risquer pour les transferts long)
serveur.on('timeout', function () {
    ;
});



serveur.listen(8000);
// Le temps 'timeout' par défaut du serveur est mis à 2 secondes (milliseconde)
serveur.timeout = 2 * 60 * 1000;



