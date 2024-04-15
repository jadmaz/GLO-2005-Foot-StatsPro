CREATE DATABASE IF NOT EXISTS FootProStats_bd;
USE FootProStats_bd;


CREATE TABLE IF NOT EXISTS Equipe
(
    equipe_id            INT PRIMARY KEY,
    nom                  VARCHAR(255),
    pays                 VARCHAR(100),
    entraineur_principal VARCHAR(255),
    stade_domicile       VARCHAR(255),
    trophee              INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Joueur (
joueur_id INT AUTO_INCREMENT PRIMARY KEY,
nom VARCHAR(255),
age INT,
position VARCHAR(50),
equipe_id INT,
FOREIGN KEY (equipe_id) REFERENCES Equipe(equipe_id)
);


CREATE TABLE IF NOT EXISTS tournoi (
    tournoi_id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    lieu VARCHAR(100),
    nb_equipe INTEGER,
    date_de_debut DATE,
    date_de_fin DATE,
    gagnant INT,
    FOREIGN KEY (gagnant) REFERENCES Equipe(equipe_id)
);


CREATE TABLE IF NOT EXISTS Partie (
    match_id INT AUTO_INCREMENT,
    date DATE,
    lieu VARCHAR(255),
    resultat VARCHAR(50),
    equipe_locale_id INT,
    equipe_visiteur_id INT,
    tournoi_id INT,
    winner VARCHAR(50),
    PRIMARY KEY (match_id),
    FOREIGN KEY (equipe_locale_id) REFERENCES Equipe(equipe_id),
    FOREIGN KEY (equipe_visiteur_id) REFERENCES Equipe(equipe_id),
    FOREIGN KEY (tournoi_id) REFERENCES tournoi(tournoi_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS Classement (
    saison VARCHAR(50),
    equipe_id INT,
    nombre_de_victoires INT,
    nombre_de_defaites INT,
    FOREIGN KEY (equipe_id) REFERENCES Equipe(equipe_id)
);

CREATE TABLE IF NOT EXISTS Statistiques (
    statistique_id INT AUTO_INCREMENT PRIMARY KEY,
    joueur_id INT,
    buts_marques INT DEFAULT 0,
    passes_decisives INT DEFAULT 0,
    nb_matchs INT DEFAULT 0,
    FOREIGN KEY (joueur_id) REFERENCES Joueur(joueur_id)
);

SELECT * FROM Partie;






