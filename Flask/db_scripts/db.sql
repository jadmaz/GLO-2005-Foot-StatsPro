CREATE DATABASE IF NOT EXISTS FootProStats_bd;
USE FootProStats_bd;


CREATE TABLE IF NOT EXISTS Equipe (
    equipe_id INT PRIMARY KEY,
    nom VARCHAR(255),
    pays VARCHAR(100),
    entraineur_principal VARCHAR(255),
    stade_domicile VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Joueur (
joueur_id INT AUTO_INCREMENT PRIMARY KEY,
nom VARCHAR(255),
age INT,
position VARCHAR(50),
equipe_id INT,
FOREIGN KEY (equipe_id) REFERENCES Equipe(equipe_id)
);

CREATE TABLE IF NOT EXISTS Partie (
    match_id INT AUTO_INCREMENT,
    date DATE,
    lieu VARCHAR(255),
    resultat VARCHAR(50),
    equipe_locale_id INT,
    equipe_visiteur_id INT,
    tournoi_id INT,
    PRIMARY KEY (match_id),
    FOREIGN KEY (equipe_locale_id) REFERENCES Equipe(equipe_id),
    FOREIGN KEY (equipe_visiteur_id) REFERENCES Equipe(equipe_id),
    FOREIGN KEY (tournoi_id) REFERENCES tournoi(tournoi_id)
);
CREATE TABLE IF NOT EXISTS Classement (
    classement_id INT AUTO_INCREMENT PRIMARY KEY,
    saison VARCHAR(50),
    equipe_id INT,
    position INT,
    nombre_de_victoires INT,
    nombre_de_defaites INT,
    FOREIGN KEY (equipe_id) REFERENCES Equipe(equipe_id)
);

CREATE TABLE IF NOT EXISTS Statistiques (
    statistique_id INT AUTO_INCREMENT PRIMARY KEY,
    joueur_id INT,
    match_id INT,
    buts_marques INT,
    passes_decisives INT,
    tirs INT,
    fautes INT,
    FOREIGN KEY (joueur_id) REFERENCES Joueur(joueur_id),
    FOREIGN KEY (match_id) REFERENCES Partie(match_id)
);

CREATE TABLE IF NOT EXISTS tournoi (
    tournoi_id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    lieu VARCHAR(100),
    nb_equipe integer,
    date_de_debut DATE,
    date_de_fin DATE
);

INSERT INTO tournoi (nom, lieu, nb_equipe, date_de_debut, date_de_fin)
VALUES
    ('Tournoi A', 'Paris', 10, '2024-05-15', '2024-05-20'),
    ('Tournoi B', 'Lyon', 8, '2024-06-01', '2024-06-05'),
    ('Tournoi C', 'Marseille', 12, '2024-07-10', '2024-07-15');

INSERT INTO Equipe (equipe_id, nom, pays, entraineur_principal, stade_domicile) VALUES
(1, 'FC Barcelona', 'Spain', 'Xavi Hernandez', 'Camp Nou'),
(2, 'Real Madrid', 'Spain', 'Carlo Ancelotti', 'Santiago Bernabeu'),
(3, 'Paris Saint-Germain', 'France', 'Mauricio Pochettino', 'Parc des Princes'),
(4, 'Manchester City', 'England', 'Pep Guardiola', 'Etihad Stadium'),
(5, 'Liverpool FC', 'England', 'Jurgen Klopp', 'Anfield'),
(6, 'AC Milan', 'Italy', 'Stefano Pioli', 'San Siro'),
(7, 'Borussia Dortmund', 'Germany', 'Edin Terzic', 'Signal Iduna Park'),
(8, 'Ajax Amsterdam', 'Netherlands', 'Erik ten Hag', 'Johan Cruyff Arena');



INSERT INTO Joueur (nom, age, position, equipe_id) VALUES
('Antoine Griezmann', 31, 'Forward', 1),
('Marc-André ter Stegen', 29, 'Goalkeeper', 1),
('Gerard Piqué', 35, 'Defender', 1),
('Sergio Busquets', 33, 'Midfielder', 1),
('Ansu Fati', 19, 'Forward', 1);

-- Players for Real Madrid
INSERT INTO Joueur (nom, age, position, equipe_id) VALUES
('Karim Benzema', 34, 'Forward', 2),
('Thibaut Courtois', 29, 'Goalkeeper', 2),
('Eden Hazard', 31, 'Forward', 2),
('Luka Modric', 36, 'Midfielder', 2),
('Eder Militao', 24, 'Defender', 2);

-- Players for Paris Saint-Germain
INSERT INTO Joueur (nom, age, position, equipe_id) VALUES
('Marco Verratti', 29, 'Midfielder', 3),
('Marquinhos', 27, 'Defender', 3),
('Keylor Navas', 35, 'Goalkeeper', 3),
('Ángel Di María', 34, 'Forward', 3),
('Presnel Kimpembe', 26, 'Defender', 3);

-- Players for Manchester City
INSERT INTO Joueur (nom, age, position, equipe_id) VALUES
('Raheem Sterling', 27, 'Forward', 4),
('Ederson', 28, 'Goalkeeper', 4),
('Ruben Dias', 24, 'Defender', 4),
('Rodri', 25, 'Midfielder', 4),
('Jack Grealish', 26, 'Midfielder', 4);

-- Players for Liverpool FC
INSERT INTO Joueur (nom, age, position, equipe_id) VALUES
('Mohamed Salah', 29, 'Forward', 5),
('Alisson Becker', 29, 'Goalkeeper', 5),
('Fabinho', 28, 'Midfielder', 5),
('Sadio Mané', 30, 'Forward', 5),
('Andrew Robertson', 27, 'Defender', 5);






INSERT INTO Partie (date, lieu, resultat, equipe_locale_id, equipe_visiteur_id) VALUES
('2024-05-21', 'Camp Nou', '2-1', 1, 2),
('2024-05-22', 'Santiago Bernabeu', '0-0', 2, 3),
('2024-05-23', 'Parc des Princes', '3-2', 3, 4),
('2024-05-24', 'Etihad Stadium', '1-4', 4, 5);
INSERT INTO Classement (saison, equipe_id, position, nombre_de_victoires, nombre_de_defaites) VALUES
('2023-2024', 1, 1, 30, 4),
('2023-2024', 2, 2, 28, 6),
('2023-2024', 3, 3, 25, 9),
('2023-2024', 4, 4, 23, 11),
('2023-2024', 5, 5, 20, 14);


DROP TABLE Statistiques;
DROP TABLE Joueur;
DROP TABLE Partie;
DROP TABLE Classement;
DROP TABLE Equipe;
DROP TABLE tournoi;

    SELECT
        E.equipe_id, E.nom AS equipe_nom, E.pays, E.entraineur_principal, E.stade_domicile,
        J.joueur_id, J.nom AS joueur_nom, J.age, J.position
    FROM
        Equipe E
    LEFT JOIN
        Joueur J ON E.equipe_id = J.equipe_id
    ORDER BY
        E.equipe_id, J.joueur_id


