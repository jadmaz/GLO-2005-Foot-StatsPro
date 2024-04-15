INSERT INTO Equipe (equipe_id, nom, pays, entraineur_principal, stade_domicile) VALUES
(1, 'FC Barcelona', 'Spain', 'Xavi Hernandez', 'Camp Nou'),
(2, 'Real Madrid', 'Spain', 'Carlo Ancelotti', 'Santiago Bernabeu'),
(3, 'Paris Saint-Germain', 'France', 'Mauricio Pochettino', 'Parc des Princes'),
(4, 'Manchester City', 'England', 'Pep Guardiola', 'Etihad Stadium'),
(5, 'Liverpool FC', 'England', 'Jurgen Klopp', 'Anfield'),
(6, 'AC Milan', 'Italy', 'Stefano Pioli', 'San Siro'),
(7, 'Borussia Dortmund', 'Germany', 'Edin Terzic', 'Signal Iduna Park'),
(8, 'Ajax Amsterdam', 'Netherlands', 'Erik ten Hag', 'Johan Cruyff Arena');

INSERT INTO Equipe (equipe_id, nom, pays, entraineur_principal, stade_domicile) VALUES
(9,'Atletico Madrid', 'Spain', 'Diego Simeone', 'Wanda Metropolitano'),
(10,'Chelsea FC', 'England', 'Thomas Tuchel', 'Stamford Bridge'),
(11, 'Bayern Munich', 'Germany', 'Julian Nagelsmann', 'Allianz Arena'),
(12, 'Inter Milan', 'Italy', 'Simone Inzaghi', 'San Siro'),
(13, 'Juventus', 'Italy', 'Massimiliano Allegri', 'Juventus Stadium'),
(14, 'Arsenal FC', 'England', 'Mikel Arteta', 'Emirates Stadium'),
(15, 'Tottenham Hotspur', 'England', 'Antonio Conte', 'Tottenham Hotspur Stadium'),
(16, 'Borussia Mönchengladbach', 'Germany', 'Adi Hütter', 'Borussia-Park');

INSERT INTO Joueur (nom, age, position, equipe_id) VALUES
('Jan Oblak', 29, 'Goalkeeper', 9),
('Luis Suarez', 35, 'Forward', 9),
('Joao Felix', 22, 'Forward', 9),
('Koke', 30, 'Midfielder', 9),
('Yannick Carrasco', 28, 'Midfielder', 9),
('Jose Gimenez', 27, 'Defender', 9),
('Edouard Mendy', 30, 'Goalkeeper', 10),
('Romelu Lukaku', 29, 'Forward', 10),
('Golo Kante', 31, 'Midfielder', 10),
('Mason Mount', 23, 'Midfielder', 10),
('Thiago Silva', 37, 'Defender', 10),
('Reece James', 22, 'Defender', 10),
('Manuel Neuer', 36, 'Goalkeeper', 11),
('Robert Lewandowski', 33, 'Forward', 11),
('Joshua Kimmich', 27, 'Midfielder', 11),
('Thomas Muller', 32, 'Midfielder', 11),
('Alphonso Davies', 21, 'Defender', 11),
('Lucas Hernandez', 26, 'Defender', 11),
('Samir Handanovic', 37, 'Goalkeeper', 12),
('Lautaro Martinez', 24, 'Forward', 12),
('Nicolo Barella', 25, 'Midfielder', 12),
('Marcelo Brozovic', 29, 'Midfielder', 12),
('Milan Skriniar', 27, 'Defender', 12),
('Alessandro Bastoni', 23, 'Defender', 12),
('Wojciech Szczesny', 32, 'Goalkeeper', 13),
('Paulo Dybala', 28, 'Forward', 13),
('Weston McKennie', 23, 'Midfielder', 13),
('Matthijs de Ligt', 22, 'Defender', 13),
('Leonardo Bonucci', 35, 'Defender', 13),
('Federico Chiesa', 24, 'Forward', 13),
('Aaron Ramsdale', 24, 'Goalkeeper', 14),
('Bukayo Saka', 20, 'Forward', 14),
('Martin Odegaard', 23, 'Midfielder', 14),
('Gabriel Magalhaes', 24, 'Defender', 14),
('Ben White', 24, 'Defender', 14),
('Kieran Tierney', 24, 'Defender', 14),
('Hugo Lloris', 35, 'Goalkeeper', 15),
('Harry Kane', 28, 'Forward', 15),
('Son Heung-min', 29, 'Forward', 15),
('Dele Alli', 26, 'Midfielder', 15),
('Eric Dier', 28, 'Defender', 15),
('Sergio Reguilon', 25, 'Defender', 15),
('Yann Sommer', 33, 'Goalkeeper', 16),
('Marcus Thuram', 24, 'Forward', 16),
('Florian Neuhaus', 25, 'Midfielder', 16),
('Alassane Plea', 29, 'Forward', 16),
('Matthias Ginter', 28, 'Defender', 16),
('Nico Elvedi', 25, 'Defender', 16);

INSERT INTO Joueur (nom, age, position, equipe_id) VALUES
('Unai Simon', 25, 'Goalkeeper', 9),
('Felipe', 32, 'Defender', 9),
('Renan Lodi', 24, 'Defender', 9),
('Saul Niguez', 27, 'Midfielder', 9),
('Rodrigo De Paul', 27, 'Midfielder', 9),

('Timo Werner', 26, 'Forward', 10),
('Christian Pulisic', 23, 'Forward', 10),
('Hakim Ziyech', 29, 'Midfielder', 10),
('Jorginho', 30, 'Midfielder', 10),
('Ben Chilwell', 25, 'Defender', 10),

('Serge Gnabry', 26, 'Forward', 11),
('Leroy Sane', 26, 'Forward', 11),
('Kingsley Coman', 25, 'Forward', 11),
('Leon Goretzka', 27, 'Midfielder', 11),
('Niklas Sule', 26, 'Defender', 11),

('Alexis Sanchez', 33, 'Forward', 12),
('Arturo Vidal', 34, 'Midfielder', 12),
('Stefan de Vrij', 30, 'Defender', 12),
('Ivan Perisic', 33, 'Midfielder', 12),
('Denzel Dumfries', 26, 'Defender', 12),

('Adrien Rabiot', 27, 'Midfielder', 13),
('Moise Kean', 22, 'Forward', 13),
('Alex Sandro', 31, 'Defender', 13),
('Juan Cuadrado', 33, 'Defender', 13),
('Danilo', 30, 'Defender', 13),

('Granit Xhaka', 29, 'Midfielder', 14),
('Pierre-Emerick Aubameyang', 32, 'Forward', 14);




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

-- Inserts pour l'équipe avec l'ID 6
INSERT INTO Joueur (nom, age, position, equipe_id) VALUES
('Lucas Martinez', 23, 'Defender', 6),
('Gabriel Silva', 21, 'Midfielder', 6),
('Marco Verratti', 28, 'Midfielder', 6),
('Eduardo Lopez', 24, 'Forward', 6),
('Sergio Ramos', 34, 'Defender', 6),
('Antoine Dupont', 26, 'Goalkeeper', 6),
('Julian Draxler', 27, 'Midfielder', 6),
('Carlos Fierro', 22, 'Forward', 6);

-- Inserts pour l'équipe avec l'ID 7
INSERT INTO Joueur (nom, age, position, equipe_id) VALUES
('Nico Schulz', 27, 'Defender', 7),
('Thiago Silva', 33, 'Defender', 7),
('David Neres', 23, 'Forward', 7),
('Arthur Melo', 24, 'Midfielder', 7),
('Bernardo Silva', 25, 'Midfielder', 7),
('Keylor Navas', 32, 'Goalkeeper', 7),
('Felipe Caicedo', 31, 'Forward', 7),
('Mason Mount', 22, 'Midfielder', 7);

-- Inserts pour l'équipe avec l'ID 8
INSERT INTO Joueur (nom, age, position, equipe_id) VALUES
('Ivan Rakitic', 32, 'Midfielder', 8),
('Jordi Alba', 31, 'Defender', 8),
('Gianluigi Donnarumma', 22, 'Goalkeeper', 8),
('Frenkie de Jong', 23, 'Midfielder', 8),
('Ansu Fati', 18, 'Forward', 8),
('Luis Suarez', 34, 'Forward', 8),
('Gerard Pique', 33, 'Defender', 8),
('Sergio Busquets', 32, 'Midfielder', 8);


Insert Into Classement(saison, nombre_de_victoires, nombre_de_defaites, equipe_id)
VALUES
('2023/2024', 0, 0, 1),
('2023/2024', 0, 0, 2),
('2023/2024', 0, 0, 3),
('2023/2024', 0, 0, 4),
('2023/2024', 0, 0, 5),
('2023/2024', 0, 0, 6),
('2023/2024', 0, 0, 7),
('2023/2024', 0, 0, 8),
('2023/2024', 0, 0, 9),
('2023/2024', 0, 0, 10),
('2023/2024', 0, 0, 11),
('2023/2024', 0, 0, 12),
('2023/2024', 0, 0, 13),
('2023/2024', 0, 0, 14),
('2023/2024', 0, 0, 15),
('2023/2024', 0, 0, 16);


INSERT INTO Statistiques (joueur_id, buts_marques, passes_decisives)
SELECT J.joueur_id, 0, 0
FROM Equipe E
JOIN Joueur J ON E.equipe_id = J.equipe_id;