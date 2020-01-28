# https://czytac.com/java-book/book/Rok_1984_George_Orwell
# http://nkjp.pl/poliqarp/help/plse2.html
import morfeusz2


morf = morfeusz2.Morfeusz()

file = open('rok_1984.txt', 'r') 

flex_dict = {
	"subst": "rzeczownik",
	"depr": "rzeczownik deprecjatywny",
	"num": "liczebnik główny",
	"numcol": "liczebnik zbiorowy",
	"adj": "przymiotnik",
	"adja": "przymiotnik przyprzym.",
	"adjp": "przymiotnik poprzyimkowy",
	"adjc": "przymiotnik predykatywny",
	"adv": "przysłówek",
	"ppron12": "zaimek nietrzecioosobowy",
	"ppron3": "zaimek trzecioosobowy",
	"siebie": "zaimek siebie",
	"fin": "forma nieprzeszła",
	"bedzie": "forma przyszła być",
	"aglt": "aglutynant być",
	"praet": "pseudoimiesłów",
	"impt": "rozkaźnik",
	"imps": "bezosobnik",
	"inf": "bezokolicznik",
	"pcon": "im. przys. współczesny",
	"pant": "im. przys. uprzedni",
	"ger": "odsłownik",
	"pact": "im. przym. czynny",
	"ppas": "im. przym. bierny",
	"winien": "winien",
	"pred": "predykatyw",
	"prep": "przyimek",
	"conj": "spójnik współrzędny",
	"comp": "spójnik podrzędny",
	"qub": "kublik",
	"brev": "skrót",
	"burk": "burkinostka",
	"interj": "wykrzyknik",
	"interp": "interpunkcja",
	"xxx": "ciało obce",
	"ign": "forma nierozpoznana"
}



singular_plural_dict = {
    "sg": "pojedyncza",
    "pl": "mnoga"
}

#analysis = morf.analyse(file.read())
analysis = morf.analyse("Ala  wywołuje koty")
print(analysis)
for i, j, interp in analysis:
    #print(i, j, interp)
    morphosyntactic_markers = interp[2].split(':')

    
    is_singular = morphosyntactic_markers[1] == 'sg'
    print(morphosyntactic_markers)