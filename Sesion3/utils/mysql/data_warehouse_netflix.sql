#creamos la base de datos para el modelo multidimensional
CREATE DATABASE dw_netflix;

##usamos la base de datos creada
USE dw_netflix;


/*creamos la tabla de dimMovie*/
CREATE TABLE dimMovie (
	movieID VARCHAR(8) PRIMARY KEY,
    title VARCHAR (100),
    releaseMovie DATE,
    gender VARCHAR(100),
    participantName VARCHAR(100),
    roleparticipant VARCHAR (100),
    awardMovie VARCHAR (20)
);


/*creamos la tabla de dimUser*/
CREATE TABLE dimUser (
	userID INTEGER PRIMARY KEY,
    username varchar (100),
    country varchar (100),
    subscription varchar (100)
);


/*creamos la tabla de FactVentas*/
CREATE TABLE FactWatchs (

	userID INTEGER,
    movieID VARCHAR(8),
    rating DECIMAL(2,1),
    timestamp  timestamp,
    
    /* CREANDO LAS REALACIONES*/
    CONSTRAINT fk_factwatchs_movie FOREIGN KEY (movieID) REFERENCES dimMovie (movieID),
	CONSTRAINT fk_factwatchs_user FOREIGN KEY (userID) REFERENCES dimUser (userID)

);