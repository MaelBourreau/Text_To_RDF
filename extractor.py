###########################################################################
# Cree a l'aide de l'article TRIPLET EXTRACTION FROM SENTENCES de D. Rusu #
###########################################################################

from nltk.parse import stanford
import os, sys
import rdflib
import operator

os.environ['STANFORD_PARSER'] = r'/home/mael/MASTER_2/TEXTE/RDF-Triple-API-master/stanford-parser-full-2015-01-30'
os.environ['STANFORD_MODELS'] = r'/home/mael/MASTER_2/TEXTE/RDF-Triple-API-master/stanford-parser-full-2015-01-30'



class Extractor():
    #Classe representant sujet, predicat, ou objet. pour predicat, contient la liste des predicats possibles. 
    class RDF_ELEMENT():
        
        def __init__(self, name, pos=''):
            self.name = name
            self.word = ''
            self.predicate_list = []
            self.parent = ''
            
        
    
    def init_data(self):
        self.parser = stanford.StanfordParser(model_path=r"/home/mael/MASTER_2/TEXTE/RDF-Triple-API-master/stanford-parser-full-2015-01-30/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
        self.NP = ''
        self.VP = ''
        #On recupere l'arbre du parseur stanford
        self.stanford_tree = self.parser.raw_parse(self.sentence)[0]
        self.subject = Extractor.RDF_ELEMENT('subject')
        self.predicate = Extractor.RDF_ELEMENT('predicate')
        self.Object = Extractor.RDF_ELEMENT('object')

    def Get_NP_VP(self, tree):
        #On test si l'arbre existe
        try:
            tree.label()
        except AttributeError:
            pass
        else:
            #On parcours l arbre, si le label est NP ou VP, on recupere le sous-arbre.
            if tree.label() == 'NP':
                if self.NP == '': 
                    self.NP = tree
            elif tree.label() == 'VP':
                if self.VP == '':
                    self.VP = tree
            for child in tree:
                self.Get_NP_VP(child)

    
    def extract_subject(self, tree):
        #on check si le mot existe deja
        if self.subject.word != '':
            return
        #on check si l'arbre existe
        try:
            tree.label()
        except AttributeError:
            pass
        else:
            #On check dans le sous arbre VB reccursivement si un label commence par NN (NN, NNP, NNPS, NNS)
            if tree.label()[:2] == 'NN':
                if self.subject.word == '':
                    self.subject.word = tree.leaves()[0]
            else:
                for child in tree:
                    self.extract_subject(child)
    
    
    def extract_predicate(self, tree, depth=0, parent=None):
        try:
            tree.label()
            #On extrais tous les verbes dans la "Verb Phrase" de l'arbre.
        except AttributeError:
            pass
        else:
            if tree.label()[:2] == 'VB':
                #On ajoute le parent pour l'extraction d'objet, le depth pour avoir la profondeur max
                self.predicate.predicate_list.append((tree.leaves()[0], depth, parent))
                self.parent = tree
            for child in tree:
                self.extract_predicate(child,parent=tree, depth=depth+1)
                
                
    def deepest_verb(self):
        if not self.predicate.predicate_list:
            return ''
        #On recupere la valeur de profondeur max
        return max(self.predicate.predicate_list, key=operator.itemgetter(1))
            
    
    def extract_object(self):
        for t in self.predicate.parent:
            if self.Object.word == '':
                self.extract_NP_PP_ADJP(t, t.label())
           
    
    def extract_NP_PP_ADJP(self, t, phrase_type):
        
        if self.Object.word != '':
            return
        try:
            t.label()
        except AttributeError:
            pass
        else:
            # Now we know that t.node is defined
            if t.label()[:2] == 'NN' and phrase_type in ['NP', 'PP']:
                if self.Object.word == '': 
                    self.Object.word = t.leaves()[0]
            elif t.label()[:2] == 'JJ' and phrase_type == 'ADJP':
                if self.Object.word == '': 
                    self.Object.word = t.leaves()[0]
            else:
                for child in t:
                    self.extract_NP_PP_ADJP(child, phrase_type)
                    
    
                        
                                 
    def main(self, line):
        #On initialise le parseur
        self.sentence = line
        self.init_data()
        #On recupere la "phrase" verbale et nominale
        self.Get_NP_VP(self.stanford_tree)
        #On recupere le sujet
        self.extract_subject(self.NP)
        
        #On recupere le predicat
        self.extract_predicate(self.VP)
        if self.subject.word == '' and self.NP != 'P':
            self.subject.word = self.NP.leaves()[0]
        self.predicate.word,  depth, self.predicate.parent = self.deepest_verb()
        
        #on recupere l'objet
        self.extract_object()

if __name__ == '__main__':
    try:
        file = sys.argv[1]
        
    except IndexError:
        print "Enter the file name"
    g = rdflib.Graph()
    filehandle = open(file, "r")
    fichier = open("graph", 'w')
    for line in filehandle:
        rdf = Extractor()
        rdf.main(line)
        fichier.write('http://www.example.org/' + rdf.subject.word + ' http://www.example.org/' + rdf.predicate.word  + ' http://www.example.org/' + rdf.Object.word  + '\n')
   