-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 08, 2023 at 09:37 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `chess`
--

-- --------------------------------------------------------

--
-- Table structure for table `scores`
--

CREATE TABLE `scores` (
  `score_id` int(11) NOT NULL,
  `player_name` varchar(30) NOT NULL,
  `tiime_minutes` int(11) NOT NULL,
  `steps_taken` int(11) NOT NULL,
  `level` int(11) NOT NULL,
  `game_timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `scores`
--

INSERT INTO `scores` (`score_id`, `player_name`, `tiime_minutes`, `steps_taken`, `level`, `game_timestamp`) VALUES
(1, 'Ahmed', 132, 23, 1, '2023-03-07 18:40:47'),
(2, 'Ali', 112, 25, 1, '2023-03-07 18:41:22'),
(3, 'Ahmed', 112, 23, 1, '2023-03-08 17:21:09'),
(4, 'Hala', 122, 24, 1, '2023-03-08 17:25:38'),
(5, 'unKnown GM', 0, 0, 3, '2023-03-08 18:19:02'),
(6, 'king GM', 0, 0, 2, '2023-03-08 18:19:49');

-- --------------------------------------------------------

--
-- Table structure for table `themes`
--

CREATE TABLE `themes` (
  `theme_name` varchar(20) NOT NULL,
  `theme_pieces_path` varchar(50) NOT NULL,
  `colorA_bg` varchar(20) NOT NULL,
  `colorB_bg` varchar(20) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `themes`
--

INSERT INTO `themes` (`theme_name`, `theme_pieces_path`, `colorA_bg`, `colorB_bg`, `status`) VALUES
('theme1', 'images/1/', 'khaki1', 'red4', 0),
('theme2', 'images/2/', 'white', 'seagreen1', 1),
('theme3', 'images/3/', 'white', 'gray', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `scores`
--
ALTER TABLE `scores`
  ADD PRIMARY KEY (`score_id`);

--
-- Indexes for table `themes`
--
ALTER TABLE `themes`
  ADD PRIMARY KEY (`theme_name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `scores`
--
ALTER TABLE `scores`
  MODIFY `score_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
