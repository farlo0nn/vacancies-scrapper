
-- INDEXES

create index idx_users_category_user_id on users_category_association(user_id);
create index idx_users_contract_types_user_id on users_contract_types_association(user_id);
create index idx_users_location_user_id on users_location_association(user_id);
create index idx_users_position_level_user_id on users_position_level_association(user_id);
create index idx_users_subcategory_user_id on users_subcategory_association(user_id);
create index idx_users_work_model_user_id on users_work_model_association(user_id);
create index idx_users_work_schedule_user_id on users_work_schedule_association(user_id);

create index idx_vacancies_subcategory_id on vacancies(subcategory_id);

create index idx_vacancies_contract_types_gin on vacancies using gin (contract_types);
create index idx_vacancies_workplaces_gin on vacancies using gin (workplaces);
create index idx_vacancies_work_models_gin on vacancies using gin (work_models);
create index idx_vacancies_work_schedules_types_gin on vacancies using gin (work_schedules);
create index idx_vacancies_position_levels_gin on vacancies using gin (position_levels);



-- POSITION LEVELS
insert into position_level values(1, 'praktykant / stażysta');
insert into position_level values(2, 'asystent');
insert into position_level values(3, 'młodszy specjalista (Junior)');
insert into position_level values(4, 'specjalista (Mid / Regular)');
insert into position_level values(5, 'starszy specjalista (Senior)');
insert into position_level values(6, 'ekspert');
insert into position_level values(7, 'menedżer');
insert into position_level values(8, 'dyrektor');
insert into position_level values(9, 'kierownik / koordynator');
insert into position_level values(10, 'prezes');
insert into position_level values(11, 'pracownik fizyczny');


-- CATEGORIES
insert into categories values (1, 'Administracja biurowa');
insert into categories values (2, 'Badania i rozwój');
insert into categories values (3, 'Bankowość');
insert into categories values (4, 'BHP / Ochrona środowiska');
insert into categories values (5, 'Budownictwo');
insert into categories values (6, 'Call Center');
insert into categories values (7, 'Doradztwo / Konsulting');
insert into categories values (8, 'Energetyka');
insert into categories values (9, 'Edukacja / Szkolenia');
insert into categories values (10, 'Finanse / Ekonomia');
insert into categories values (11, 'Franczyza / Własny Biznes');
insert into categories values (12, 'Hotelarstwo / Gastronomia / Turystyka');
insert into categories values (13, 'Human Resources / Zacoby ludzkie');
insert into categories values (14, 'Internet / e-Commerce / Nowe media');
insert into categories values (15, 'Inżyneria');
insert into categories values (16, 'IT - Administracja');
insert into categories values (17, 'IT - Rozwój opgrogramowania');
insert into categories values (18, 'Kontrola jakości');
insert into categories values (19, 'Łańcuch dostaw');
insert into categories values (20, 'Marketing');
insert into categories values (21, 'Media / Sztuka / Rozrywka');
insert into categories values (22, 'Nieruchomości');
insert into categories values (23, 'Obsługa klienta');
insert into categories values (24, 'Praca fizyczna');
insert into categories values (25, 'Prawo');
insert into categories values (26, 'Produkcja');
insert into categories values (27, 'Public Relations');
insert into categories values (28, 'Reklama / Grafika / Kreacja / Fotografia');
insert into categories values (29, 'Sektor publiczny');
insert into categories values (30, 'Sprzedaż');
insert into categories values (31, 'Transport / Spedycja / Logistyka');
insert into categories values (32, 'Ubezpieczenia');
insert into categories values (33, 'Zakupy');
insert into categories values (34, 'Zdrowie / Uroda / Rekreacja');
insert into categories values (35, 'Inne');


-- CONTRACT TYPES
insert into contract_type values (1, 'umowa o pracę');
insert into contract_type values (2, 'umowa o dzielo');
insert into contract_type values (3, 'umowa zlecenie');
insert into contract_type values (4, 'kontrakt B2B');
insert into contract_type values (5, 'umowa na zastępstwo');
insert into contract_type values (6, 'umowa agencyjna');
insert into contract_type values (7, 'umowa o pracę tymczasową');
insert into contract_type values (8, 'umowa o staź / praktyki');


-- WORK SCHEDULES
insert into work_schedule values (1, 'część etatu');
insert into work_schedule values (2, 'dodatkowa / tymczasowa');
insert into work_schedule values (3, 'pełny etat');


-- WORK MODELS 
insert into work_model values (1, 'praca stacjonarna');
insert into work_model values (2, 'praca hybrydowa');
insert into work_model values (3, 'praca zdalna');
insert into work_model values (4, 'praca mobilna');

-- SUBCATEGORIES
insert into subcategories values (1, 'Sekretariat / Recepcja', 1);
insert into subcategories values (2, 'Stanowiska asystenckie', 1);
insert into subcategories values (3, 'Tłumaczenia / Korekta', 1);
insert into subcategories values (4, 'Wprowadzanie / Przetwarzanie danych', 1);
insert into subcategories values (5, 'Wsparcie administracyjne', 1);
insert into subcategories values (6, 'Zarządzanie biurem i administracją', 1);

insert into subcategories values (7, 'Business Intelligence / Data Warehouse', 2);
insert into subcategories values (8, 'Chemia przemysłowa', 2);
insert into subcategories values (9, 'Farmaceutyka / Biotechnologia', 2);
insert into subcategories values (10, 'FMCG', 2);
insert into subcategories values (11, 'Tworzywa sztuczne', 2);

insert into subcategories values (12, 'Analiza / Ryzyko', 3);
insert into subcategories values (13, 'Bankowość detaliczna', 3);
insert into subcategories values (14, 'Bankowość inwestycyjna', 3);
insert into subcategories values (15, 'Bankowość korporacyjna / SME', 3);
insert into subcategories values (16, 'Pośrednictwo finansowe', 3);

insert into subcategories values (17, 'Inżynieria', 4);
insert into subcategories values (18, 'Nadzór', 4);
insert into subcategories values (19, 'Specjaliści / Konsultanci', 4);

insert into subcategories values (20, 'Architektura / Projektowanie', 5);
insert into subcategories values (21, 'Ekologiczne', 5);
insert into subcategories values (22, 'Energetyczne', 5);
insert into subcategories values (23, 'Infrastrukturalne', 5);
insert into subcategories values (24, 'Instalacje', 5);
insert into subcategories values (25, 'Mieszkaniowe / Przemysłowe', 5);

insert into subcategories values (26, 'Przychodzące', 6);
insert into subcategories values (27, 'Wychodzące', 6);

insert into subcategories values (28, 'Finanse', 7);
insert into subcategories values (29, 'Podatki / prawo', 7);
insert into subcategories values (30, 'Sektor publiczny', 7);
insert into subcategories values (31, 'IT/Telekomunikacja', 7);
insert into subcategories values (32, 'Biznes/Strategia', 7);

insert into subcategories values (33, 'Budownictwo', 8);
insert into subcategories values (34, 'Konwencjonalna', 8);
insert into subcategories values (35, 'Nafta i gaz', 8);
insert into subcategories values (36, 'Odnawialna', 8);

insert into subcategories values (37, 'Nauka języków obcych', 9);
insert into subcategories values (38, 'Szkolenia / Rozwój osobisty', 9);
insert into subcategories values (39, 'Szkolnictwo', 9);

insert into subcategories values (40, 'Audyt / Podatki', 10);
insert into subcategories values (41, 'Doradztwo / Konsulsting', 10);
insert into subcategories values (42, 'Kontroling', 10);
insert into subcategories values (43, 'Księgowość', 10);
insert into subcategories values (44, 'Rynki Kapitałowe', 10);
insert into subcategories values (45, 'Analiza', 10);


-- LOCATIONS 
insert into location values (1, 'Warszawa');
insert into location values (2, 'Wrocław');
insert into location values (3, 'Kraków');
insert into location values (4, 'Szczecin');
insert into location values (5, 'Gdańsk');
insert into location values (6, 'Poznań');
insert into location values (7, 'Łódż');
insert into location values (8, 'Bydgoszcz');
insert into location values (9, 'Katowice');
insert into location values (10, 'Gdynia');
insert into location values (11, 'Radom');
insert into location values (12, 'Białystok');
insert into location values (13, 'Częstochowa');
insert into location values (14, 'Kielce');
insert into location values (15, 'Lublin');
insert into location values (16, 'Olsztyn');
insert into location values (17, 'Wałbrzych');
