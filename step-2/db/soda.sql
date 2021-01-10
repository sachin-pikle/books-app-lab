-- https://oracle-base.com/articles/misc/sqlcl-soda-integration

soda list collection

-- soda drop books
soda create books

soda insert books { "isbn": "1", "title": "Java - The Complete Reference", "author": "Herbert Schildt" } 
soda insert books { "isbn": "2", "title": "Effective Java", "author": "Joshua Bloch" } 
soda insert books { "isbn": "3", "title": "Learning Python", "author": "Mark Lutz" } 
soda insert books { "isbn": "4", "title": "JavaScript: The Definitive Guide", "author": "David Flanagan" }
soda insert books { "isbn": "5", "title": "Oracle SOA Suite 12c Handbook", "author": "Lucas Jellema" }
soda insert books { "isbn": "6", "title": "Programming with Java | 6th Edition", "author": "E Balagurusamy" } 
soda insert books { "isbn": "7", "title": "Java - A Beginner’s Guide", "author": "Herbert Schildt" } 
soda insert books { "isbn": "8", "title": "Java 8 in Action", "author": "Raoul-Gabriel Urma, Mario Fusco, et al." } 
soda insert books { "isbn": "9", "title": "Core Python Programming", "author": "R. Nageswara Rao" }
soda insert books { "isbn": "10", "title": "Learning with Python", "author": "Allen Downey , Jeffrey Elkner, et al." }

soda get books -all

-- soda get books -klist "EC831D913E454478B9B20371E3A5EC31"

soda get books -f {"isbn": "13"}



-- 	KEY						Created On

-- 	2106C12646E24835BC24727D5535C24C		2021-01-08T06:39:01.398011000Z
-- 	D23974E212F24DFF8A66B55C71113BB3		2021-01-08T06:31:13.015584000Z
-- 	14A4B800FB134853B42B845EF87DEB5C		2021-01-08T06:31:13.015584000Z
-- 	238D3E7FFF6348B58D1C95AB9B14D378		2021-01-08T06:31:13.015584000Z
-- 	66A144B51849430FBA2EBF3FF7B222AC		2021-01-08T06:31:13.015584000Z
-- 	2C9A5B9811D84067856F8F828BACBCAF		2021-01-08T06:31:13.015584000Z

--  6 rows selected. 
