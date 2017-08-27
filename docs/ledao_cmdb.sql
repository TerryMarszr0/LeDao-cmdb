-- MySQL dump 10.13  Distrib 5.7.12, for osx10.11 (x86_64)
--
-- Host: localhost    Database: ledao_cmdb
-- ------------------------------------------------------
-- Server version	5.7.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_app`
--

CREATE DATABASE `ledao_cmdb` character set utf8;
use ledao_cmdb;

DROP TABLE IF EXISTS `app_app`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_app` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) DEFAULT NULL,
  `cname` varchar(120) DEFAULT NULL,
  `group` varchar(30) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_app`
--

LOCK TABLES `app_app` WRITE;
/*!40000 ALTER TABLE `app_app` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_app` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_app_principals`
--

DROP TABLE IF EXISTS `app_app_principals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_app_principals` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) DEFAULT NULL,
  `user_name` varchar(120) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_app_principals`
--

LOCK TABLES `app_app_principals` WRITE;
/*!40000 ALTER TABLE `app_app_principals` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_app_principals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_appsegment`
--

DROP TABLE IF EXISTS `app_appsegment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_appsegment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) DEFAULT NULL,
  `segment` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_appsegment`
--

LOCK TABLES `app_appsegment` WRITE;
/*!40000 ALTER TABLE `app_appsegment` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_appsegment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_group`
--

DROP TABLE IF EXISTS `app_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `full_name` varchar(120) DEFAULT NULL,
  `owner` varchar(120) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_group`
--

LOCK TABLES `app_group` WRITE;
/*!40000 ALTER TABLE `app_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_service`
--

DROP TABLE IF EXISTS `app_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) DEFAULT NULL,
  `name` varchar(120) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `vcs_rep` varchar(255) DEFAULT NULL,
  `state` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_service`
--

LOCK TABLES `app_service` WRITE;
/*!40000 ALTER TABLE `app_service` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_service_principals`
--

DROP TABLE IF EXISTS `app_service_principals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_service_principals` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service_id` int(11) DEFAULT NULL,
  `user_name` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_service_principals`
--

LOCK TABLES `app_service_principals` WRITE;
/*!40000 ALTER TABLE `app_service_principals` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_service_principals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_service_resource`
--

DROP TABLE IF EXISTS `app_service_resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_service_resource` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service` varchar(50) DEFAULT NULL,
  `key` varchar(50) DEFAULT NULL,
  `max` double DEFAULT NULL,
  `min` double DEFAULT NULL,
  `avg` double DEFAULT NULL,
  `ctime` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_service_resource`
--

LOCK TABLES `app_service_resource` WRITE;
/*!40000 ALTER TABLE `app_service_resource` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_service_resource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_servicehost`
--

DROP TABLE IF EXISTS `app_servicehost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_servicehost` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service_id` int(11) DEFAULT NULL,
  `host_id` int(11) DEFAULT NULL,
  `state` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_servicehost_service_id_host_id_de1b77b1_uniq` (`service_id`,`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_servicehost`
--

LOCK TABLES `app_servicehost` WRITE;
/*!40000 ALTER TABLE `app_servicehost` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_servicehost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asset_conf`
--

DROP TABLE IF EXISTS `asset_conf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `asset_conf` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) DEFAULT NULL,
  `cpu` varchar(255) DEFAULT NULL,
  `disk` varchar(255) DEFAULT NULL,
  `memory` varchar(255) DEFAULT NULL,
  `raid` varchar(255) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asset_conf`
--

LOCK TABLES `asset_conf` WRITE;
/*!40000 ALTER TABLE `asset_conf` DISABLE KEYS */;
/*!40000 ALTER TABLE `asset_conf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asset_ipaddress`
--

DROP TABLE IF EXISTS `asset_ipaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `asset_ipaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `network_id` int(11) DEFAULT NULL,
  `ip` varchar(30) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ip` (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asset_ipaddress`
--

LOCK TABLES `asset_ipaddress` WRITE;
/*!40000 ALTER TABLE `asset_ipaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `asset_ipaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asset_model`
--

DROP TABLE IF EXISTS `asset_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `asset_model` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  `firm_name` varchar(255) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asset_model`
--

LOCK TABLES `asset_model` WRITE;
/*!40000 ALTER TABLE `asset_model` DISABLE KEYS */;
/*!40000 ALTER TABLE `asset_model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asset_network`
--

DROP TABLE IF EXISTS `asset_network`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `asset_network` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room_id` int(11) NOT NULL,
  `env` varchar(30) NOT NULL,
  `network` varchar(30) NOT NULL,
  `mask` varchar(30) NOT NULL,
  `maskint` int(11) NOT NULL,
  `gateway` varchar(30) NOT NULL,
  `vlan` int(11) NOT NULL,
  `ctime` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `asset_network_network_maskint_9db24f2f_uniq` (`network`,`maskint`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asset_network`
--

LOCK TABLES `asset_network` WRITE;
/*!40000 ALTER TABLE `asset_network` DISABLE KEYS */;
/*!40000 ALTER TABLE `asset_network` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asset_rack`
--

DROP TABLE IF EXISTS `asset_rack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `asset_rack` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asset_rack`
--

LOCK TABLES `asset_rack` WRITE;
/*!40000 ALTER TABLE `asset_rack` DISABLE KEYS */;
/*!40000 ALTER TABLE `asset_rack` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asset_room`
--

DROP TABLE IF EXISTS `asset_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `asset_room` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `region_id` varchar(100) DEFAULT NULL,
  `zone_id` varchar(100) DEFAULT NULL,
  `cn_name` varchar(100) DEFAULT NULL,
  `tag` varchar(30) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `cn_name` (`cn_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asset_room`
--

LOCK TABLES `asset_room` WRITE;
/*!40000 ALTER TABLE `asset_room` DISABLE KEYS */;
/*!40000 ALTER TABLE `asset_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asset_type`
--

DROP TABLE IF EXISTS `asset_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `asset_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `cn_name` varchar(100) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asset_type`
--

LOCK TABLES `asset_type` WRITE;
/*!40000 ALTER TABLE `asset_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `asset_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_default_group`
--

DROP TABLE IF EXISTS `auth_default_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_default_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_default_group`
--

LOCK TABLES `auth_default_group` WRITE;
/*!40000 ALTER TABLE `auth_default_group` DISABLE KEYS */;
INSERT INTO `auth_default_group` VALUES (1,'普通用户');
/*!40000 ALTER TABLE `auth_default_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'普通用户'),(2,'管理员');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_menus`
--

DROP TABLE IF EXISTS `auth_group_menus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_menus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `menu_id` varchar(720) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_menus`
--

LOCK TABLES `auth_group_menus` WRITE;
/*!40000 ALTER TABLE `auth_group_menus` DISABLE KEYS */;
INSERT INTO `auth_group_menus` VALUES (1,1,'21'),(2,1,'27'),(3,1,'28'),(4,1,'29'),(5,1,'22'),(6,1,'30'),(7,1,'31'),(8,1,'33'),(9,1,'34'),(10,1,'23'),(11,1,'35'),(12,1,'36'),(13,1,'24'),(14,1,'39'),(15,2,'20'),(16,2,'25'),(17,2,'21'),(18,2,'27'),(19,2,'28'),(20,2,'29'),(21,2,'22'),(22,2,'30'),(23,2,'31'),(24,2,'32'),(25,2,'33'),(26,2,'34'),(27,2,'23'),(28,2,'35'),(29,2,'36'),(30,2,'37'),(31,2,'38'),(32,2,'24'),(33,2,'39'),(34,2,'40'),(35,2,'41'),(36,2,'42'),(37,2,'69'),(38,2,'70');
/*!40000 ALTER TABLE `auth_group_menus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add permission',3,'add_permission'),(8,'Can change permission',3,'change_permission'),(9,'Can delete permission',3,'delete_permission'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add Token',7,'add_token'),(20,'Can change Token',7,'change_token'),(21,'Can delete Token',7,'delete_token'),(22,'Can add conf',8,'add_conf'),(23,'Can change conf',8,'change_conf'),(24,'Can delete conf',8,'delete_conf'),(25,'Can add asset type',9,'add_assettype'),(26,'Can change asset type',9,'change_assettype'),(27,'Can delete asset type',9,'delete_assettype'),(28,'Can add asset model',10,'add_assetmodel'),(29,'Can change asset model',10,'change_assetmodel'),(30,'Can delete asset model',10,'delete_assetmodel'),(31,'Can add rack',11,'add_rack'),(32,'Can change rack',11,'change_rack'),(33,'Can delete rack',11,'delete_rack'),(34,'Can add network',12,'add_network'),(35,'Can change network',12,'change_network'),(36,'Can delete network',12,'delete_network'),(37,'Can add ip address',13,'add_ipaddress'),(38,'Can change ip address',13,'change_ipaddress'),(39,'Can delete ip address',13,'delete_ipaddress'),(40,'Can add room',14,'add_room'),(41,'Can change room',14,'change_room'),(42,'Can delete room',14,'delete_room'),(43,'Can add app service',15,'add_appservice'),(44,'Can change app service',15,'change_appservice'),(45,'Can delete app service',15,'delete_appservice'),(46,'Can add app segment',16,'add_appsegment'),(47,'Can change app segment',16,'change_appsegment'),(48,'Can delete app segment',16,'delete_appsegment'),(49,'Can add app principals',17,'add_appprincipals'),(50,'Can change app principals',17,'change_appprincipals'),(51,'Can delete app principals',17,'delete_appprincipals'),(52,'Can add service host',18,'add_servicehost'),(53,'Can change service host',18,'change_servicehost'),(54,'Can delete service host',18,'delete_servicehost'),(55,'Can add service principals',19,'add_serviceprincipals'),(56,'Can change service principals',19,'change_serviceprincipals'),(57,'Can delete service principals',19,'delete_serviceprincipals'),(58,'Can add group',20,'add_group'),(59,'Can change group',20,'change_group'),(60,'Can delete group',20,'delete_group'),(61,'Can add app',21,'add_app'),(62,'Can change app',21,'change_app'),(63,'Can delete app',21,'delete_app'),(64,'Can add service resource',22,'add_serviceresource'),(65,'Can change service resource',22,'change_serviceresource'),(66,'Can delete service resource',22,'delete_serviceresource'),(67,'Can add hosts',23,'add_hosts'),(68,'Can change hosts',23,'change_hosts'),(69,'Can delete hosts',23,'delete_hosts'),(70,'Can add image',24,'add_image'),(71,'Can change image',24,'change_image'),(72,'Can delete image',24,'delete_image'),(73,'Can add host info',25,'add_hostinfo'),(74,'Can change host info',25,'change_hostinfo'),(75,'Can delete host info',25,'delete_hostinfo'),(76,'Can add image tag',26,'add_imagetag'),(77,'Can change image tag',26,'change_imagetag'),(78,'Can delete image tag',26,'delete_imagetag'),(79,'Can add host password',27,'add_hostpassword'),(80,'Can change host password',27,'change_hostpassword'),(81,'Can delete host password',27,'delete_hostpassword'),(82,'Can add host deleted',28,'add_hostdeleted'),(83,'Can change host deleted',28,'change_hostdeleted'),(84,'Can delete host deleted',28,'delete_hostdeleted'),(85,'Can add async task',29,'add_asynctask'),(86,'Can change async task',29,'change_asynctask'),(87,'Can delete async task',29,'delete_asynctask'),(88,'Can add default group',30,'add_defaultgroup'),(89,'Can change default group',30,'change_defaultgroup'),(90,'Can delete default group',30,'delete_defaultgroup'),(91,'Can add menu',31,'add_menu'),(92,'Can change menu',31,'change_menu'),(93,'Can delete menu',31,'delete_menu'),(94,'Can add group menu',32,'add_groupmenu'),(95,'Can change group menu',32,'change_groupmenu'),(96,'Can delete group menu',32,'delete_groupmenu'),(97,'Can add lb',33,'add_lb'),(98,'Can change lb',33,'change_lb'),(99,'Can delete lb',33,'delete_lb'),(100,'Can add service lb',34,'add_servicelb'),(101,'Can change service lb',34,'change_servicelb'),(102,'Can delete service lb',34,'delete_servicelb'),(103,'Can add change',35,'add_change'),(104,'Can change change',35,'change_change'),(105,'Can delete change',35,'delete_change'),(106,'Can add ssh key',36,'add_sshkey'),(107,'Can change ssh key',36,'change_sshkey'),(108,'Can delete ssh key',36,'delete_sshkey'),(109,'Can add apply record',37,'add_applyrecord'),(110,'Can change apply record',37,'change_applyrecord'),(111,'Can delete apply record',37,'delete_applyrecord'),(112,'Can add auth record',38,'add_authrecord'),(113,'Can change auth record',38,'change_authrecord'),(114,'Can delete auth record',38,'delete_authrecord'),(115,'Can add apply task',39,'add_applytask'),(116,'Can change apply task',39,'change_applytask'),(117,'Can delete apply task',39,'delete_applytask');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$36000$3vZlF75goRZA$5TxJLEbj82js/NK3QWrcWEbDHEUqQFGxSnmhXrL3oLI=','2017-08-27 02:23:56.545731',1,'chenshaodong','','','csd@163.com',1,1,'2017-08-27 02:21:25.385542');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
INSERT INTO `authtoken_token` VALUES ('8205b39f0c66b62ae47fcbabc036f184cb8c41dc','2017-08-27 02:28:41.686782',1);
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `change_change`
--

DROP TABLE IF EXISTS `change_change`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `change_change` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(128) DEFAULT NULL,
  `username` varchar(60) DEFAULT NULL,
  `resource` varchar(60) DEFAULT NULL,
  `res_id` varchar(64) DEFAULT NULL,
  `action` varchar(30) DEFAULT NULL,
  `index` varchar(100) DEFAULT NULL,
  `message` longtext NOT NULL,
  `change_time` int(11) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `change_change_resource_res_id_b4b21f9f_idx` (`resource`,`res_id`),
  KEY `change_change_index_e0b35760` (`index`),
  KEY `change_change_change_time_3c1950cd` (`change_time`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `change_change`
--

LOCK TABLES `change_change` WRITE;
/*!40000 ALTER TABLE `change_change` DISABLE KEYS */;
INSERT INTO `change_change` VALUES (1,'fd0d2ac5-8ace-11e7-abf7-20c9d07f6101','chenshaodong','home_menu','43','delete','location列表','delete menu: location列表',1503800727,1503800727),(2,'913f02a6-8acf-11e7-b03e-20c9d07f6101','chenshaodong','home_menu','34','update','网段管理','{\"name\": \"\\u7f51\\u6bb5\\u7ba1\\u7406\", \"weight\": 0, \"pid\": 22, \"tag\": \"\\u67e5\\u770b\\u7f51\\u6bb5\", \"path\": \"/asset/network/\", \"id\": 34}',1503800975,1503800975),(3,'9f1b4830-8acf-11e7-9bfc-20c9d07f6101','chenshaodong','home_menu','33','update','配置管理','{\"name\": \"\\u914d\\u7f6e\\u7ba1\\u7406\", \"weight\": 0, \"pid\": 22, \"tag\": \"\\u67e5\\u770b\\u914d\\u7f6e\", \"path\": \"/asset/conf/\", \"id\": 33}',1503800999,1503800999),(4,'a4e54163-8acf-11e7-b890-20c9d07f6101','chenshaodong','home_menu','32','update','镜像管理','{\"name\": \"\\u955c\\u50cf\\u7ba1\\u7406\", \"weight\": 0, \"pid\": 22, \"tag\": \"\\u67e5\\u770b\\u955c\\u50cf\", \"path\": \"/host/image/\", \"id\": 32}',1503801008,1503801008),(5,'aa5779a8-8acf-11e7-abb6-20c9d07f6101','chenshaodong','home_menu','31','update','机房管理','{\"name\": \"\\u673a\\u623f\\u7ba1\\u7406\", \"weight\": 0, \"pid\": 22, \"tag\": \"\\u67e5\\u770b\\u673a\\u623f\", \"path\": \"/asset/room/\", \"id\": 31}',1503801017,1503801017),(6,'b84dc64a-8acf-11e7-9a0e-20c9d07f6101','chenshaodong','home_menu','30','update','设备管理','{\"name\": \"\\u8bbe\\u5907\\u7ba1\\u7406\", \"weight\": 0, \"pid\": 22, \"tag\": \"\\u67e5\\u770b\\u8d44\\u4ea7\", \"path\": \"/host/\", \"id\": 30}',1503801041,1503801041),(7,'bec27430-8acf-11e7-996c-20c9d07f6101','chenshaodong','home_menu','29','update','查看服务','{\"name\": \"\\u67e5\\u770b\\u670d\\u52a1\", \"weight\": 0, \"pid\": 21, \"tag\": \"\\u670d\\u52a1\\u7ba1\\u7406\", \"path\": \"/app/service/\", \"id\": 29}',1503801052,1503801052),(8,'d4c01b66-8acf-11e7-9841-20c9d07f6101','chenshaodong','home_menu','29','update','Service管理','{\"name\": \"Service\\u7ba1\\u7406\", \"weight\": 0, \"pid\": 21, \"tag\": \"\\u670d\\u52a1\\u7ba1\\u7406\", \"path\": \"/app/service/\", \"id\": 29}',1503801089,1503801089),(9,'dc003b8f-8acf-11e7-869e-20c9d07f6101','chenshaodong','home_menu','28','update','应用管理','{\"name\": \"\\u5e94\\u7528\\u7ba1\\u7406\", \"weight\": 0, \"pid\": 21, \"tag\": \"\\u67e5\\u770b\\u5e94\\u7528\", \"path\": \"/app/app/\", \"id\": 28}',1503801101,1503801101),(10,'e30d4f05-8acf-11e7-b05d-20c9d07f6101','chenshaodong','home_menu','27','update','业务线管理','{\"name\": \"\\u4e1a\\u52a1\\u7ebf\\u7ba1\\u7406\", \"weight\": 0, \"pid\": 21, \"tag\": \"\\u67e5\\u770b\\u4e1a\\u52a1\\u7ebf\", \"path\": \"/app/group/\", \"id\": 27}',1503801113,1503801113),(11,'e9255ddc-8acf-11e7-b211-20c9d07f6101','chenshaodong','home_menu','26','update','菜单管理','{\"name\": \"\\u83dc\\u5355\\u7ba1\\u7406\", \"weight\": 0, \"pid\": 20, \"tag\": \"\\u67e5\\u770b\\u83dc\\u5355\", \"path\": \"/user/menu/\", \"id\": 26}',1503801123,1503801123),(12,'efa6a011-8acf-11e7-86e7-20c9d07f6101','chenshaodong','home_menu','25','update','用户管理','{\"name\": \"\\u7528\\u6237\\u7ba1\\u7406\", \"weight\": 0, \"pid\": 20, \"tag\": \"\\u67e5\\u770b\\u7528\\u6237\", \"path\": \"/user/user/\", \"id\": 25}',1503801134,1503801134);
/*!40000 ALTER TABLE `change_change` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(21,'app','app'),(17,'app','appprincipals'),(16,'app','appsegment'),(15,'app','appservice'),(20,'app','group'),(18,'app','servicehost'),(19,'app','serviceprincipals'),(22,'app','serviceresource'),(10,'asset','assetmodel'),(9,'asset','assettype'),(8,'asset','conf'),(13,'asset','ipaddress'),(12,'asset','network'),(11,'asset','rack'),(14,'asset','room'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(7,'authtoken','token'),(35,'change','change'),(5,'contenttypes','contenttype'),(37,'fortress','applyrecord'),(39,'fortress','applytask'),(38,'fortress','authrecord'),(36,'fortress','sshkey'),(28,'host','hostdeleted'),(25,'host','hostinfo'),(27,'host','hostpassword'),(23,'host','hosts'),(24,'host','image'),(26,'host','imagetag'),(33,'lb','lb'),(34,'lb','servicelb'),(29,'public','asynctask'),(6,'sessions','session'),(30,'users','defaultgroup'),(32,'users','groupmenu'),(31,'users','menu');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-08-27 02:19:51.561364'),(2,'auth','0001_initial','2017-08-27 02:19:51.987440'),(3,'admin','0001_initial','2017-08-27 02:19:52.078774'),(4,'admin','0002_logentry_remove_auto_add','2017-08-27 02:19:52.120884'),(5,'app','0001_initial','2017-08-27 02:19:52.393894'),(6,'asset','0001_initial','2017-08-27 02:19:52.642637'),(7,'contenttypes','0002_remove_content_type_name','2017-08-27 02:19:52.772991'),(8,'auth','0002_alter_permission_name_max_length','2017-08-27 02:19:52.812577'),(9,'auth','0003_alter_user_email_max_length','2017-08-27 02:19:52.860005'),(10,'auth','0004_alter_user_username_opts','2017-08-27 02:19:52.879664'),(11,'auth','0005_alter_user_last_login_null','2017-08-27 02:19:52.930233'),(12,'auth','0006_require_contenttypes_0002','2017-08-27 02:19:52.933415'),(13,'auth','0007_alter_validators_add_error_messages','2017-08-27 02:19:52.954958'),(14,'auth','0008_alter_user_username_max_length','2017-08-27 02:19:53.005458'),(15,'authtoken','0001_initial','2017-08-27 02:19:53.082531'),(16,'authtoken','0002_auto_20160226_1747','2017-08-27 02:19:53.216520'),(17,'change','0001_initial','2017-08-27 02:19:53.310041'),(18,'fortress','0001_initial','2017-08-27 02:19:53.435687'),(19,'host','0001_initial','2017-08-27 02:19:53.659379'),(20,'lb','0001_initial','2017-08-27 02:19:53.779277'),(21,'public','0001_initial','2017-08-27 02:19:53.825542'),(22,'sessions','0001_initial','2017-08-27 02:19:53.878255'),(23,'users','0001_initial','2017-08-27 02:19:53.966741');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('q0rh349wgq2calwljgpsmbbglkexwtx3','NzU5NWY2ZTcxZjc1NTQxNDFmOWEzZTg5OWY2YTViY2M2MWE4NjA5Yjp7Il9hdXRoX3VzZXJfaGFzaCI6IjM4ZTFmMzU3MWViNDBlMzNmY2RlNTA3MDc4YTBjOTIzMWVmNWU1M2IiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2017-09-10 02:23:56.550548');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fortress_applyrecord`
--

DROP TABLE IF EXISTS `fortress_applyrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fortress_applyrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apply_user` varchar(60) DEFAULT NULL,
  `apply_time` int(11) DEFAULT NULL,
  `role` varchar(60) DEFAULT NULL,
  `day` int(11) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `reason` varchar(500) DEFAULT NULL,
  `reviewer` varchar(60) DEFAULT NULL,
  `audit_time` int(11) DEFAULT NULL,
  `reviewer_reason` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fortress_applyrecord`
--

LOCK TABLES `fortress_applyrecord` WRITE;
/*!40000 ALTER TABLE `fortress_applyrecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `fortress_applyrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fortress_applytask`
--

DROP TABLE IF EXISTS `fortress_applytask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fortress_applytask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apply_id` int(11) DEFAULT NULL,
  `host_id` int(11) DEFAULT NULL,
  `role` varchar(60) DEFAULT NULL,
  `day` int(11) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `result` varchar(255) DEFAULT NULL,
  `run_time` int(11) DEFAULT NULL,
  `finish_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fortress_applytask`
--

LOCK TABLES `fortress_applytask` WRITE;
/*!40000 ALTER TABLE `fortress_applytask` DISABLE KEYS */;
/*!40000 ALTER TABLE `fortress_applytask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fortress_authrecord`
--

DROP TABLE IF EXISTS `fortress_authrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fortress_authrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(60) DEFAULT NULL,
  `host_id` int(11) DEFAULT NULL,
  `role` varchar(60) DEFAULT NULL,
  `cuser` varchar(60) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  `expiration_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fortress_authrecord`
--

LOCK TABLES `fortress_authrecord` WRITE;
/*!40000 ALTER TABLE `fortress_authrecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `fortress_authrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fortress_sshkey`
--

DROP TABLE IF EXISTS `fortress_sshkey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fortress_sshkey` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `ssh_key` longtext,
  `private_key` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fortress_sshkey`
--

LOCK TABLES `fortress_sshkey` WRITE;
/*!40000 ALTER TABLE `fortress_sshkey` DISABLE KEYS */;
/*!40000 ALTER TABLE `fortress_sshkey` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `home_menu`
--

DROP TABLE IF EXISTS `home_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `home_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `name` varchar(120) DEFAULT NULL,
  `path` varchar(360) DEFAULT NULL,
  `tag` varchar(120) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `home_menu`
--

LOCK TABLES `home_menu` WRITE;
/*!40000 ALTER TABLE `home_menu` DISABLE KEYS */;
INSERT INTO `home_menu` VALUES (20,0,'系统管理','#','group',0),(21,0,'服务管理','#','list',0),(22,0,'资产管理','#','inbox',0),(23,0,'堡垒机管理','#','laptop',0),(24,0,'变更管理','#','tasks',0),(25,20,'用户管理','/user/user/','查看用户',0),(26,20,'菜单管理','/user/menu/','查看菜单',0),(27,21,'业务线管理','/app/group/','查看业务线',0),(28,21,'应用管理','/app/app/','查看应用',0),(29,21,'Service管理','/app/service/','服务管理',0),(30,22,'设备管理','/host/','查看资产',0),(31,22,'机房管理','/asset/room/','查看机房',0),(32,22,'镜像管理','/host/image/','查看镜像',0),(33,22,'配置管理','/asset/conf/','查看配置',0),(34,22,'网段管理','/asset/network/','查看网段',0),(35,23,'授权申请','/fortress/myapply/','授权申请',0),(36,23,'我的授权','/fortress/myauthrecord/','我的授权',0),(37,23,'授权审批','/fortress/audit/','授权审批',0),(38,23,'授权查询','/fortress/authrecord/','授权查询',0),(39,24,'变更查询','/change/change/','变更查询',0),(40,24,'任务查询','/public/task/','任务查询',0),(41,0,'负载均衡管理','#','sitemap',0),(42,41,'负载均衡列表','/lb/lblist/','sitemap',0),(44,20,'角色菜单','/user/group_menu/','fa',0),(69,0,'Dashboard','#','tachometer',100),(70,69,'设备统计','/dashboard/servers/','fa',100);
/*!40000 ALTER TABLE `home_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_hostdeleted`
--

DROP TABLE IF EXISTS `host_hostdeleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_hostdeleted` (
  `id` int(11) NOT NULL,
  `instance_id` varchar(128) NOT NULL,
  `sn` varchar(90) DEFAULT NULL,
  `mac` varchar(90) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  `attribute` varchar(30) DEFAULT NULL,
  `env` varchar(30) DEFAULT NULL,
  `model_id` int(11) DEFAULT NULL,
  `conf_id` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `rack_id` int(11) DEFAULT NULL,
  `location` varchar(60) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `hostname` varchar(100) DEFAULT NULL,
  `img_id` int(11) DEFAULT NULL,
  `service_id` int(11) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `ip` varchar(60) DEFAULT NULL,
  `oobip` varchar(60) DEFAULT NULL,
  `publicip` varchar(60) DEFAULT NULL,
  `expiration_time` int(11) DEFAULT NULL,
  `shiptime` int(11) DEFAULT NULL,
  `amount` double DEFAULT NULL,
  `aliyun_id` varchar(128) DEFAULT NULL,
  `cpu` varchar(255) DEFAULT NULL,
  `memory` varchar(255) DEFAULT NULL,
  `disk` varchar(500) DEFAULT NULL,
  `os_name` varchar(255) DEFAULT NULL,
  `kernel` varchar(120) DEFAULT NULL,
  `region_id` varchar(60) DEFAULT NULL,
  `zone_id` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `instance_id` (`instance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_hostdeleted`
--

LOCK TABLES `host_hostdeleted` WRITE;
/*!40000 ALTER TABLE `host_hostdeleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `host_hostdeleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_hostpassword`
--

DROP TABLE IF EXISTS `host_hostpassword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_hostpassword` (
  `ip` varchar(30) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_hostpassword`
--

LOCK TABLES `host_hostpassword` WRITE;
/*!40000 ALTER TABLE `host_hostpassword` DISABLE KEYS */;
/*!40000 ALTER TABLE `host_hostpassword` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_hosts`
--

DROP TABLE IF EXISTS `host_hosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_hosts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` varchar(128) NOT NULL,
  `sn` varchar(90) DEFAULT NULL,
  `mac` varchar(90) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  `attribute` varchar(30) DEFAULT NULL,
  `env` varchar(30) DEFAULT NULL,
  `model_id` int(11) DEFAULT NULL,
  `conf_id` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `rack_id` int(11) DEFAULT NULL,
  `location` varchar(60) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `hostname` varchar(100) DEFAULT NULL,
  `img_id` int(11) DEFAULT NULL,
  `service_id` int(11) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `ip` varchar(60) DEFAULT NULL,
  `oobip` varchar(60) DEFAULT NULL,
  `publicip` varchar(60) DEFAULT NULL,
  `expiration_time` int(11) DEFAULT NULL,
  `shiptime` int(11) DEFAULT NULL,
  `amount` double DEFAULT NULL,
  `aliyun_id` varchar(128) DEFAULT NULL,
  `cpu` varchar(255) DEFAULT NULL,
  `memory` varchar(255) DEFAULT NULL,
  `disk` varchar(500) DEFAULT NULL,
  `os_name` varchar(255) DEFAULT NULL,
  `kernel` varchar(120) DEFAULT NULL,
  `region_id` varchar(60) DEFAULT NULL,
  `zone_id` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `instance_id` (`instance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_hosts`
--

LOCK TABLES `host_hosts` WRITE;
/*!40000 ALTER TABLE `host_hosts` DISABLE KEYS */;
/*!40000 ALTER TABLE `host_hosts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_image`
--

DROP TABLE IF EXISTS `host_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `image_id` varchar(100) DEFAULT NULL,
  `os_type` varchar(30) DEFAULT NULL,
  `platform` varchar(60) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_image`
--

LOCK TABLES `host_image` WRITE;
/*!40000 ALTER TABLE `host_image` DISABLE KEYS */;
/*!40000 ALTER TABLE `host_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_image_tag`
--

DROP TABLE IF EXISTS `host_image_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_image_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img_id` int(11) DEFAULT NULL,
  `tag` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_image_tag`
--

LOCK TABLES `host_image_tag` WRITE;
/*!40000 ALTER TABLE `host_image_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `host_image_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_info`
--

DROP TABLE IF EXISTS `host_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(32) DEFAULT NULL,
  `network` varchar(32) DEFAULT NULL,
  `gateway` varchar(32) DEFAULT NULL,
  `netmask` varchar(32) DEFAULT NULL,
  `fqdn` varchar(128) DEFAULT NULL,
  `network_card` varchar(1024) DEFAULT NULL,
  `mac` varchar(128) DEFAULT NULL,
  `os_name` varchar(128) DEFAULT NULL,
  `kernel` varchar(128) DEFAULT NULL,
  `cpu` varchar(128) DEFAULT NULL,
  `memory` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_info`
--

LOCK TABLES `host_info` WRITE;
/*!40000 ALTER TABLE `host_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `host_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lb_lb`
--

DROP TABLE IF EXISTS `lb_lb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lb_lb` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lb_service_id` int(11) NOT NULL,
  `env` varchar(30) NOT NULL,
  `server_name` varchar(255) NOT NULL,
  `port` int(11) NOT NULL,
  `sslport` int(11) NOT NULL,
  `parameter` varchar(3000) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  `cuser` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lb_lb_server_name_port_env_3785041a_uniq` (`server_name`,`port`,`env`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lb_lb`
--

LOCK TABLES `lb_lb` WRITE;
/*!40000 ALTER TABLE `lb_lb` DISABLE KEYS */;
/*!40000 ALTER TABLE `lb_lb` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lb_servicelb`
--

DROP TABLE IF EXISTS `lb_servicelb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lb_servicelb` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lb_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `path` varchar(255) NOT NULL,
  `proxy_path` varchar(255) NOT NULL,
  `backend_port` int(11) NOT NULL,
  `location_parameter` varchar(1500) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lb_servicelb_lb_id_path_9d0e42d1_uniq` (`lb_id`,`path`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lb_servicelb`
--

LOCK TABLES `lb_servicelb` WRITE;
/*!40000 ALTER TABLE `lb_servicelb` DISABLE KEYS */;
/*!40000 ALTER TABLE `lb_servicelb` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `public_asynctask`
--

DROP TABLE IF EXISTS `public_asynctask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `public_asynctask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task` varchar(255) DEFAULT NULL,
  `params` longtext,
  `state` varchar(30) DEFAULT NULL,
  `result` varchar(255) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  `cuser` varchar(60) DEFAULT NULL,
  `start_time` int(11) DEFAULT NULL,
  `finish_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `public_asynctask`
--

LOCK TABLES `public_asynctask` WRITE;
/*!40000 ALTER TABLE `public_asynctask` DISABLE KEYS */;
/*!40000 ALTER TABLE `public_asynctask` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-27 10:47:14
