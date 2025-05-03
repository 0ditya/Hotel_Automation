-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: hotel_db
-- ------------------------------------------------------
-- Server version	8.0.30

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
-- Table structure for table `catering_order_item`
--

DROP TABLE IF EXISTS `catering_order_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `catering_order_item` (
  `id` int NOT NULL AUTO_INCREMENT,
  `orderID` int NOT NULL,
  `itemID` int DEFAULT NULL,
  `item_name` varchar(120) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `price_per_unit` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `orderID` (`orderID`),
  CONSTRAINT `catering_order_item_ibfk_1` FOREIGN KEY (`orderID`) REFERENCES `catering_order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catering_order_item`
--

LOCK TABLES `catering_order_item` WRITE;
/*!40000 ALTER TABLE `catering_order_item` DISABLE KEYS */;
INSERT INTO `catering_order_item` VALUES (1,3,1,NULL,3,NULL),(2,3,2,NULL,1,NULL),(3,3,3,NULL,1,NULL),(4,3,4,NULL,1,NULL),(5,4,1,NULL,2,NULL),(6,4,2,NULL,1,NULL),(7,4,3,NULL,1,NULL),(8,4,4,NULL,1,NULL),(9,5,1,NULL,2,NULL),(10,5,2,NULL,2,NULL),(11,5,3,NULL,2,NULL),(12,5,4,NULL,2,NULL),(13,6,1,'Paneer Butter Masala',3,180),(14,6,2,'Veg Biryani',2,150),(15,6,3,'Tandoori Roti',3,20),(16,6,4,'Gulab Jamun',3,40),(17,7,1,'Paneer Butter Masala',4,180),(18,7,2,'Veg Biryani',1,150),(19,7,4,'Gulab Jamun',1,40),(20,8,1,'Paneer Butter Masala',55,180),(21,9,1,'Paneer Butter Masala',3,180),(22,9,2,'Veg Biryani',1,150),(23,9,3,'Tandoori Roti',1,20),(24,9,4,'Gulab Jamun',1,40);
/*!40000 ALTER TABLE `catering_order_item` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-24 11:00:16
