# Projekt

## Utvecklingsmiljö & Verktyg

Operativsystemet som användes under denna uppgift var Windows 10. Programmeringsspråket är Python,
därför används PyCharm som är ett populärt IDE för Python. Git Bash är nedladdat för att kunna 
hämta och ladda upp filer, där Bitbucket är den versionshanteringsprogram som används.


## Syfte

Syftet med projektet är att skapa Game of Life simulator. Lösningen behöver uppfylla de krav som
anges i projektbeskrivningen och har olika mål beroende på vilket betyg som eftersträvas. I detta
projekt implementerades kraven för att uppnå betyget B, alla dessa krav kommer att presenteras
nedanför och det är specificerat vilka krav som gäller för vilket betyg:

Grundkrav (Betyg E):

* Game of Life skall följa och tillämpa Conways regler:

  * Varje levande cell med färre än två levande grannar dör, som av underbefolkning
  
  * Varje levande cell med två eller tre levande grannar lever vidare till nästa generation
  
  * Varje levande cell med fler än tre levande grannar dör, som av överbefolkning
  
  * Alla döda celler med exakt tre levande grannar blir en levande cell, som om det vore fortplantning.
  
* Världsstorleken ska bestämmas av funktionen `parse_world_size_args()`
och cellbefolkning efter funktionen `populate_world()`.

* Simuleringen skall startas genom att anropa `run_simulation()`

* En validering för världsstorlek skall skapas i funktionen `parse_world_size_args()` och om den 
misslyckas skall standardvärdet 80x40 returneras

* Cellernas status kan bestämmas genom två sätt: om `_seed_pattern` i funktionen `populate_world()`
är annat än None ska de levande
cellerna bestämmas av `get_pattern()`, annars genom randomisering inom intervallet 0-20.
Ifall randomiseringen är större än 16 skall cellen vara vid liv, annars död

Krav betyg D:

* `run_simulation()` skall ha en rekursiv lösning

Krav betyg C:

* Om användaren anger ett filnamn ska både cellpopulationen och världsstorleken att returneras från
funktionen `load_seed_from_file()`. Detta genom att ladda data från lagrade JSON-filer som finns
tillsammans med projektbeskrivningen.

Krav betyg B:

* run_simulation skall enbart returnera befolkningstillståndet av `update_world()`

* En anpassad logger ska skapas av funktionen `create_logger()` som returnerar denna till `simulation_decorator()`.

* Simulationskörningen skall hanteras av `simulation_decorator()` som också loggar statusrapporter.


## Genomförande

Projektet består av att skapa ett program för att simulera spelet Game of Life. Flera funktioner fanns 
fördefinierade där kod skulle implementeras för att få programmet att fungera enligt kraven.

Funktionen `parse_world_size_arg()` tar emot en string som argument där strängen motsvarar världsstorleken som
användaren har fyllt i programmet (eller det som är satt som default). Först splittras strängen vid bokstaven 'x'
och filtrerar None-värden, dessa värden läggs sen till i en lista: `values = list(filter(None, _arg.split('x')))`.
Try-catch block lades till för att skicka felmeddelanden till användaren ifall felaktig data har skrivits in. I
try-blocket kontrollerades först ifall listan innehöll två värden och skickade annars ett AssertionError: `if len(values) != 2:  
raise AssertionError("World size should contain width and height")`. Det kontrollerades också att listan
innehöll två positiva nummer större än 0, annars skickades ett ValueError: `for num in values: if num <= 0:
raise ValueError("Both width and height needs to have positive values")`. Om något av de tidigare inte stämde
och catch-blocket triggades så printades det specifika felmeddelandet ut och `values = [80, 40]` gjorde att
80x40 sattes som standardvärde. Funktionen `parse_world_size_arg` returnerar en tuple med höjd x bredd.

Funktionen `populate_world()` tar emot världsstorleken och eventuell mönster som ska användas. Funktionens uppgift
är att befolka världen med celler och sätta tillstånd på dessa. Först hämtas eventuellt mönster från den andra
fördefinierade klassen med `pattern = cb.get_pattern(_seed_pattern, (_world_size[1], _world_size[0]))`. Bredd x höjd
skickades in istället för tvärtom då det annars var ett problem med att koordinaterna hämtades fel.
Alla celler i världen hämtades genom `coordinates = (tuple(product(height, width)))` där metoden product() hämtar
alla möjliga kombinationer som finns med höjden och bredden. Alla celler kontrolleras sen i en for-loop och för att
få ut alla rim-celler (de celler som kommer att vara i kanterna av världen för att skapa en ram) hämtas genom
`if 0 in cell or cell[0] == _world_size[0]-1 or cell[1] == _world_size[1]-1:`. Rim-cellerna `population[cell] = None`
sätts värdet None. Efter att rim-cellerna är deklarerade kontrolleras det sen om ett mönster finns eller inte:
`if pattern is not None:` och om de cellerna som hämtas från mönstret även finns i världen så sätts dessa till alive
`if cell in pattern: population[cell] = {'state': cb.STATE_ALIVE}`, alla andra celler blir döda `else: population[cell] = {'state': 
cb.STATE_DEAD}`. Ifall ett mönster inte finns så ska cellernas tillstånd randomiseras fram. Först
randomiseras ett nummer mellan 0-20: `random_number = random.randint(0, 20)` och om random_number är över 16 blir 
den cellen vid liv: `if random_number > 16: population[cell] = {'state': cb.STATE_ALIVE}`, annars sätts cellens tillstånd till död.
När alla cellers tillstånd är klara hämtas alla grannar till cellerna genom att anropa en metod som räknar
ut cellers grannar: `neighbours = calc_neighbour_positions(cell)`. I dictionaryn för cellen så läggs dessa grannar in: 
`population[cell]['neighbours'] = neighbours`.
Funktionen returnerar en dictionary innehållande celler, där varje cell som inte är en rim-cell också har två andra 
dictionarys deklarerade innehållande tillstånd och grannar.

Funktionen `calc_neighbour_positions()` tar emot en tuple som argument innehållande koordinater från funktionen
`populate_world()`. Alla möjliga riktningar som koordinaten har deklarerades i en lista 
`coords = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]` och de koordinater som togs emot
som argument tilldelades specifika värden `x, y = _cell_coord`. Granncellerna kunde sedan räknas ut med
`neighbours = {(x + x_add, y + y_add) for x_add, y_add in coords}` och funktionen returnerade en lista med
koordinatens grannar.

`run_simulation()` är en funktion som för krav till betyg E-C hanterade körning av simuleringen för specificerat 
antal generationer. Funktionen tar emot generationer, population och världsstorlek som argument. För betyget E
gick funktionen igenom alla generationer som finns `for i in range(_generations):`, och för varje generation rensades
konsolen `cb.clear_console()`, populationen
hämtades och uppdaterades av funktionen `update_world()` med`_population = update_world(_population, _world_size)`
och en fördröjning med 0.2 sekunder sattes innan exekveringen 
av nästa generation startade: `sleep(0.200)`.
För betyget D fanns kravet att `run_simulation()` skulle ha en rekursiv lösning. Lösningen blev lik betyget E
men istället för att göra en for-loop där varje generation gick igenom så löstes uppgiften med:
`_nth_generation if _nth_generation <= 1 else run_simulation(_nth_generation - 1, _population, _world_size)`
Om generationen var mindre än eller lika med 1 var funktionen klar, men annars kördes funktionen på nytt
där den anropade sig själv och satte generation-1 och därmed tickade ner varje gång den kördes.
För betyg B var kravet att run_simulation enbart skulle returnera befolkningstillståndet av `update_world()` och 
simulatorkörningarna skulle istället hanteras av funktionen `simulation_decorator()`. Detta gjorde
genom `return update_world(_population, _world_size)` och `@simulation_decorator`
skrevs ovanför funktionen `run_simulation` då den metoden skulle köras varje gång run_simulation körs.

`count_alive_neighbours()` är en funktion som tar emot grannar och celler som argument. Funktionens
uppgift är att bestämma hur många av de närliggande cellerna som för närvarande är vid liv.
Detta räknas genom att gå igenom alla grannceller `for i in _neighbours:` och ifall det inte är
en rim-cell och ifall cellernas tillstånd är 'X' (vilket betyder att den är vid liv) 
`if _cells[i] is not None and _cells[i]['state'] == 'X':` så ska en räknare
plussas på med 1 `count +=1`. När alla grannceller är kollade så returneras räknaren som innehåller
antalet grannceller som är vid liv.

Funktionen `update_world()` tar emot en dictionary med den nuvarande generationen och världsstorleken.
Funktionen ska representera ett steg i simuleringen. Varje cell i den nuvarande generationen
gås igenom med `for cell in _cur_gen:` och ifall cellen är None (alltså en rim-cell) så sätts
cellens tillstånd till rim-cell med: `if _cur_gen[cell] is None: _cur_gen[cell] = 
{'state': cb.STATE_RIM}`. Färg och cellens symbol baserat på tillstånd hämtas med
`color = cb.get_print_value(list(_cur_gen[cell].values())[0])`. Detta printas ut med
`cb.progress(f"{color}\n") if cell[1] == _world_size[1]-1 \ else cb.progress(f"{color}")` där
där den även kontrollerar om det är i slutet av en rad då ett radbryt ska infogas.
Rim-cellernas grannar och tillstånd är inget som ändras eller behöver räknas så för att försäkra 
sig om att rim-cellerna
inte inkluderas skrivs: `if '#' not in _cur_gen[cell].values():`. Cellens grannar hämtas
genom att anropa funktionen calc_neighbour_positions `neighbours = calc_neighbour_positions(cell)`
och för att se hur många grannceller som är vid liv anropas funktionen count_alive_neighbours
`count = count_alive_neighbours(neighbours ,_cur_gen)`. Funktionen kontrollerar sen cellen
efter Conways regler och lägger till dessa i en ny lista som ska motsvara den nya generationen.
En cell som är vid liv och har två eller tre grannar ska fortsätta vara
vid liv: `if _cur_gen[cell]['state'] == 'X' and count == 2 or count == 3: next_gen[cell] = 
{'state': 'X'}`. En död cell som har tre grannar ska bli vid liv: `elif _cur_gen[cell]['state'] == '-' and count == 3:
next_gen[cell] = {'state': 'X'}` och annars är det en död cell: `else: next_gen[cell] =
{'state': '-'}`. Funktionen returnerar en lista med cellernas nya tillstånd. De celler som inte
blev inkluderade tidigare får tillståndet rim-cell: `else: next_gen[cell] = 
{'state': cb.STATE_RIM}`

Funktionen `load_seed_from_file()` tar emot en sträng som argument som motsvarar det filnamn
användaren vill hämta mönster ifrån. Användaren ska kunna skriva filnamnet utan att inkludera
.json i slutet, därför kontrolleras först om ".json" finns i filnamnet och om det inte gör det så
läggs det till: 
`_file_name = f"{_file_name}.json" if ".json" not in _file_name else _file_name`
Filen laddas sen in och data hämtas med `data = json.load(file)`. Json-filen innehåller en dictionary
och en list, för att separera och deklarera dessa används en if-sats.
Världsstorleken är deklarerad som en lista i json-filen och den går att hämta genom:
`if isinstance(element, list): world_size = tuple(element)`. Cellerna hämtas på liknande sätt: 
`if isinstance(element, dict):` och där varje cell i dictionaryn gås igenom och sparas som int istället för
string i population tillsammans med cellens värde:
`population.setdefault(ast.literal_eval(key), value)`.
En tuple innehållande population och världsstorlek skapas genom 
`return_value = population, (world_size[1], world_size[0])` vilket sen är det som metoden returnerar.

Funktionen `create_logger()` är en funktion som skapar ett logging objekt som används för att 
skriva ut detaljer om programmets körningar. En logger skapas 
`logger = logging.getLogger('gol_logger')` och sätts till INFO `logger.setLevel(logging.INFO)`.
En filhanterare skapades och filen öppnas med skrivläge:
`file_handler = logging.FileHandler(log_path, mode='w')`. Loggnivå sattes till INFO
`file_handler.setLevel(logging.INFO)` och filhanteraren lades in i logger:
`logger.addHandler(file_handler)`. Funktionen returnerade sen logger.

Funktionen `simulation_decorator()` tar funktionen `run_simulation` som argument och används för att
köra hela simuleringen. En inre funktion skapades som tog emot samma argument som run_simulation,
alltså generation, population och världsstorlek. Först skapades logger genom anrop till 
create_logger funktionen:
`logger = create_logger()`. Sen går funktionen igenom varje generation med
`for i in range(_generation):`. Konsolen rensas med `cb.clear_console()` och varje key + value
i populationen gås igenom med `for key, value in _population.items():`. 
Först kontrolleras att cellen inte är rim-cell genom `if value is not None and value['state'] != '#':`
Om cellens tillstånd är vid liv så blir räknaren för celler som är vid liv + 1: 
`if value['state'] == 'X': count_alive +=1`. Samma kontroll sker för att se om cellen är
död och om den är det så ökar räknaren för döda: 
`if value['state'] == '-': count_dead +=1`. Om cellen är en rim-cell så adderas räknaren för
rim-celler: `count_rim +=1`
I logger printas det sen information om vilken generation det är: 
`logger.info(f"GENERATION {i}")`, hur stor populationen är:
`logger.info(f"  Population: {len(_population) - count_rim}")`, hur många som är vid liv:
`logger.info(f"  Alive: {count_alive}")` och hur många som är döda:
`logger.info(f"  Dead: {count_dead}")`.
Populationen räknas sen ut genom att anropa run_simulation
`_population = func(_generation, _population, _world_size)` och en fördröjning med 
0.2 sekunder sattes innan exekveringen 
av nästa generation startade: `sleep(0.200)`.
Den inre funktionen returnerar sig själv.


## Diskussion

Den implementerade lösningen kan anses vara korrekt och uppfylla laborationens syfte av flera 
orsaker:
Grundkrav (Betyg E):

* Spelet följer och har implementerat Conways regler. Detta kunde kontinuerligt testas
genom att använda breakpoints i funktionen `calc_neighbour_positions` där grannarna till cellerna
blev deklarerade samt i funktionen `update_world` där Conways regler testades. Med breakpoint
kunde koden stegas igenom och därför kunde man följa steg för steg för att försäkra sig om att
koden stämde överens med de kraven som fanns. Vid implementering av mönster gick det också tydligt
att se att koden stämde överens med de förväntade beteendena som mönstret skulle ha, exempel på
mönsters beteende låg ute i Moodle.

* Ett annat krav på programmet var att världsstorleken skulle bestämmas av `parse_world_size_args()`
och cellbefolkningen av `populate_world()`. Detta kunde som med kravet ovan bekräftas genom
att använda breakpoints under utvecklandets gång. `parse_world_size_args()` testades flera gånger
genom att skriva ut både korrekt och felaktig data i terminalen. Det gick att se att exempelvis
80x40 skulle användas vid inmatning av felaktig data då terminalen först skrev ut den varningen samt
genom att räkna storleken som blev på spelet i terminalen. `populate_world()` kontrollerades flera
gånger genom att hämta olika mönster samt användning av randomisering.

* Simuleringen skall startas genom att anropa `run_simulation()`. Detta kunde tydligt ses genom
användning av breakpoint samt genom att analysera koden i funktionen `main()`.

* Ett krav var att validering för världsstorlek skall skapas i funktionen `parse_world_size_args()`
och sättas till 80x40 om den misslyckades. Som tidigare nämnt testades denna funktion flera gånger
genom olika anrop till terminalen. Alla möjliga tester provades för att försäkra sig om att
lösningen inte hade några brister, som att exempelvis använda bokstäver istället för siffror
eller att skicka in ett tal tillsammans med 'x' och inget efter det. Alla tester till terminalen
gjorde att vissa brister fanns med koden vilket åtgärdades under utvecklingens gång.

* Sista grundkravet var att cellernas status kunde beräknas antingen genom att 
`_seed_pattern` returnerar något annat än None och därav hämtar ett mönster eller genom randomisering.
Detta testades flera gånger genom att både skriva olika uppgifter i terminalen samt genom användning
av breakpoint och ändra default-värdena i `main()` funktionen. Då `_seed_pattern` faktiskt returnerar
ett mönster gick det enkelt att se ifall det fungerade korrekt eller inte. Randomiseringen
stegades igenom flera gånger för att se att ett nummer randomiserades mellan 0-20 och att cellen
fick sitt tillstånd baserat på vad siffran blev.

Krav betyg D:

* Kravet för betyg D var att `run_simulation()` skulle ha rekursiv lösning. Det innebär att funktionen
anropar sig själv. Huruvida ett rekursivt anrop ska göras bestäms av värdet för _nth_generation,
därför körs funktionen bara om det är nödvändigt. Detta kunde man kontrollera genom att använda
breakpoint i funktionen för att se om den kördes så många gånger som den blev tillsagd. Det gick
även att testköra programmet visst många generationer för att se om den kördes så många gånger
som förväntat.

Krav betyg C:

* Kravet för betyg C var att om användaren uppger ett existerande filnamn ska cellpopulationen och 
världsstorleken
returneras från `load_seed_from_file()` och inte `parse_world_size_arg` och `populate_world` som
tidigare. Ett annat krav i den funktionen var att användaren inte ska behöva skriva .json efter
filnamnet. Detta testades flera gånger genom att i terminalen skriva in filnamnet med och utan
.json efteråt där båda fungerade klockrent samt att skriva in filnamn som inte existerar, då
blir den randomiserad som tidigare. Det testades också genom att lägga in defaultvärden i `main()`
funktionen under utvecklingens gång. Att json-filerna var korrekta och att metoden hämtade korrekt
data kunde man se genom att köra programmet och kontrollera att mönstren överensstämde de 
exempelmönster som fanns i Moodle.

Krav betyg B:

* Ett krav för betyg B var att funktionen `run_simulation` enbart skulle returnera
befolkningstillståndet av `update_world()`. Detta kunde man utläsa efter att analysera
koden i `run_simulation` men det testades även med breakpoint för att försäkra sig om att det
stämde.

* Ett annat krav var att en logger skulle skapas av funktionen `create_logger()` som skulle
logga statusrapporter från funktionen `simulation_decorator()`. Detta kunde testas
genom att logger hämtades i `simulation_decorator` och sen skriva ut data i den. Det kunde tidigt
i utvecklingen av funktionen märkas att logger var korrekt utformad då den skapades som det var
tänkt och skrev in det data som det var krav på att den skulle innehålla.

Kraven för projektet kan anses vara uppfyllda och metodiken i detta projekt fungerade som det var 
tänkt. Därför behövs inte andra tillvägagångssätt övervägas.
Detta projekt har knutit ihop säcken över hela kursen och de läromoment som har inkluderats.
Något som var svårt med projektet var att förstå helheten och hur alla funktioner är kopplade med
varandra. För att försöka komma runt detta spenderades tid på att läsa sig in och förstå vad metoderna
skulle implementera.

Alla inlärningsmoduler och laborationer inför detta projekt var bra och täckte upp den information
som behövdes för att lösa detta projekt. 
