DELIMITER //

CREATE PROCEDURE GetWinPercentage(team1_id INT, team2_id INT)
BEGIN
    DECLARE total_matches INT DEFAULT 0;
    DECLARE team1_wins INT DEFAULT 0;
    DECLARE team2_wins INT DEFAULT 0;
    DECLARE team1_win_percentage DECIMAL(5,2);
    DECLARE team2_win_percentage DECIMAL(5,2);

    -- Create a temporary table to hold the results
    CREATE TEMPORARY TABLE WinPercentage (
        Team_ID INT,
        Team_Name VARCHAR(255),
        Win_Percentage DECIMAL(5,2)
    );

    -- Calcul du nombre total de matches entre les deux équipes
    SELECT COUNT(*) INTO total_matches
    FROM Partie
    WHERE (equipe_locale_id = team1_id AND equipe_visiteur_id = team2_id)
       OR (equipe_locale_id = team2_id AND equipe_visiteur_id = team1_id);

    -- Calcul du nombre de victoires de team1
    SELECT COUNT(*) INTO team1_wins
    FROM Partie
    WHERE ((equipe_locale_id = team1_id AND equipe_visiteur_id = team2_id AND winner = 'home')
        OR (equipe_locale_id = team2_id AND equipe_visiteur_id = team1_id AND winner = 'away'));

    -- Calcul du nombre de victoires de team2
    SELECT COUNT(*) INTO team2_wins
    FROM Partie
    WHERE ((equipe_locale_id = team2_id AND equipe_visiteur_id = team1_id AND winner = 'home')
        OR (equipe_locale_id = team1_id AND equipe_visiteur_id = team2_id AND winner = 'away'));

    -- Calcul du pourcentage de victoire de team1
    IF total_matches > 0 THEN
        SET team1_win_percentage = (team1_wins / total_matches) * 100;
        SET team2_win_percentage = (team2_wins / total_matches) * 100;
    ELSE
        SET team1_win_percentage = 0;
        SET team2_win_percentage = 0;
    END IF;

    -- Insert the results into the temporary table
    INSERT INTO WinPercentage (Team_ID, Team_Name, Win_Percentage)
    VALUES (team1_id, (SELECT nom FROM Equipe WHERE equipe_id = team1_id), team1_win_percentage),
           (team2_id, (SELECT nom FROM Equipe WHERE equipe_id = team2_id), team2_win_percentage);

    -- Select from the temporary table to display the results
    SELECT * FROM WinPercentage;

    -- Drop the temporary table
    DROP TEMPORARY TABLE WinPercentage;
END//

DELIMITER ;


/*PROCEDURE AFIN DE GÉNÉRER LA BONNE REQUETE SQL POUR LE FILTRE DANS LA SECTION JOUEURS*/
DELIMITER //
CREATE PROCEDURE GetPlayerStatistics(IN position VARCHAR(255), OUT query TEXT)
BEGIN
    IF position = 'None' OR position = 'undefined' THEN
        SET query = 'SELECT
            J.joueur_id,
            J.nom AS nom_joueur,
            J.age,
            J.position,
            J.equipe_id,
            E.nom AS nom_equipe,
            S.buts_marques AS Total_Buts,
            S.passes_decisives AS Total_Passes,
            S.nb_matchs
        FROM
            Joueur J
        JOIN Equipe E ON J.equipe_id = E.equipe_id
        JOIN
            Statistiques S ON J.joueur_id = S.joueur_id
        GROUP BY
            J.joueur_id, J.nom, J.age, J.position, J.equipe_id, E.nom, S.buts_marques, S.passes_decisives, S.nb_matchs
        ORDER BY E.nom;';
    ELSEIF position ='buts' THEN
        SET query = 'SELECT
            J.joueur_id,
            J.nom AS nom_joueur,
            J.age,
            J.position,
            J.equipe_id,
            E.nom AS nom_equipe,
            S.buts_marques AS Total_Buts,
            S.passes_decisives AS Total_Passes,
            S.nb_matchs
        FROM
            Joueur J
        JOIN Equipe E ON J.equipe_id = E.equipe_id
        JOIN
            Statistiques S ON J.joueur_id = S.joueur_id
        GROUP BY
            J.joueur_id, J.nom, J.age, J.position, J.equipe_id, E.nom, S.buts_marques, S.passes_decisives, S.nb_matchs
        ORDER BY S.buts_marques DESC;';
    ELSEIF position = 'passes' THEN
        SET query = '
        SELECT
            J.joueur_id,
            J.nom AS nom_joueur,
            J.age,
            J.position,
            J.equipe_id,
            E.nom AS nom_equipe,
            S.buts_marques AS Total_Buts,
            S.passes_decisives AS Total_Passes,
            S.nb_matchs
        FROM
            Joueur J
        JOIN Equipe E ON J.equipe_id = E.equipe_id
        JOIN
            Statistiques S ON J.joueur_id = S.joueur_id
        GROUP BY
            J.joueur_id, J.nom, J.age, J.position, J.equipe_id, E.nom, S.buts_marques, S.passes_decisives, S.nb_matchs
        ORDER BY S.passes_decisives DESC;';
    ELSE
        SET query = CONCAT('
        SELECT
            J.joueur_id,
            J.nom AS nom_joueur,
            J.age,
            J.position,
            J.equipe_id,
            E.nom AS nom_equipe,
            S.buts_marques AS Total_Buts,
            S.passes_decisives AS Total_Passes,
            S.nb_matchs
        FROM
            Joueur J
        JOIN Equipe E ON J.equipe_id = E.equipe_id
        JOIN
            Statistiques S ON J.joueur_id = S.joueur_id
        WHERE J.position = ''', position, '''
        GROUP BY
            J.joueur_id, J.nom, J.age, J.position, J.equipe_id, E.nom, S.buts_marques, S.passes_decisives, S.nb_matchs
        ORDER BY E.nom;');
    end if;
end //
DELIMITER ;
