# Laboration 3

## Utvecklingsmiljö & Verktyg

Operativsystemet som användes under denna uppgift var Windows 10. Programmeringsspråket är Python,
därför används PyCharm som är ett populärt IDE för Python. Git Bash är nedladdat för att kunna 
hämta och ladda upp filer, där Bitbucket är den versionshanteringsprogram som används.


## Syfte

Syftet med laboration 3 var att konstruera en lösning för att jämföra olika Fibonacci-sekvenser
med varandra. En iterativ och rekursiv lösning var fördefinierad och en tredje lösning ska
implementeras, baserat på den rekursiva lösningen men där resultatet lagras i en dictionary för
att påskynda beräkningarna. Lösningen behöver uppfylla krav som anges i laborationsbeskrivningen
och är beroende av att uppnå följande mål:
- Den tredje lösningen skall vara en rekursiv lösning och som behåller minnet av beräknade sekvenser
- Dessa tre Fibonacci-funktioner skall utökas med en enda decorator som ska beräkna körtiden samt 
kommunicera med en anpassad logger
- Statistikinformation ska köra mätningar och skriva ut dessa i terminalen.
- Motsvarande filer för Fibonacci-funktionerna ska skapas som innehåller beräknande värden

## Genomförande

Laborationens uppgift i stort består av att skapa ett program som kan mäta körtiden för
Fibonacci sekvensberäkningar med tre olika tillvägagångssätt. Två av dessa var redan definierad och
den sista skulle implementeras med en variation av `rekursion` som behåller ett minne av de beräknade
sekvenserna vilket påskyndar exekveringstiden. Dessa tre tillvägagångssätt skulle också utökas med en
enda `decorator` som kör tidmätningar på de tre olika tillvägagångssätten och presenterar viss
resultat i en logg.

Funktionen `fibonacci_memory` tar emot ett argument innehållande ett heltalstyp och returnerar
samma datatyp. Funktionen går ut på att skapa en effektiv rekursiv implementering genom att lagra
redan beräknande värden för enkel åtkomst i senare iterationer. Logiken skulle likna en av de andra
sekvensberäkningarna som var definierad på förhand. En `dictionary` med fördeklarerade värden skapades för att
undvika `RecursionError` och har därför redan startvärden för Fibonacci-sekvensen 0 och 1. 
En inre funktion skapades då kravet var att lösningen skulle innebära en förbättring av 
rekursiv implementering. I funktionen kontrolleras först om Fibonacci-numret för det aktuella ingångsvärdet (30 är 
standardvärdet) inte
finns i dictionary, detta genom `if _n not in memory:`. Om ingångsvärdet inte finns som
Fibonacci-tal i dictionary så beräknas det genom att anropa metoden fib() rekursivt och uppdatera cachen 
`memory[_n] = fib(_n - 1) + fib(_n - 2)`, värdet adderas då även in i dictionary. Det sista som sker är att 
funktionen returnerar det begärda Fibonacci-numret.

Funktionen `create_logger` användes för att skapa en anpassad logger för att mata ut information under hela
mätningen. Kraven var att loggers namn måste vara ass_3_logger och den måste konfigureras med två hanterare, en
för att skicka meddelanden till konsolen (INFO) och den andra för filutdata (DEBUG). Logger kunde antingen skapas
manuellt eller genom att använda den befintliga konfigurationsfilen, det sistnämnda valde jag att göra då
konfigurationsfilen redan innehöll den data som var nödvändig. Först deklarerades den korrekta filvägen till 
konfigurationsfilen genom `file_path = RESOURCES / 'ass3_log_conf.json'` där RESOURCES var en fördeklarerad
variabel till mappen _Resources. Konfigurationsfilen kunde då öppnas genom `with open(file_path, 'r') as file:`
och det var då möjligt att skapa en logger för jsonfilen och hämta konfigurationen från den filen. Ett objekt
skapades genom `logger = logging.getLogger('ass_3_logger')` vilket även var det funktionen returnerade.

Varje Fibonacci-funktion är dekorerad med `measurements_decorator`, vilket är den metod som ansvarar för att mäta
exekveringstiden och trigga loggning av information. Funktionen innehöll en inre funktion som gås igenom för varje
Fibonacci-funktion, denna funktion tog emot ingångsvärdet som argument. I den inre funktionen skapades först en 
tom lista vilket senare skulle få värdet av
Fibonacci. För att mäta exekveringstiden för varje Fibonacci-funktion så skrevs `start = timeit.default_timer()`
vilket startar en timer för programmet. `for i in reversed(range(nth_nmb +1)):` gjorde att varje värde av
ingångsvärdet gicks igenom där iterationen gick i omvänd ordning för att starta med det högsta talet.
`result = func(i)` hämtade Fibonacci värdet från metoden för det ingångsvärde som var aktuellt. Detta Fibonacci
värde lades till i en lista och för var 5e iteration presenterades data i loggern, detta kontrollerades genom att
se om talet var delbart med 5: `if i % 5 == 0: 
LOGGER.debug('%s: %s', i, result)` Efter att alla Fibonacci-värden var hämtade räknades exekveringstiden ut genom
`duration = timeit.default_timer() - start` där duration innehåller den aktuella tiden minus starttiden. Denna
returnerades tillsammans med listan som blev omvandlad till en tuple.

Funktionen `print_stats` ansvarar för att skriva ut statistikinformation om hur lång tid exekveringstiden tog för
de olika Fibonacci-funktionerna. Funktionen tar emot två argument, en dictionary med Fibonacci-data, och det aktuella
ingångsvärdet.
`print(f"DURATION FOR EACH APPROACH WITHIN INTERVAL: {nth_value}-0".center(75)+f"{line}")` ansvarade för att printa
ut main titeln för programmet. Ingångsvärdet hämtades från funktionens argument och titeln blev placerad i mitten
av terminalen. Exekveringstiden som skulle skrivas ut i terminalen skulle presenteras i sekunder, millisekunder,
mikrosekunder och nanosekunder. Dessa strängar lades in i en lista för att snyggt kunna presentera titlarna:
`print(f"{values[0].rjust(27)}{values[1].rjust(16)}{values[2].rjust(16)}{values[3].rjust(16)}")` och de justerades
till höger. All data från dictionaryn hämtades och deklarerades med `for key, val in fib_details.items():`.
Exekveringstiden hämtades genom att hämta första värdet i dictionaryns value. De olika tidsramarna som skulle 
presenteras hämtades genom att skicka ett argument till en annan funktion. Sekunder deklarerades genom:
`sec = duration_format(duration, values[0])` där exekveringstiden och Seconds skickas in i funktionen
duration_format, som innehöll en dictionary och resulterade get() metoden av dictionaryn vilket returnerar värdet
av det argument som skickas in. I detta fall var det "Seconds" som skickades in och då hämtade metoden värdet i 
dictionaryn där
key = "Seconds" och konverterar duration till en sträng. Detta gjorde för alla tidsramar och printades senare ut i terminalen med:
`print(f"{key.title().ljust(20)}{sec.rjust(0)}{millisec.rjust(16)}{microsec.rjust(16)}{nanosec.rjust(16)}")`
där key.titel för dictionaryn är presenterad till vänster och tidsramarna åt höger.

Funktionen `write_to_file` accepterar Fibonacci-detaljerna som argument och skapar motsvarande filer som innehåller
de beräknade värdena. Tre filer ska skapas, en för varje Fibonacci-tillvägagångssätt och ska sparas i katalogen
_Resources. I funktionen hämtas och deklareras först Fibonacci-detaljerna med 
`for key, val in fib_details.items():`.
Textfilerna skapas sen och namnet modifieras så de matchar uppgiftsbeskrivningen, modifiering av namnet gjordes
genom att ersätta mellanslag i Fibonacci-metoderna med _ och lägga till .text i slutet:
`key.replace(' ', '_') + '.txt'` Listan med Fibonacci-detaljer startade med det högsta värdet först, därför
vändes listan så att de lägsta värdena kommer först. Detta då varje Fibonacci-värde ska sättas tillsammans med sitt
index-värde. `seqAndValue = tuple(zip(itertools.count(), newValue)) ` tar emot listan newValue och returnerar en
lista med indexvärden till varje Fibonacci-värde. När detta var klart vändes listan igen så att de högsta värdena
kommer först, detta genom `result = reversed(seqAndValue)`. Varje värde i listan gicks till sist igenom för att
skriva ut värdena till textfilen `for data in result: f.write("%s: %s \n" % data)`.


## Diskussion

Den implementerade lösningen kan anses vara korrekt och uppfylla laborationens syfte av flera orsaker:
- Den egenimplementerade Fibonacci-metoden var en rekursiv lösning, vilket innebär att funktionen
anropar sig själv. Funktionen kontrollerade först om det önskade data redan fanns sparat i 
dictionaryn, ifall det inte gjorde det så beräknades värdet och sparades. Detta kunde man följa genom
att använda sig av breakpoint i funktionen och då se hur den kontrollerar värdet och registrerar
det i dictionaryn.

- Alla Fibonacci-funktioner blev kopplade till en decorator som beräknade körtiden. Detta kunde
kontrolleras tidigt genom att använda breakpoint. Senare när funktionen som skrev ut tiden var klar
kunde det bekräfta att tidsutskriften stämde. Den anpassade loggern blev skapad och var 5e körning
skrevs information ut i den. För att kontrollera att loggern stämde var det enbart att kontrollera
den tillsammans med de siffror för Fibonacci som fanns i laborationsbeskrivningen.

- Körtiden blev beräknad och utskriven i terminalen, både i sekunder, millisekunder, mikrosekunder
och nanosekunder. Utskriften i terminalen stämde överens med vad laborationsbeskrivningen gav som
exempel på hur tidsutskriften kunde se ut.

- Motsvarande Fibonacci-filer skulle skapas för de funktionerna som fanns, där det beräknade innehållet
skulle finnas. Som med tidigare logger var det enkelt att jämföra siffrorna i loggern tillsammans med
de Fibonacci-siffror som fanns i laborationsbeskrivningen för att kontrollera att de var korrekta.

Metodiken i denna laboration fungerade men det finns rum för förbättring, bland annat
då dictionaryn i fibonacci_memory skapas på nytt varje gång funktionen anropas. Detta gör att tidigare
körning inte sparas i dictionaryn för framtida körningar. En lösning på detta hade exempelvis varit
att skapa dictionaryn globalt så den kan hämta minnet från den andra rekursiva Fibonacci-metoden
eller att spara tidigare körningar.

Denna laboration har gett en förståelse över hur logging fungerar, både hur dessa skapas och hur man fyller den med 
data. Även hur bra och smidigt det är att använda sig av decorators, något som tog mig ett tag att greppa. Den
största utmaningen med laborationen var att förstå helheten av uppgiften och hur metoderna kommunicerar med varandra.
Under ett labbpass delade läraren med sig om tips om att lägga till print() i varje funktion för att se själva
flödet. Detta hjälpa definitivt och gjorde det enklare att greppa funktionerna.

Inlärningsmodulerna som var förberedande steget inför denna laboration var bra och täckte upp den information
som behövdes för att lösa denna uppgift. Hade önskat någon mer förklarande källa över decorators men det ligger
såklart på vårat ansvar att kunna googla och finna fler källor på sådant som känns svårare.