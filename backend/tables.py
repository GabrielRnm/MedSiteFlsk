from __future__ import print_function
import mysql.connector


DB_NAME = 'medusrmain'

TABLES = {}

TABLES['users'] = (
    "CREATE TABLE `user` ("    
    "    `usr_id` INTEGER NOT NULL," 
    "    `username` TEXT,"
    "    `user_email` TEXT," 
    "    `password` TEXT,"
    "    `cpf` TEXT,"     
    "    `contact_number` TEXT,"
    "    `active_status` BOOLEAN,"
    "    `reg_date` TEXT,"
    "    `reg_time` TEXT,"
    "    PRIMARY KEY (`usr_id`)"
    ")")

TABLES['curso'] = (
    "CREATE TABLE `curso` ("
    "   `curs_id` INTEGER NOT NULL,"
    "   `cur_name` TEXT,"
    "   `prof` TEXT,"
    "   `curs_price` TEXT,"
    "   `urs_active` BOOLEAN DEFAULT 1,"
    "   PRIMARY KEY (`curs_id`)"
    ")")

TABLES['curso_check'] = (
    "CREATE TABLE `curso_check` ("
    "   `cc_curs_id` INTEGER NOT NULL,"
    "   `cc_usr_id` INTEGER NOT NULL,"
    "   FOREIGN KEY (`cc_curs_id`) REFERENCES `curso` (`curs_id`),"
    "   FOREIGN KEY (`cc_usr_id`) REFERENCES `user` (`usr_id`)"
    ")")

TABLES['classes'] = (
    "CREATE TABLE `classes` ("
    "   `id` INTEGER NOT NULL AUTO_INCREMENT,"
    "   `a_id` INTEGER NOT NULL,"
    "   `c_a_id` INTEGER NOT NULL,"
    "   `cntnt` TEXT,"
    "   `a_name` TEXT,"
    "   `a_curs_id` INTEGER NOT NULL,"
    "   PRIMARY KEY (`id`),"
    "   FOREIGN KEY (`a_curs_id`) REFERENCES `curso` (`curs_id`)"
    ")")