# coding: utf-8
import re
import tika 
import sys 
from tika import parser 

#Cas consideres : 
alphabet= "([A-Za-z])"
#Mr. Mrs.
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
#Inc. Ltd. Co.
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
#Tous types d'accronimes
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
#Tous types de sites en .com, .net, .org, .io, .gov
websites = "[.](com|net|org|io|gov)"

def make_sentences(nomfichier):
    raw = parser.from_file(nomfichier)
    texte = raw['content']
    texte = " " + texte + "  "
    texte = texte.replace("\n"," ")
    texte = re.sub(prefixes,"\\1<prd>",texte)
    texte = re.sub(websites,"<prd>\\1",texte)
    if "Ph.D" in texte: texte = texte.replace("Ph.D.","Ph<prd>D<prd>")
    texte = re.sub("\s" + alphabet + "[.] "," \\1<prd> ",texte)
    texte = re.sub(acronyms+" "+starters,"\\1<stop> \\2",texte)
    texte = re.sub(alphabet + "[.]" + alphabet + "[.]" + alphabet + "[.]","\\1<prd>\\2<prd>\\3<prd>",texte)
    texte = re.sub(alphabet + "[.]" + alphabet + "[.]","\\1<prd>\\2<prd>",texte)
    texte = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",texte)
    texte = re.sub(" "+suffixes+"[.]"," \\1<prd>",texte)
    texte = re.sub(" " + alphabet + "[.]"," \\1<prd>",texte)
    if "”" in texte: texte = texte.replace(".”","”.")
    if "\"" in texte: texte = texte.replace(".\"","\".")
    if "!" in texte: texte = texte.replace("!\"","\"!")
    if "?" in texte: texte = texte.replace("?\"","\"?")
    texte = texte.replace(".",".<stop>")
    texte = texte.replace("?","?<stop>")
    texte = texte.replace("!","!<stop>")
    texte = texte.replace("<prd>",".")
    phrases = texte.split("<stop>")
    phrases = phrases[:-1]
    phrases = [s.strip() for s in phrases]
    return phrases

phrases = make_sentences(sys.argv[1])
fichier = open("text","w") 
for phrase in phrases:
	fichier.write(phrase+"\n")

fichier.close() 
