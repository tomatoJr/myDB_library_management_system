create database myDB;

use myDB;

create table Student(Student_id int, name varchar(255) not null, Dept varchar(255) not null, gender varchar(1) not null, email varchar(255) not null, check(gender='F' or gender='M'), primary key(Student_id));

create table Faculty(Faculty_id int, name varchar(255) not null, Dept varchar(255) not null, gender varchar(1) not null,email varchar(255) not null,check(gender='F' or gender='M'),primary key(Faculty_id));

create table Book(Book_id int,isbn long not null,title varchar(255) not null,author varchar(255) not null, status varchar(255) not null,primary key(Book_id));

create table Student_Rent_Books(Student_id int,Book_id int,borrow_date timestamp not null,due_date timestamp,return_date timestamp,primary key(Student_id, Book_id, borrow_date),foreign key(Student_id) references Student(Student_id)  ON DELETE CASCADE ON UPDATE CASCADE,foreign key(Book_id) references Book(Book_id) on delete cascade on update cascade);

create table Faculty_Rent_Books(Faculty_id int, Book_id int, borrow_date timestamp not null, due_date timestamp ,  return_date timestamp, primary key(Faculty_id, Book_id, borrow_date), foreign key(Faculty_id) references Faculty(Faculty_id)  ON DELETE CASCADE ON UPDATE CASCADE, foreign key(Book_id) references Book(Book_id) on delete cascade on update cascade);

create table Student_Fine_History(Fine_id int NOT NULL auto_increment,Student_id int,Book_id int,due_date timestamp not null,return_date timestamp not null,amount int not null,status varchar(255) not null,primary key(Fine_id),foreign key(Student_id) references Student(Student_id) on delete cascade on update cascade,foreign key(Book_id) references Book(Book_id) on delete cascade on update cascade);

create table Faculty_Fine_History(Fine_id int NOT NULL auto_increment,Faculty_id int,Book_id int,due_date timestamp not null,return_date timestamp not null,amount int not null,status varchar(255) not null,primary key(Fine_id),foreign key(Faculty_id) references Faculty(Faculty_id) on delete cascade on update cascade,foreign key(Book_id) references Book(Book_id) on delete cascade on update cascade);