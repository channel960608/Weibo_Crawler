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

