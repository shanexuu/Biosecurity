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
  `user_id` int NOT NULL,
  `mariners_id_number` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `mariners_id_number` (`mariners_id_number`),
  CONSTRAINT `mariners_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `ocean_type` enum('pest','disease') NOT NULL,
  `present_in_nz` enum('yes','no') NOT NULL,
  `common_name` varchar(255) NOT NULL,
  `scientific_name` varchar(255) DEFAULT NULL,
  `characteristics` longtext,
  `description` longtext,
  `threats` longtext,
  `location` longtext,
  PRIMARY KEY (`ocean_id`),
  KEY `common_name` (`common_name`),
  KEY `scientific_name` (`scientific_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocean`
--

LOCK TABLES `ocean` WRITE;
/*!40000 ALTER TABLE `ocean` DISABLE KEYS */;
INSERT INTO `ocean` VALUES (1,'pest','no','Northern Pacific Sea Star','Asterias amurensis','The North Pacific Sea star generally has five arms which have pointed and often up-turned tips. The arms join onto a central disc and are covered by clumps of small chisel-like spines. Adults are ~10 cm diameter, with individual arms sometimes up to 40-60 mm long. The topside of the seastar varies in colour and can be yellow, orange or have purple markings. Underneath, they are generally yellow with spines in a single line either side of the groove where the tube feet lie.','The Northern Pacific sea star is a large star fish (up to 50cm in diameter) that is native to the coastal waters of the north-western Pacific Ocean, including Japan, Russia, North China, and Korea. It has been introduced inadvertently to Australia where it occurs in large numbers in several estuaries and embayments in the states of Tasmania and Victoria. The Northern Pacific sea star is normally found in shallow water but occurs from the intertidal area through to the subtidal as deep as 200 m. It can be found on muddy, sandy, pebbly seabeds as well as on rocks and man-made surfaces, even mussel lines. You would not normally see it in areas with high wave action.','The Northern Pacific sea star is a voracious predator that will feed on a wide variety of other marine animals, including shellfish, crabs, worms and even dead fish and other sea stars. Because it can occur in very large numbers and also feeds on wild and farmed shellfish, it could have a serious impact on our aquaculture industry and our marine environment generally.',''),(2,'pest','yes','European shore crab','Carcinus maenas','European shore crabs are medium-sized with a body width (carapace) of up to 9 cm. The upper carapace of adult crabs is a mottled dark brown to green, with small yellow patches and the underside varies from green to orange to red. Juveniles are normally a light sandy colour. Five pointed spines are located on either side of the eyes, with three rounded lobes present between the eyes. Although relate to paddle crabs, the European shore crab does not have swimming paddles on its hind legs.','The European shore crab (also called the \'green crab\') is native to the Atlantic Coast of Europe and northern Africa. It has been introduced to North America, Japan, South Africa and Australia. It is a habitat generalist that can tolerate a wide range of salinities and temperature, helping it to survive in a range of habitats from the intertidal zone of estuaries to the open ocean.Â  It is also tolerant of low levels of dissolved oxygen and can persist in polluted water.\r\n\r\nEuropean shore crabs can live for up to 6 years. Females reproduce at 1-3 years old and are highly fecund, producing between 185,000 to 200,000 fertilised eggs at a time. The free swimming larvae remain in the plankton for up to 90 days, facilitating dispersal by water currents. It may have been spread intentionally for human consumption or through vessel ballast water or as hull fouling.They are nocturnal, feeding mostly at night.','In some areas where it has been introduced, the European shore crab can reach densities of up to 200 per square metre. It consumes a wide range of species, including other crabs and shellfish. Because of this it can have large impacts on the native flora and fauna in estuarine and marine ecosystems. It has also had economic impacts on some shellfish industries.','');
/*!40000 ALTER TABLE `ocean` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oceanImages`
--

DROP TABLE IF EXISTS `oceanImages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oceanImages` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `ocean_id` int NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `is_primary` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`image_id`),
  KEY `ocean_id` (`ocean_id`),
  CONSTRAINT `oceanimages_ibfk_1` FOREIGN KEY (`ocean_id`) REFERENCES `ocean` (`ocean_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oceanImages`
--

LOCK TABLES `oceanImages` WRITE;
/*!40000 ALTER TABLE `oceanImages` DISABLE KEYS */;
INSERT INTO `oceanImages` VALUES (1,1,'app/static/assets/img/Asterias-cropped-280px.png',0),(2,2,'app/static/assets/img/green-crab-id-280px.png',0);
/*!40000 ALTER TABLE `oceanImages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `user_id` int NOT NULL,
  `staff_number` varchar(255) NOT NULL,
  `hire_date` date NOT NULL,
  `position` varchar(255) NOT NULL,
  `department` varchar(255) DEFAULT NULL,
  `work_phone_number` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `staff_number` (`staff_number`),
  CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (1,'Staff_1','2010-04-20','Administrator','Management','0828327788');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `phone_number` varchar(50) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `status` enum('active','inactive') DEFAULT NULL,
  `role` enum('mariners','staff','admin') DEFAULT NULL,
  `date_joined` date DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','24bee570a67c39d332322e28ca612a6e41b5f4faac151392fed4fbc9b4c6391e','admin@hotmail.com','Jane','Doe','0210972323','120 lincoln St, Lincoln 7647, Canterbury New Zealand','active','admin','2010-04-20'),(5,'shanexu','729138248fb61c8f894beb145df1f7d8ca6805c3e388b3b1cbf9fd532d352e0c','shanexu@gmail.com','Shane','Xu',NULL,NULL,'active','mariners','2024-03-10'),(6,'alex','24bee570a67c39d332322e28ca612a6e41b5f4faac151392fed4fbc9b4c6391e','alex@alex.com','Alex','Captain','None','None','active','mariners','2024-03-10');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-11 11:23:44
