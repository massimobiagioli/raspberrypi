/* User */
drop table if exists users;
create table users (
	id integer primary key autoincrement,
	username string not null,
	password string not null,
	fullname string not null,
	isadmin bool not null default 0 
);

/* DeviceType */
drop table if exists device_types;
create table device_types (
	id integer primary key autoincrement,
	name string not null	
);


/* Data */
insert into users values (1, "admin", "AxEKEREKRRE=", "Amministratore Sistema", 1);
insert into users values (2, "unit", "BBlUBlI=", "Utilizzatore", 0);

insert into device_types values (1, "Arduino UNO rev.3");
insert into device_types values (2, "KMtronic 4 channel usb relay board");