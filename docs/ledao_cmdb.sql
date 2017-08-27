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

-- CREATE DATABASE `ledao_cmdb` character set utf8;

-- use ledao_cmdb;

DROP TABLE IF EXISTS `app_app`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_app` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `group` varchar(30),
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
-- Table structure for table `app_service`
--

DROP TABLE IF EXISTS `app_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `app_id` int(11),
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_service_name_2bb4b8e8_uniq` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `comment` varchar(255),
  `ctime` int(11),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `ctime` int(11),
  PRIMARY KEY (`id`),
  UNIQUE KEY `asset_model_name_22228117_uniq` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
-- Table structure for table `asset_room`
--

DROP TABLE IF EXISTS `asset_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `asset_room` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `cn_name` varchar(100) DEFAULT NULL,
  `tag` varchar(30) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  `region_id` varchar(100) DEFAULT NULL,
  `zone_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `asset_room_cn_name_52312b99_uniq` (`cn_name`),
  UNIQUE KEY `asset_room_tag_b1f8ea70_uniq` (`tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `change_change`
--

DROP TABLE IF EXISTS `change_change`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `change_change` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(60) DEFAULT NULL,
  `resource` varchar(60) DEFAULT NULL,
  `res_id` varchar(64),
  `action` varchar(30) DEFAULT NULL,
  `index` varchar(100) DEFAULT NULL,
  `message` longtext NOT NULL,
  `change_time` int(11) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  `uuid` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `change_change_resource_res_id_b4b21f9f_idx` (`resource`,`res_id`),
  KEY `change_change_index_e0b35760` (`index`),
  KEY `change_change_change_time_3c1950cd` (`change_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `host_hosts`
--

DROP TABLE IF EXISTS `host_hosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_hosts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(90) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  `attribute` varchar(30) DEFAULT NULL,
  `model_id` int(11) DEFAULT NULL,
  `conf_id` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `rack_id` int(11) DEFAULT NULL,
  `location` varchar(60) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `hostname` varchar(100) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `ip` varchar(60) DEFAULT NULL,
  `oobip` varchar(60) DEFAULT NULL,
  `expiration_time` int(11) DEFAULT NULL,
  `shiptime` int(11) DEFAULT NULL,
  `env` varchar(30),
  `mac` varchar(90),
  `pid` int(11),
  `amount` double,
  `ctime` int(11),
  `instance_id` varchar(128) NOT NULL,
  `aliyun_id` varchar(128) DEFAULT NULL,
  `publicip` varchar(60),
  `service_id` int(11),
  `cpu` varchar(255),
  `disk` varchar(500),
  `memory` varchar(255),
  `os_name` varchar(255),
  `kernel` varchar(120) DEFAULT NULL,
  `region_id` varchar(60) DEFAULT NULL,
  `zone_id` varchar(60) DEFAULT NULL,
  `img_id` int(11),
  PRIMARY KEY (`id`),
  UNIQUE KEY `instance_id` (`instance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `host_image`
--

DROP TABLE IF EXISTS `host_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `ctime` int(11),
  `image_id` varchar(100),
  `os_type` varchar(30),
  `platform` varchar(60),
  PRIMARY KEY (`id`),
  UNIQUE KEY `host_os_name_230ad653_uniq` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
-- Table structure for table `lb_appslb`
--

DROP TABLE IF EXISTS `lb_appslb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lb_appslb` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slb_id` int(11),
  `domain` varchar(255) DEFAULT NULL,
  `listen` varchar(100) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `rs_port` int(11) DEFAULT NULL,
  `include_conf` longtext,
  `upstream_path` varchar(255) NOT NULL,
  `proxy_set_header_host` varchar(255) NOT NULL,
  `head_include_conf` longtext,
  `proxy_set_header_conf` longtext NOT NULL,
  `ctime` int(11) DEFAULT NULL,
  `cuser` varchar(60) DEFAULT NULL,
  `service_id` int(11),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lb_slb`
--

DROP TABLE IF EXISTS `lb_slb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lb_slb` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `env` varchar(30) NOT NULL,
  `position` varchar(30) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `cuser` varchar(60) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  `app_id` int(11),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lb_slbip`
--

DROP TABLE IF EXISTS `lb_slbip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lb_slbip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slb_id` int(11) DEFAULT NULL,
  `ip` varchar(255) NOT NULL,
  `ctime` int(11) DEFAULT NULL,
  `cuser` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lb_slbvip`
--

DROP TABLE IF EXISTS `lb_slbvip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lb_slbvip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slb_id` int(11) DEFAULT NULL,
  `line` varchar(30) NOT NULL,
  `line_type` varchar(30) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `ctime` int(11) DEFAULT NULL,
  `cuser` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-05-03  9:12:25


CREATE TABLE `app_servicehost` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service_id` int(11) DEFAULT NULL,
  `host_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_servicehost_service_id_host_id_de1b77b1_uniq` (`service_id`,`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



-- 20170509

CREATE TABLE `public_asynctask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task` varchar(255) DEFAULT NULL,
  `params` longtext,
  `state` varchar(30) DEFAULT NULL,
  `result` varchar(255) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  `cuser` varchar(60) DEFAULT NULL,
  `finish_time` int(11) DEFAULT NULL,
  `start_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `fortress_applytask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apply_id` int(11) DEFAULT NULL,
  `host_id` int(11) DEFAULT NULL,
  `role` varchar(60) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `result` varchar(255) DEFAULT NULL,
  `run_time` int(11) DEFAULT NULL,
  `finish_time` int(11) DEFAULT NULL,
  `day` int(11),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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

CREATE TABLE `fortress_sshkey` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `ssh_key` longtext,
  `private_key` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


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


CREATE TABLE `asset_ipaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `network_id` int(11) DEFAULT NULL,
  `ip` varchar(30) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `asset_ipaddress_ip_b9c6d19e_uniq` (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER table app_app add COLUMN cname varchar(120);

CREATE TABLE `app_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `full_name` varchar(120) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `owner` varchar(120),
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER table app_service add COLUMN `vcs_rep` varchar(255);


CREATE TABLE `host_hostpassword` (
  `ip` varchar(30) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `app_utilizationrate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service_id` int(11) DEFAULT NULL,
  `load` double DEFAULT NULL,
  `cpu` double DEFAULT NULL,
  `memory` double DEFAULT NULL,
  `qps` double DEFAULT NULL,
  `tps` double DEFAULT NULL,
  `ctime` int(11),
  `iops` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `lb_lb` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `service_id` int(11) NOT NULL,
  `hostname` varchar(255) NOT NULL,
  `port` int(11) NOT NULL,
  `sslport` int(11) NOT NULL,
  `ssl_conf` varchar(255) DEFAULT NULL,
  `parameter` varchar(1500) DEFAULT NULL,
  `access_log` varchar(255) DEFAULT NULL,
  `error_log` varchar(255) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  `cuser` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `lb_upstream` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `lb_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `url` varchar(255) NOT NULL,
  `upstreamtype` varchar(30) DEFAULT NULL,
  `port` int(11) NOT NULL,
  `max_fails` int(11) NOT NULL,
  `fail_timeout` int(11) NOT NULL,
  `parameter` varchar(1500) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `ctime` int(11) DEFAULT NULL,
  `cuser` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `app_app_principals` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) DEFAULT NULL,
  `user_name` varchar(120) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `auth_group_menus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `menu_id` varchar(720) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `app_service_principals` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service_id` int(11) DEFAULT NULL,
  `user_name` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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

CREATE TABLE `auth_default_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `app_service_resource` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service` varchar(50) NOT NULL,
  `key` varchar(50) NOT NULL,
  `max` float NOT NULL,
  `min` float NOT NULL,
  `avg` float NOT NULL,
  `ctime` int(11) NOT NULL COMMENT '时间戳',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


alter table home_menu change id id int not null auto_increment primary key;

alter table app_service add state varchar(30) not null DEFAULT 'online';


-- lb管理
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

CREATE TABLE `lb_servicelb` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lb_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `proxy_path` varchar(255) NOT NULL,
  `path` varchar(255) NOT NULL,
  `backend_port` int(11) NOT NULL,
  `location_parameter` varchar(1500) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lb_servicelb_lb_id_path_9d0e42d1_uniq` (`lb_id`,`path`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

alter table app_servicehost add state varchar(30) not null DEFAULT 'Down';

alter table app_servicehost modify column state varchar(30) not null DEFAULT 'Down';
