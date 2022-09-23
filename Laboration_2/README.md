# Laboration 2

## Utvecklingsmiljö & Verktyg

Operativsystemet som användes under denna uppgift var Windows 10. Programmeringsspråket är Python,
därför används PyCharm som är ett populärt IDE för Python. Git Bash är nedladdat för att kunna 
hämta och ladda upp filer, där Bitbucket är den versionshanteringsprogram som används.


## Syfte

Syftet med laboration 2 är att få praktisk erfarenhet av användning av `string`, `function` samt användarinmatning,
interaktion och validering. Detta gjordes främst genom att lösa en enskild uppgift som laborationen bestod av.


## Genomförande

Uppgiften i stort går ut på att användare ska kunna starta programmet genom att fylla i ett strängvärde i
kommandoraden innehållande ett användarnamn och lösenord. I detta fall är autentiseringsuppgifterna för användarna
redan ifylla och därför är det möjligt att testa systemet under utveckling genom att ange standardargument i 
PyCharm där man väljer de värden som ska användas som parametrar. Systemet ska vara beredd på att användaren
ska kunna uppge ett användarnamn med en blandning på stora och små bokstäver och ett lösenordet som är
skiftlägeskänsligt.

Funktionen authenticate_user ansvarar för att verifiera att den angivna inloggningsuppgiften är korrekt. Funktionen
tar emot inloggningsuppgiften bestående av användarnamn samt lösenord där dessa måste separeras i två separata
strängar. `rsplit(" ")[-1]` används för att ta fram lösenordet i strängen, då den tar det sista värdet som finns i 
strängen. `split(" ")[0:2]` används för att ta fram användarnamnet som består av de två första orden i strängen (för-
och efternamn) och returnerar automatiskt en lista då innehållet är mer än ett. Dessa variabler skickas senare till 
varsin metod då dessa ska ändras baserat på olika regler.

Funktionen format_username tar emot en lista av ett användarnamn från funktionen authenticate_user. format_username 
ska ändra användarnamnet så att alla bokstäver är små förutom de första bokstäverna i för- och efternamnet som ska 
vara stora. Detta gjordes genom att använda en `for-loop` som går igenom användarnamnet, i for-loopen sätts första 
bokstaven i för- och 
efternamnet i username till en stor bokstav och resten litet genom att använda den inbyggda metoden `title()`. 
Mellanslag mellan för- och efternamn ska ersättas med ett understreck vilket gjordes genom 
`'_'.join(map(str, username)` då användning metoden join() är en bra metod för att sammanlänka strängvärden från en 
lista. Funktionen returnerar det ändrade användarnamnet tillbaka till funktionen authenticate_user.

Funktionen decrypt_password används för att kryptera användarens lösenord. Funktionen tar emot lösenordet som en 
sträng och returnerar det krypterade lösenordet. Lösenordet krypteras först genom att kontrollera vissa villkor,
därför användes en for-loop med ett villkor där villkoret hade ytterligare ett villkor. Villkoren i for-loopen
kontrollerades med if-satser. Då aktuell iteration skulle räknas samt varje bokstav skulle gås igenom användes
enumerate i en for-loop, `for i, char in enumerate(password):`. Sedan kontrolleras ifall bokstaven 
är en vokal eller inte genom att ha en if-sats i for-loopen :`if char in vowels:`. Om bokstaven är en vokal så ska 
den krypterade bokstaven ha 0 framför och efter bokstaven, detta gjordes genom koden 
`decrypted += f"0{new_val}0"`. Är bokstaven däremot en konsonant läggs bara den krypterade bokstaven in i variabeln
decrypted = `decrypted += new_val`. Om den aktuella iterationen är udda så ska den krypterade bokstaven hoppa 9 steg
i ASCII tabellen när den krypteras, är bokstaven däremot jämn ska den hoppa 7 steg. Koden `ord(char) + rot9` användes 
för att ge bokstaven 9 hopp i ASCII tabellen och `chr((tmp - 126) + 32) if tmp > 126 else chr(tmp)` användes för att
ge bokstaven ett nytt värde från ASCII tabellen. Rotationen i ASCII tabellen är från 33-126 då 32 är ett tomt värde 
och 127 representerar delete, vilket inte är relevant vid denna kryptering av lösenord. Funktionen returnerar det 
ändrade lösenordet till metoden authenticate_user.

Funktionen authenticate_user innehåller en `dictionary` med aktuella användarnamn och lösenord. Funktionen tar emot 
det ändrade användarnamnet från format_username och krypterade lösenordet från decrypt_password och 
kontrollerar om dessa
passar in i de `key/values` som finns i `dictionaryn`. Detta gjorde med en for-loop `for key, val in agents.items():`
som kontrollerar varje `key` och `value` från `dictionaryn`. ` if key == user_tmp:` kontrollerar senare om `key` från
`dictionaryn` matchar med användarnamnet som funktionen mottog från format_username. Ifall detta stämmer kontrolleras
det om `value` kopplat till den matchade `keyn` är samma lösenord som mottogs från funktionen decrypt_password. Om 
dessa villkor är korrekt returnerar funktionen True, annars false.

Main metoden tar senare emot detta och ifall authenticate_user returnerar true så kommer en sträng i terminalen
om att användaren har loggats in. Om användaren och/eller lösenordet var felaktigt och authenticate_user returnerar 
false så visas ett felmeddelande i terminalen.


## Diskussion

Syftet med laboration 2 var att få en ökad erfarenhet om användandet av `string`, `function`, användarinmatning,
interaktion och validering. Syftet med uppgiften kan därför anses vara uppfylld då detta användes för att lösa
uppgiften i laboration 2. Uppgiftens utskrift i terminalen stämmer överens med vad uppgiftsbeskrivningen krävde
och lösningen överträder inte de krav som var satta. Lösningen kan anses vara tillförlitlig då den både följer
uppgiften samt Pythons kodstruktur.

Denna laboration har gjort att jag har lärt mig om hur funktioner i Python fungerar och olika inbyggda metoder, som 
join() och title() med mera. Även en ökad förståelse för validering där flera nästlande villkor användes för att lösa
uppgiften. Största utmaningen var ASCII-tabellen vilket är något jag inte har stött på tidigare och det tog ett tag 
för att förstå hur den fungerar och få till det i kod. 

Inlärningsmodulerna som var det förberedande steget inför denna uppgift var bra och täckte
upp den information som behövdes för att lösa denna uppgift. Angående förbättringar om uppgiften
så har jag inga kommentarer då jag anser denna vara väldigt tydlig och enkel att förstå. Uppgifterna kopplade till
modulerna var roliga och relevanta för denna uppgift.
