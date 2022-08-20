-- Run first the ddl script to create the tables
-- Run this script to insert some sample data into the tables

INSERT INTO workstation.endereco (cep,rua,numero,complemento,bairro,cidade,estado) VALUES
	 ('01452000','Avenida Brigadeiro Faria Lima',2705,'próximo ao museu','Jardim Paulistano','São Paulo','SP'),
	 ('30160000','Praça Rui Barbosa',600,'ao lado do hospital','Centro','Belo Horizonte','MG'),
	 ('05005001','Rua Turiassu',147,'predio b','Perdizes','São Paulo','SP'),
	 ('06093010','Avenida Marechal Rondon',260,'2 andar','Centro','Osasco','SP'),
	 ('01311923','Avenida Paulista',1313,'proximo a lanchonete x','Bela Vista','São Paulo','SP');


INSERT INTO workstation.box (id_endereco,nome,preco_hora,descricao,ativo,largura,altura,comprimento,`zone`) VALUES
	 (0,'Espaço Faria Lima',100.0,'Muito mais que uma sala de reunião, um espaço para fechar negócios importantes e ter grandes ideias. Capacidade para até 12 pessoas.',1,121.0,111.0,131.0,'Leste'),
	 (1,'Espaço BH',100.0,'Muito mais que uma sala de reunião, um espaço para fechar negócios importantes e ter grandes ideias. Capacidade para até 12 pessoas.',1,221.0,211.0,231.0,'Leste'),
	 (2,'Espaço Bourbom',100.0,'Muito mais que uma sala de reunião, um espaço para fechar negócios importantes e ter grandes ideias. Capacidade para até 12 pessoas.',1,321.0,311.0,331.0,'Oeste'),
	 (3,'Espaço Biblioteca de Osasco',100.0,'Muito mais que uma sala de reunião, um espaço para fechar negócios importantes e ter grandes ideias. Capacidade para até 12 pessoas.',1,421.0,411.0,431.0,'Oeste'),
	 (4,'Espaço Paulista',200.0,'Muito mais que uma sala de reunião, um espaço para fechar negócios importantes e ter grandes ideias. Capacidade para até 12 pessoas.',1,521.0,511.0,531.0,'Oeste');


