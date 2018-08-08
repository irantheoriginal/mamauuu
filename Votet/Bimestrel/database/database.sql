-- Usuario
CREATE TABLE Usuario(
  id serial NOT NULL,
  nome varchar(100) NOT NULL,
  email varchar(100) NOT NULL,
  senha varchar(100) NOT NULL,
  CONSTRAINT ref_user PRIMARY KEY(id)
);

-- Publicação
CREATE TABLE Publicacao(
  id serial NOT NULL,
  id_user int,
  autor varchar(100),
  data date,
  conteudo text,
  CONSTRAINT ref_public PRIMARY KEY(id),
  FOREIGN KEY (id_user) REFERENCES Usuario(id)
);