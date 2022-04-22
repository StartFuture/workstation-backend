
CREATE DATABASE workstation IF NOT EXISTS;

USE workstation;

-- workstation.endereco definition
CREATE TABLE `endereco` (
  `id_endereco` int NOT NULL AUTO_INCREMENT,
  `cep` varchar(10) DEFAULT NULL,
  `rua` varchar(30) DEFAULT NULL,
  `numero` int DEFAULT NULL,
  `complemento` text,
  `bairro` varchar(30) DEFAULT NULL,
  `cidade` varchar(30) DEFAULT NULL,
  `estado` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id_endereco`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;


-- workstation.mobilia definition

CREATE TABLE `mobilia` (
  `id_mobilia` int(11) NOT NULL AUTO_INCREMENT,
  `tipo_mobilia` varchar(50) DEFAULT NULL,
  `nome_mobilia` varchar(50) DEFAULT NULL,
  `box_id` int(11) DEFAULT NULL,
  `quantidade` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_mobilia`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- workstation.recurso definition

CREATE TABLE `recurso` (
  `id_recurso` int(11) NOT NULL AUTO_INCREMENT,
  `tipo_recurso` varchar(50) DEFAULT NULL,
  `nome_recurso` varchar(50) DEFAULT NULL,
  `box_id` int(11) DEFAULT NULL,
  `quantidade` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_recurso`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- workstation.usuarios definition

CREATE TABLE `usuarios` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) DEFAULT NULL,
  `sobrenome` varchar(50) DEFAULT NULL,
  `sexo` varchar(45) DEFAULT NULL,
  `data_nascimento` date DEFAULT NULL,
  `telefone` varchar(25) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `senha` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id_user`),
  UNIQUE KEY `telefone_UNIQUE` (`telefone`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;


-- workstation.box definition

CREATE TABLE `box` (
  `id_box` int(11) NOT NULL AUTO_INCREMENT,
  `id_endereco` int(11) DEFAULT NULL,
  `nome` varchar(30) DEFAULT NULL,
  `preco_hora` double DEFAULT NULL,
  `descricao` text,
  `ativo` enum('Y','N') DEFAULT NULL,
  `largura` double DEFAULT NULL,
  `altura` double DEFAULT NULL,
  `comprimento` double DEFAULT NULL,
  PRIMARY KEY (`id_box`),
  KEY `id_endereco` (`id_endereco`),
  CONSTRAINT `box_ibfk_1` FOREIGN KEY (`id_endereco`) REFERENCES `endereco` (`id_endereco`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


-- workstation.info_user_cnpj definition

CREATE TABLE `info_user_cnpj` (
  `id_cnpj` int(11) NOT NULL AUTO_INCREMENT,
  `cnpj` varchar(30) DEFAULT NULL,
  `id_user` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_cnpj`),
  UNIQUE KEY `cnpj_UNIQUE` (`cnpj`),
  KEY `id_user_idx` (`id_user`),
  CONSTRAINT `id_user` FOREIGN KEY (`id_user`) REFERENCES `usuarios` (`id_user`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- workstation.info_user_cpf definition

CREATE TABLE `info_user_cpf` (
  `id_cpf` int(11) NOT NULL AUTO_INCREMENT,
  `cpf` varchar(200) DEFAULT NULL,
  `id_user` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_cpf`),
  UNIQUE KEY `cpf_UNIQUE` (`cpf`),
  KEY `id_user` (`id_user`),
  CONSTRAINT `info_user_cpf_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `usuarios` (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;


-- workstation.locacao definition

CREATE TABLE `locacao` (
  `id_locacao` int(11) NOT NULL AUTO_INCREMENT,
  `datainicio` date DEFAULT NULL,
  `horainicio` time DEFAULT NULL,
  `horafim` time DEFAULT NULL,
  `datafim` date DEFAULT NULL,
  `id_user` int(11) DEFAULT NULL,
  `id_box` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_locacao`),
  KEY `id_user` (`id_user`),
  KEY `id_box` (`id_box`),
  CONSTRAINT `locacao_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `usuarios` (`id_user`),
  CONSTRAINT `locacao_ibfk_2` FOREIGN KEY (`id_box`) REFERENCES `box` (`id_box`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;