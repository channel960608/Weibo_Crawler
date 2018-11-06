/*
 Navicat Premium Data Transfer

 Source Server         : connect
 Source Server Type    : MySQL
 Source Server Version : 50716
 Source Host           : localhost
 Source Database       : weibo

 Target Server Type    : MySQL
 Target Server Version : 50716
 File Encoding         : utf-8

 Date: 01/03/2018 22:28:19 PM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` varchar(10) NOT NULL,
  `nickname` varchar(200) NOT NULL,
  `gender` varchar(200) NOT NULL,
  `location` varchar(200) NOT NULL,
  `signup_date` varchar(200) NOT NULL,
  `brief_intro` varchar(200) NOT NULL,
  `credit` varchar(200) NOT NULL,
  `age` varchar(200) DEFAULT NULL,
  `verify` varchar(200) DEFAULT NULL,
  `tags` varchar(200) DEFAULT NULL,
  `level` varchar(200) DEFAULT NULL,
  `company` varchar(200) DEFAULT NULL,
  `school` varchar(200) DEFAULT NULL,
  `blog` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `weibo_content`
-- ----------------------------
DROP TABLE IF EXISTS `weibo_content`;
CREATE TABLE `weibo_content` (
  `userid` varchar(200) NOT NULL,
  `id` varchar(200) NOT NULL,
  `pub_date` varchar(200) NOT NULL,
  `text` text NOT NULL,
  `pic` varchar(800) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------
--  Table structure for `fans`
-- ----------------------------
DROP TABLE IF EXISTS `fans`;
CREATE TABLE `fans` (
  `id` varchar(10) NOT NULL,
  `nickname` varchar(200) NOT NULL,
  `profile_image_url` varchar(200) NOT NULL,
  `profile_url` varchar(200) NOT NULL,
  `statuses_count` varchar(200) DEFAULT NULL,
  `verified` tinyint(4) NOT NULL,
  `verified_type` tinyint(4) NOT NULL,
  `close_blue_v` tinyint(4) DEFAULT NULL,
  `description` varchar(200) NOT NULL,
  `gender` varchar(4) DEFAULT NULL,
  `urank` varchar(255) DEFAULT NULL,
  `mbtype` tinyint(4) NOT NULL,
  `followers_count` int(11) NOT NULL,
  `follow_count` int(11) NOT NULL,
  `cover_image_phone` varchar(200) NOT NULL,
  `desc1` varchar(255) DEFAULT NULL,
  `desc2` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
