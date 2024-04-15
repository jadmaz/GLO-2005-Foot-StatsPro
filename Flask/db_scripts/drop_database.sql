DROP TRIGGER IF EXISTS IncrementerTropheeAfterInsert;
DROP TRIGGER IF EXISTS AssignGoalsToPlayers;
DROP TRIGGER IF EXISTS IncrementerNombreMatchs;

DROP PROCEDURE IF EXISTS AssignGoalsAndAssistsToTeam;
DROP PROCEDURE IF EXISTS GetWinPercentage;
DROP PROCEDURE IF EXISTS GetPlayerStatistics;


drop database FootProStats_bd;
