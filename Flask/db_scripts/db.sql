CREATE DATABASE IF NOT EXISTS FootProStats_bd;
USE FootProStats_bd;

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

SELECT * FROM tournoi;
drop table tournoi