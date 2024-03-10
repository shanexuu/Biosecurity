-- MySQL dump 10.13  Distrib 8.0.34, for macos13 (x86_64)
--
-- Host: 127.0.0.1    Database: biosecurity
-- ------------------------------------------------------
-- Server version	8.1.0

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
-- Table structure for table `mariners`
--

DROP TABLE IF EXISTS `mariners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mariners` (
  `mariners_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `psw` varchar(30) NOT NULL,
  `first_name` varchar(25) NOT NULL,
  `last_name` varchar(25) NOT NULL,
  `address` varchar(100) DEFAULT NULL,
  `email` varchar(45) NOT NULL,
  `phone_number` int DEFAULT NULL,
  `date_joined` datetime NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`mariners_id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mariners`
--

LOCK TABLES `mariners` WRITE;
/*!40000 ALTER TABLE `mariners` DISABLE KEYS */;
/*!40000 ALTER TABLE `mariners` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ocean`
--

DROP TABLE IF EXISTS `ocean`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ocean` (
  `ocean_id` int NOT NULL AUTO_INCREMENT,
  `ocean_type` varchar(10) NOT NULL,
  `present_in_nz` int NOT NULL,
  `common_name` varchar(45) NOT NULL,
  `scientific_name` varchar(45) NOT NULL,
  `characteristics` varchar(100) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `threats` varchar(1000) DEFAULT NULL,
  `location` varchar(1000) DEFAULT NULL,
  `images` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ocean_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocean`
--

LOCK TABLES `ocean` WRITE;
/*!40000 ALTER TABLE `ocean` DISABLE KEYS */;
INSERT INTO `ocean` VALUES (1,'pest',1,'Asian brown mussel','Perna perna\n','','','The green-lipped mussel is culturally and economically important to New Zealand. If the Asian brown mussel got here, it would compete for food and space with green-lipped mussels. Asian brown mussels thrive on human structures. They can create fouling problems in places like jetties, buoys, and boat hulls. They could also bring new diseases to New Zealand that could harm our native shellfish.','You would be more likely to find Asian brown mussels in the north of New Zealand, as they need warm temperatures to reproduce. But they can survive nearly anywhere in our waters.',''),(2,'disease',1,'Bacterial kidney disease in finfish','Renibacterium salmoninarum','','This kidney disease mostly infects salmon and trout but other species are also at risk. A bacterium causes the disease. The bacteria are passed from fish to fish and from parent to egg. This disease is prevalent in the Northern Hemisphere and Chile. It was first described in Scotland.','Chinook salmon is the main species of salmon farmed in New Zealand. It is susceptible to this disease. Bacterial kidney disease kills large numbers of young fish in both freshwater and seawater. If a fish survives the infection they can pass on the bacteria to their offspring','Infected fish are mostly likely to be found in fish farms, both freshwater and marine.','');
/*!40000 ALTER TABLE `ocean` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `staff_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `psw` varchar(100) NOT NULL,
  `email` varchar(30) NOT NULL,
  `first_name` varchar(25) DEFAULT NULL,
  `last_name` varchar(25) DEFAULT NULL,
  `work_phone_number` int DEFAULT NULL,
  `hire_date` datetime DEFAULT NULL,
  `position` varchar(20) DEFAULT NULL,
  `department` varchar(20) DEFAULT NULL,
  `status` int DEFAULT NULL,
  PRIMARY KEY (`staff_id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-02 12:26:32
