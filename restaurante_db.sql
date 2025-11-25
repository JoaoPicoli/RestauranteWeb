-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 25/11/2025 às 11:17
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `restaurante_db`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `clientes`
--

CREATE TABLE `clientes` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `nome` varchar(120) NOT NULL,
  `contato` varchar(120) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Despejando dados para a tabela `clientes`
--

INSERT INTO `clientes` (`id`, `user_id`, `nome`, `contato`) VALUES
(1, 1, 'Cliente 1', '(41) 99999-0001'),
(2, 4, 'João Paulo da Silva Picoli', '41999529902'),
(3, 2, 'atendente1', NULL),
(4, 3, 'LuizaADM', NULL);

-- --------------------------------------------------------

--
-- Estrutura para tabela `comandas`
--

CREATE TABLE `comandas` (
  `id` int(11) NOT NULL,
  `codigo` int(11) NOT NULL,
  `cliente_id` int(11) DEFAULT NULL,
  `mesa` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `closed_at` datetime DEFAULT NULL,
  `paid_at` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `closed_by` int(11) DEFAULT NULL,
  `paid_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Despejando dados para a tabela `comandas`
--

INSERT INTO `comandas` (`id`, `codigo`, `cliente_id`, `mesa`, `status`, `created_at`, `closed_at`, `paid_at`, `created_by`, `closed_by`, `paid_by`) VALUES
(22, 1, NULL, NULL, 'aberta', '2025-11-25 09:36:06', NULL, NULL, 3, NULL, NULL),
(23, 2, NULL, NULL, 'aberta', '2025-11-25 09:36:16', NULL, NULL, 3, NULL, NULL),
(24, 3, NULL, NULL, 'aberta', '2025-11-25 09:39:05', NULL, NULL, 3, NULL, NULL);

-- --------------------------------------------------------

--
-- Estrutura para tabela `funcionarios`
--

CREATE TABLE `funcionarios` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `nome` varchar(120) NOT NULL,
  `cargo` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Despejando dados para a tabela `funcionarios`
--

INSERT INTO `funcionarios` (`id`, `user_id`, `nome`, `cargo`) VALUES
(1, 2, 'Atendente 1', 'Atendente');

-- --------------------------------------------------------

--
-- Estrutura para tabela `itens_cardapio`
--

CREATE TABLE `itens_cardapio` (
  `id` int(11) NOT NULL,
  `nome` varchar(200) NOT NULL,
  `descricao` text DEFAULT NULL,
  `preco` decimal(10,2) NOT NULL,
  `disponivel` tinyint(1) DEFAULT NULL,
  `categoria` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Despejando dados para a tabela `itens_cardapio`
--

INSERT INTO `itens_cardapio` (`id`, `nome`, `descricao`, `preco`, `disponivel`, `categoria`) VALUES
(4, 'Morango do Amor', 'Morango coberto com chocolate e confeitos coloridos, uma explosão de fofura e sabor.', 12.50, 1, 'Sobremesa'),
(5, 'Dubai Chocolate', 'Delicioso chocolate cremoso servido com chantilly e lascas de amêndoas.', 15.00, 1, 'Sobremesa'),
(6, 'Sorvete de Pistache', 'Sorvete artesanal de pistache, cremoso e refrescante.', 10.00, 1, 'Sobremesa'),
(7, 'Bibimbap', 'Tradicional prato coreano com arroz, vegetais variados, ovo e molho picante.', 28.00, 1, 'Prato Principal'),
(8, 'Kimchi', 'Clássico acompanhamento coreano de repolho fermentado picante.', 8.00, 1, 'Acompanhamento'),
(9, 'Tteokbokki', 'Bolinhos de arroz cozidos em molho picante e doce, irresistível e divertido.', 18.50, 1, 'Lanche'),
(10, 'Chá de Flor de Cerejeira', 'Bebida delicada, floral e levemente adocicada.', 9.50, 1, 'Bebida'),
(11, 'Soju de Melancia', 'Bebida alcoólica coreana sabor melancia, refrescante e doce.', 22.00, 1, 'Bebida'),
(12, 'Dorayaki de Feijão Vermelho', 'Panquecas japonesas recheadas com pasta de feijão vermelho, fofinhas e doces.', 7.50, 1, 'Sobremesa'),
(13, 'Frappuccino Coreano', 'Bebida gelada com café, leite e cobertura de chantilly, divertida e colorida.', 14.00, 1, 'Bebida');

-- --------------------------------------------------------

--
-- Estrutura para tabela `itens_comanda`
--

CREATE TABLE `itens_comanda` (
  `id` int(11) NOT NULL,
  `comanda_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `quantidade` int(11) NOT NULL,
  `preco_unitario` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `pagamentos`
--

CREATE TABLE `pagamentos` (
  `id` int(11) NOT NULL,
  `comanda_id` int(11) NOT NULL,
  `forma` varchar(50) NOT NULL,
  `valor_recebido` decimal(10,2) NOT NULL,
  `troco` decimal(10,2) NOT NULL,
  `paid_at` datetime DEFAULT NULL,
  `paid_by` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Despejando dados para a tabela `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `role`, `created_at`) VALUES
(1, 'cliente1', 'cliente1@example.com', 'scrypt:32768:8:1$LfIBbidgILUM0gsQ$643a0301b6f00dced8145b3061a97914fa52239c06940ce2b6eba05616b73f56d2a9eb1cf47bab91bf036556537b16f364d79aa1d2cefb67876219c969ac2e93', 'cliente', '2025-11-25 00:03:00'),
(2, 'atendente1', 'atendente1@example.com', 'scrypt:32768:8:1$5UDhQmsmnC4IENZk$00e432d58954be559311070fcbf872e0b84596b65fdd314ccb6d1903055db0a1b1e7bad4d2bc788947240ec78c9af59a65ed352fb1af7e0790314837eadd5ce5', 'atendente', '2025-11-25 00:03:01'),
(3, 'LuizaADM', 'luiza@examplo.com', 'scrypt:32768:8:1$oMBbbzdY7k72fZFH$e4722199ebd4708fa851222a494986f1e5b818950bd985433668aa5baee70793f9a05d224d8b8940639ed2778ac7f8dc98db7678b12f1e0c6622bc3be249228a', 'admin', '2025-11-25 00:03:01'),
(4, 'joao', 'joaopicoli27@gmail.com', 'scrypt:32768:8:1$dy7i9ET7lFPlMSSe$72c73f76c8df6156210c22c1e5556e32b9e83d175b3fccc500137a5902bf563bc42523b32463565927ed7311d886129a34e374cc7e9d116666d09417c38744ca', 'cliente', '2025-11-25 02:08:14');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Índices de tabela `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Índices de tabela `comandas`
--
ALTER TABLE `comandas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo` (`codigo`),
  ADD UNIQUE KEY `codigo_2` (`codigo`),
  ADD UNIQUE KEY `codigo_3` (`codigo`),
  ADD KEY `cliente_id` (`cliente_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `closed_by` (`closed_by`),
  ADD KEY `paid_by` (`paid_by`);

--
-- Índices de tabela `funcionarios`
--
ALTER TABLE `funcionarios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Índices de tabela `itens_cardapio`
--
ALTER TABLE `itens_cardapio`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `itens_comanda`
--
ALTER TABLE `itens_comanda`
  ADD PRIMARY KEY (`id`),
  ADD KEY `comanda_id` (`comanda_id`),
  ADD KEY `item_id` (`item_id`);

--
-- Índices de tabela `pagamentos`
--
ALTER TABLE `pagamentos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `comanda_id` (`comanda_id`),
  ADD KEY `paid_by` (`paid_by`);

--
-- Índices de tabela `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de tabela `comandas`
--
ALTER TABLE `comandas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de tabela `funcionarios`
--
ALTER TABLE `funcionarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `itens_cardapio`
--
ALTER TABLE `itens_cardapio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de tabela `itens_comanda`
--
ALTER TABLE `itens_comanda`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de tabela `pagamentos`
--
ALTER TABLE `pagamentos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `clientes`
--
ALTER TABLE `clientes`
  ADD CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Restrições para tabelas `comandas`
--
ALTER TABLE `comandas`
  ADD CONSTRAINT `comandas_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `comandas_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `comandas_ibfk_3` FOREIGN KEY (`closed_by`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `comandas_ibfk_4` FOREIGN KEY (`paid_by`) REFERENCES `users` (`id`);

--
-- Restrições para tabelas `funcionarios`
--
ALTER TABLE `funcionarios`
  ADD CONSTRAINT `funcionarios_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Restrições para tabelas `itens_comanda`
--
ALTER TABLE `itens_comanda`
  ADD CONSTRAINT `itens_comanda_ibfk_1` FOREIGN KEY (`comanda_id`) REFERENCES `comandas` (`id`),
  ADD CONSTRAINT `itens_comanda_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `itens_cardapio` (`id`);

--
-- Restrições para tabelas `pagamentos`
--
ALTER TABLE `pagamentos`
  ADD CONSTRAINT `pagamentos_ibfk_1` FOREIGN KEY (`comanda_id`) REFERENCES `comandas` (`id`),
  ADD CONSTRAINT `pagamentos_ibfk_2` FOREIGN KEY (`paid_by`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
