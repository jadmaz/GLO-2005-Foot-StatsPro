DELIMITER //

CREATE TRIGGER IncrementerTropheeAfterInsert
AFTER UPDATE ON tournoi
FOR EACH ROW
BEGIN
    IF NEW.gagnant IS NOT NULL THEN
        UPDATE Equipe SET trophee = trophee + 1 WHERE equipe_id = NEW.gagnant;
    END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER AssignGoalsAndAssistsToPlayers
AFTER UPDATE ON Partie
FOR EACH ROW
BEGIN
    DECLARE home_team_goals INT;
    DECLARE visitor_team_goals INT;
    DECLARE home_team_id INT;
    DECLARE visitor_team_id INT;

    SET home_team_goals = SUBSTRING_INDEX(NEW.resultat, '-', 1);
    SET visitor_team_goals = SUBSTRING_INDEX(NEW.resultat, '-', -1);

    SET home_team_id = NEW.equipe_locale_id;
    SET visitor_team_id = NEW.equipe_visiteur_id;

    CALL AssignGoalsAndAssistsToTeam(home_team_id, home_team_goals);

    CALL AssignGoalsAndAssistsToTeam(visitor_team_id, visitor_team_goals);
END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE AssignGoalsAndAssistsToTeam(team_id INT, goals INT)
BEGIN
    DECLARE goal_count INT;
    DECLARE player_count INT;
    DECLARE i INT;
    DECLARE player_id INT;

    SELECT COUNT(*) INTO player_count FROM Joueur WHERE equipe_id = team_id;

    SET goal_count = 0;

    WHILE goal_count < goals DO
        SET player_id = (SELECT joueur_id FROM Joueur WHERE equipe_id = team_id ORDER BY RAND() LIMIT 1);

        UPDATE Statistiques SET buts_marques = buts_marques + 1 WHERE joueur_id = player_id;

        SET player_id = (SELECT joueur_id FROM Joueur WHERE equipe_id = team_id AND joueur_id != player_id ORDER BY RAND() LIMIT 1);
        UPDATE Statistiques SET passes_decisives = passes_decisives + 1 WHERE joueur_id = player_id;

        SET goal_count = goal_count + 1;
    END WHILE;
END//
DELIMITER ;


DELIMITER //
CREATE TRIGGER IncrementerNombreMatchs
AFTER INSERT ON Partie
FOR EACH ROW
BEGIN
    UPDATE Statistiques
    SET nb_matchs = nb_matchs + 1
    WHERE joueur_id IN (SELECT joueur_id FROM Joueur WHERE equipe_id = NEW.equipe_locale_id);


    UPDATE Statistiques
    SET nb_matchs = nb_matchs + 1
    WHERE joueur_id IN (SELECT joueur_id FROM Joueur WHERE equipe_id = NEW.equipe_visiteur_id);
END//
DELIMITER ;





