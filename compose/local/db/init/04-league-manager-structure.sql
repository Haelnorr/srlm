CREATE DATABASE  IF NOT EXISTS `league_manager` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `league_manager`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 192.168.0.6    Database: league_manager
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `arena`
--

DROP TABLE IF EXISTS `arena`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `arena` (
  `value` varchar(32) NOT NULL,
  `label` varchar(32) NOT NULL,
  `info` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`value`),
  UNIQUE KEY `label` (`label`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `award`
--

DROP TABLE IF EXISTS `award`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `award` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `description` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_award_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `discord`
--

DROP TABLE IF EXISTS `discord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discord` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `access_token` varchar(64) DEFAULT NULL,
  `refresh_token` varchar(64) DEFAULT NULL,
  `discord_id` varchar(32) NOT NULL,
  `token_expiration` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_discord_discord_id` (`discord_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `discord_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `division`
--

DROP TABLE IF EXISTS `division`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `division` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `league_id` int NOT NULL,
  `description` varchar(128) DEFAULT NULL,
  `acronym` varchar(5) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `league_id` (`league_id`),
  CONSTRAINT `division_ibfk_1` FOREIGN KEY (`league_id`) REFERENCES `league` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `end_reason`
--

DROP TABLE IF EXISTS `end_reason`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `end_reason` (
  `value` varchar(32) NOT NULL,
  `label` varchar(32) NOT NULL,
  `info` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`value`),
  UNIQUE KEY `label` (`label`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `module` varchar(50) DEFAULT NULL,
  `message` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_event_module` (`module`),
  KEY `ix_event_timestamp` (`timestamp`),
  CONSTRAINT `event_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `external_app`
--

DROP TABLE IF EXISTS `external_app`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `external_app` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `client_id` varchar(128) DEFAULT NULL,
  `client_secret` varchar(128) DEFAULT NULL,
  `grant_type` varchar(128) DEFAULT NULL,
  `access_token` varchar(128) DEFAULT NULL,
  `token_type` varchar(128) DEFAULT NULL,
  `token_expiration` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `final`
--

DROP TABLE IF EXISTS `final`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `final` (
  `id` int NOT NULL AUTO_INCREMENT,
  `season_division_id` int DEFAULT NULL,
  `best_of` int NOT NULL,
  `elimination` tinyint(1) NOT NULL,
  `round` varchar(20) NOT NULL,
  `home_team_id` int DEFAULT NULL,
  `away_team_id` int DEFAULT NULL,
  `completed` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `away_team_id` (`away_team_id`),
  KEY `home_team_id` (`home_team_id`),
  KEY `season_division_id` (`season_division_id`),
  CONSTRAINT `final_ibfk_1` FOREIGN KEY (`away_team_id`) REFERENCES `team` (`id`),
  CONSTRAINT `final_ibfk_2` FOREIGN KEY (`home_team_id`) REFERENCES `team` (`id`),
  CONSTRAINT `final_ibfk_3` FOREIGN KEY (`season_division_id`) REFERENCES `season_division` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `final_results`
--

DROP TABLE IF EXISTS `final_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `final_results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `final_id` int DEFAULT NULL,
  `winner_id` int DEFAULT NULL,
  `loser_id` int DEFAULT NULL,
  `home_team_score` int NOT NULL,
  `away_team_score` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `final_id` (`final_id`),
  KEY `loser_id` (`loser_id`),
  KEY `winner_id` (`winner_id`),
  CONSTRAINT `final_results_ibfk_1` FOREIGN KEY (`final_id`) REFERENCES `final` (`id`),
  CONSTRAINT `final_results_ibfk_2` FOREIGN KEY (`loser_id`) REFERENCES `team` (`id`),
  CONSTRAINT `final_results_ibfk_3` FOREIGN KEY (`winner_id`) REFERENCES `team` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `free_agent`
--

DROP TABLE IF EXISTS `free_agent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `free_agent` (
  `id` int NOT NULL AUTO_INCREMENT,
  `player_id` int DEFAULT NULL,
  `season_division_id` int DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `player_id` (`player_id`),
  KEY `season_division_id` (`season_division_id`),
  CONSTRAINT `free_agent_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `player` (`id`),
  CONSTRAINT `free_agent_ibfk_2` FOREIGN KEY (`season_division_id`) REFERENCES `season_division` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `game_mode`
--

DROP TABLE IF EXISTS `game_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_mode` (
  `value` varchar(32) NOT NULL,
  `label` varchar(32) NOT NULL,
  `info` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`value`),
  UNIQUE KEY `label` (`label`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `league`
--

DROP TABLE IF EXISTS `league`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `league` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `acronym` varchar(5) NOT NULL,
  `server_region_value` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `acronym` (`acronym`),
  UNIQUE KEY `ix_league_name` (`name`),
  KEY `server_region_value` (`server_region_value`),
  CONSTRAINT `league_ibfk_1` FOREIGN KEY (`server_region_value`) REFERENCES `server_region` (`value`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lobby`
--

DROP TABLE IF EXISTS `lobby`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lobby` (
  `id` int NOT NULL AUTO_INCREMENT,
  `match_id` int DEFAULT NULL,
  `lobby_id` varchar(64) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `password` varchar(64) NOT NULL,
  `task_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `match_id` (`match_id`),
  CONSTRAINT `lobby_ibfk_1` FOREIGN KEY (`match_id`) REFERENCES `match` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `match`
--

DROP TABLE IF EXISTS `match`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `match` (
  `id` int NOT NULL AUTO_INCREMENT,
  `season_division_id` int DEFAULT NULL,
  `home_team_id` int DEFAULT NULL,
  `away_team_id` int DEFAULT NULL,
  `round` int DEFAULT NULL,
  `match_week` int DEFAULT NULL,
  `cancelled` varchar(32) DEFAULT NULL,
  `streamer_id` int DEFAULT NULL,
  `final_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `away_team_id` (`away_team_id`),
  KEY `final_id` (`final_id`),
  KEY `home_team_id` (`home_team_id`),
  KEY `season_division_id` (`season_division_id`),
  KEY `streamer_id` (`streamer_id`),
  CONSTRAINT `match_ibfk_1` FOREIGN KEY (`away_team_id`) REFERENCES `team` (`id`),
  CONSTRAINT `match_ibfk_2` FOREIGN KEY (`final_id`) REFERENCES `final` (`id`),
  CONSTRAINT `match_ibfk_3` FOREIGN KEY (`home_team_id`) REFERENCES `team` (`id`),
  CONSTRAINT `match_ibfk_4` FOREIGN KEY (`season_division_id`) REFERENCES `season_division` (`id`),
  CONSTRAINT `match_ibfk_5` FOREIGN KEY (`streamer_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `match_availability`
--

DROP TABLE IF EXISTS `match_availability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `match_availability` (
  `id` int NOT NULL AUTO_INCREMENT,
  `match_id` int DEFAULT NULL,
  `team_id` int DEFAULT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `available` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `match_id` (`match_id`),
  KEY `team_id` (`team_id`),
  CONSTRAINT `match_availability_ibfk_1` FOREIGN KEY (`match_id`) REFERENCES `match` (`id`),
  CONSTRAINT `match_availability_ibfk_2` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `match_data`
--

DROP TABLE IF EXISTS `match_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `match_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lobby_id` int DEFAULT NULL,
  `match_id` varchar(64) NOT NULL,
  `processed` tinyint(1) NOT NULL,
  `region` varchar(16) NOT NULL,
  `gamemode` varchar(16) NOT NULL,
  `created` datetime NOT NULL,
  `arena` varchar(16) NOT NULL,
  `home_score` int NOT NULL,
  `away_score` int NOT NULL,
  `winner` varchar(10) NOT NULL,
  `current_period` int NOT NULL,
  `periods_enabled` tinyint(1) NOT NULL,
  `custom_mercy_rule` varchar(16) NOT NULL,
  `accepted` tinyint(1) NOT NULL,
  `end_reason` varchar(32) NOT NULL,
  `source` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `lobby_id` (`lobby_id`),
  CONSTRAINT `match_data_ibfk_1` FOREIGN KEY (`lobby_id`) REFERENCES `lobby` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `match_result`
--

DROP TABLE IF EXISTS `match_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `match_result` (
  `id` int NOT NULL,
  `winner_id` int DEFAULT NULL,
  `loser_id` int DEFAULT NULL,
  `draw` tinyint(1) DEFAULT NULL,
  `score_winner` int NOT NULL,
  `score_loser` int NOT NULL,
  `overtime` tinyint(1) NOT NULL,
  `forfeit` tinyint(1) NOT NULL,
  `vod` varchar(128) DEFAULT NULL,
  `completed_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `loser_id` (`loser_id`),
  KEY `winner_id` (`winner_id`),
  CONSTRAINT `match_result_ibfk_1` FOREIGN KEY (`id`) REFERENCES `match` (`id`),
  CONSTRAINT `match_result_ibfk_2` FOREIGN KEY (`loser_id`) REFERENCES `team` (`id`),
  CONSTRAINT `match_result_ibfk_3` FOREIGN KEY (`winner_id`) REFERENCES `team` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `match_review`
--

DROP TABLE IF EXISTS `match_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `match_review` (
  `id` int NOT NULL AUTO_INCREMENT,
  `match_id` int DEFAULT NULL,
  `type` varchar(16) NOT NULL,
  `reason` varchar(256) NOT NULL,
  `raised_by` varchar(32) DEFAULT NULL,
  `comments` varchar(256) DEFAULT NULL,
  `resolved` tinyint(1) NOT NULL,
  `resolved_by` int DEFAULT NULL,
  `resolved_on` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `match_id` (`match_id`),
  KEY `resolved_by` (`resolved_by`),
  CONSTRAINT `match_review_ibfk_1` FOREIGN KEY (`match_id`) REFERENCES `match` (`id`),
  CONSTRAINT `match_review_ibfk_2` FOREIGN KEY (`resolved_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `match_schedule`
--

DROP TABLE IF EXISTS `match_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `match_schedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `match_id` int DEFAULT NULL,
  `scheduled_time` datetime DEFAULT NULL,
  `home_team_accepted` tinyint(1) NOT NULL,
  `away_team_accepted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `match_id` (`match_id`),
  CONSTRAINT `match_schedule_ibfk_1` FOREIGN KEY (`match_id`) REFERENCES `match` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `matchtype`
--

DROP TABLE IF EXISTS `matchtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matchtype` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `description` varchar(128) DEFAULT NULL,
  `periods` tinyint(1) NOT NULL,
  `arena` varchar(32) NOT NULL,
  `mercy_rule` int NOT NULL,
  `match_length` int NOT NULL,
  `game_mode` varchar(32) NOT NULL,
  `num_players` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `arena` (`arena`),
  KEY `game_mode` (`game_mode`),
  CONSTRAINT `matchtype_ibfk_1` FOREIGN KEY (`arena`) REFERENCES `arena` (`value`),
  CONSTRAINT `matchtype_ibfk_2` FOREIGN KEY (`game_mode`) REFERENCES `game_mode` (`value`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `key` varchar(32) NOT NULL,
  `description` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_permission_key` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player`
--

DROP TABLE IF EXISTS `player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player` (
  `id` int NOT NULL AUTO_INCREMENT,
  `slap_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `player_name` varchar(64) NOT NULL,
  `rookie` tinyint(1) NOT NULL,
  `first_season_id` int DEFAULT NULL,
  `next_name_change` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slap_id` (`slap_id`),
  KEY `first_season_id` (`first_season_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `player_ibfk_1` FOREIGN KEY (`first_season_id`) REFERENCES `season_division` (`id`),
  CONSTRAINT `player_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=387 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_award`
--

DROP TABLE IF EXISTS `player_award`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_award` (
  `id` int NOT NULL AUTO_INCREMENT,
  `player_id` int DEFAULT NULL,
  `award_id` int DEFAULT NULL,
  `season_division_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `award_id` (`award_id`),
  KEY `player_id` (`player_id`),
  KEY `season_division_id` (`season_division_id`),
  CONSTRAINT `player_award_ibfk_1` FOREIGN KEY (`award_id`) REFERENCES `award` (`id`),
  CONSTRAINT `player_award_ibfk_2` FOREIGN KEY (`player_id`) REFERENCES `player` (`id`),
  CONSTRAINT `player_award_ibfk_3` FOREIGN KEY (`season_division_id`) REFERENCES `season_division` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_match_data`
--

DROP TABLE IF EXISTS `player_match_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_match_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `match_id` int DEFAULT NULL,
  `player_id` int DEFAULT NULL,
  `team_id` int DEFAULT NULL,
  `goals` int DEFAULT NULL,
  `shots` int DEFAULT NULL,
  `assists` int DEFAULT NULL,
  `saves` int DEFAULT NULL,
  `primary_assists` int DEFAULT NULL,
  `secondary_assists` int DEFAULT NULL,
  `passes` int DEFAULT NULL,
  `blocks` int DEFAULT NULL,
  `takeaways` int DEFAULT NULL,
  `turnovers` int DEFAULT NULL,
  `game_winning_goals` int DEFAULT NULL,
  `overtime_goals` int DEFAULT NULL,
  `post_hits` int DEFAULT NULL,
  `faceoffs_won` int DEFAULT NULL,
  `faceoffs_lost` int DEFAULT NULL,
  `score` int DEFAULT NULL,
  `possession_time_sec` int DEFAULT NULL,
  `current_period` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `match_id` (`match_id`),
  KEY `player_id` (`player_id`),
  KEY `team_id` (`team_id`),
  CONSTRAINT `player_match_data_ibfk_1` FOREIGN KEY (`match_id`) REFERENCES `match_data` (`id`),
  CONSTRAINT `player_match_data_ibfk_2` FOREIGN KEY (`player_id`) REFERENCES `player` (`id`),
  CONSTRAINT `player_match_data_ibfk_4` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_team`
--

DROP TABLE IF EXISTS `player_team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_team` (
  `id` int NOT NULL AUTO_INCREMENT,
  `player_id` int DEFAULT NULL,
  `team_id` int DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `player_id` (`player_id`),
  KEY `team_id` (`team_id`),
  CONSTRAINT `player_team_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `player` (`id`),
  CONSTRAINT `player_team_ibfk_2` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=824 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `season`
--

DROP TABLE IF EXISTS `season`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `season` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `league_id` int NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `finals_start` date DEFAULT NULL,
  `finals_end` date DEFAULT NULL,
  `match_type_id` int DEFAULT NULL,
  `acronym` varchar(5) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `league_id` (`league_id`),
  KEY `match_type_id` (`match_type_id`),
  KEY `ix_season_name` (`name`),
  CONSTRAINT `season_ibfk_1` FOREIGN KEY (`league_id`) REFERENCES `league` (`id`),
  CONSTRAINT `season_ibfk_2` FOREIGN KEY (`match_type_id`) REFERENCES `matchtype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `season_division`
--

DROP TABLE IF EXISTS `season_division`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `season_division` (
  `id` int NOT NULL AUTO_INCREMENT,
  `season_id` int DEFAULT NULL,
  `division_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `division_id` (`division_id`),
  KEY `season_id` (`season_id`),
  CONSTRAINT `season_division_ibfk_1` FOREIGN KEY (`division_id`) REFERENCES `division` (`id`),
  CONSTRAINT `season_division_ibfk_2` FOREIGN KEY (`season_id`) REFERENCES `season` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `season_division_team`
--

DROP TABLE IF EXISTS `season_division_team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `season_division_team` (
  `season_division_id` int DEFAULT NULL,
  `team_id` int DEFAULT NULL,
  KEY `season_division_id` (`season_division_id`),
  KEY `team_id` (`team_id`),
  CONSTRAINT `season_division_team_ibfk_1` FOREIGN KEY (`season_division_id`) REFERENCES `season_division` (`id`),
  CONSTRAINT `season_division_team_ibfk_2` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `server_region`
--

DROP TABLE IF EXISTS `server_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `server_region` (
  `value` varchar(32) NOT NULL,
  `label` varchar(32) NOT NULL,
  `info` varchar(64) DEFAULT NULL,
  `utc_offset` varchar(7) DEFAULT NULL,
  PRIMARY KEY (`value`),
  UNIQUE KEY `label` (`label`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `team`
--

DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `team` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `acronym` varchar(5) NOT NULL,
  `color` varchar(7) DEFAULT NULL,
  `logo` varchar(128) DEFAULT NULL,
  `founded_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_team_acronym` (`acronym`),
  UNIQUE KEY `ix_team_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=269 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `team_award`
--

DROP TABLE IF EXISTS `team_award`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `team_award` (
  `id` int NOT NULL AUTO_INCREMENT,
  `team_id` int DEFAULT NULL,
  `award_id` int DEFAULT NULL,
  `season_division_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `award_id` (`award_id`),
  KEY `season_division_id` (`season_division_id`),
  KEY `team_id` (`team_id`),
  CONSTRAINT `team_award_ibfk_1` FOREIGN KEY (`award_id`) REFERENCES `award` (`id`),
  CONSTRAINT `team_award_ibfk_2` FOREIGN KEY (`season_division_id`) REFERENCES `season_division` (`id`),
  CONSTRAINT `team_award_ibfk_3` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `twitch`
--

DROP TABLE IF EXISTS `twitch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `twitch` (
  `id` int NOT NULL AUTO_INCREMENT,
  `twitch_id` varchar(32) NOT NULL,
  `user_id` int NOT NULL,
  `access_token` varchar(64) NOT NULL,
  `refresh_token` varchar(64) NOT NULL,
  `token_expiration` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_twitch_twitch_id` (`twitch_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `twitch_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `reset_pass` tinyint(1) NOT NULL,
  `token` varchar(32) DEFAULT NULL,
  `token_expiration` datetime DEFAULT NULL,
  `steam_id` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_username` (`username`),
  UNIQUE KEY `ix_user_email` (`email`),
  UNIQUE KEY `ix_user_token` (`token`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_permissions`
--

DROP TABLE IF EXISTS `user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `permission_id` int DEFAULT NULL,
  `additional_modifiers` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `permission_id` (`permission_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_permissions_ibfk_1` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`id`),
  CONSTRAINT `user_permissions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-16 12:24:26
