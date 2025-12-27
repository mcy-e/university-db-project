from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal

from .base_crud import BaseCRUD

TEST_DATA=data = [
    ("1","Reffas","Chouaib","23-02-2007","1t, 02","Annaba","202235","064862265","Null","mcy@gmail.com"),
    ("2","Amine","Benkacem","15-05-2006","12 Av. Liberté","Algiers","16000","0555123456","021123456","amine.b@gmail.com"),
    ("3","Sara","Belkacem","02-11-2007","23 Rue El-Fadjr","Oran","31000","0661234567","031987654","sara.belkacem@gmail.com"),
    ("4","Youssef","Haddad","18-07-2005","45 Bd. Pasteur","Constantine","25000","0559876543","031123987","youssef.h@gmail.com"),
    ("5","Leila","Mansouri","09-01-2006","7 Impasse des Roses","Annaba","202200","0669876543","038123456","leila.m@gmail.com"),
    ("6","Omar","Bensaid","12-12-2007","88 Rue des Fleurs","Oran","31010","0556655443","031112233","omar.b@gmail.com"),
    ("7","Nadia","Khelifi","05-06-2005","34 Av. Emir Abdelkader","Algiers","16010","0663344556","021998877","nadia.k@gmail.com"),
    ("8","Rachid","Toumi","20-09-2006","21 Bd. de la République","Constantine","25010","0554433221","031776655","rachid.t@gmail.com"),
    ("9","Meryem","Zebdi","30-03-2007","56 Rue du 1er Novembre","Annaba","202210","0661122334","038887766","meryem.z@gmail.com"),
    ("10","Farid","Cherif","14-08-2006","11 Av. des Martyrs","Oran","31020","0559988776","031665544","farid.c@gmail.com"),
    ("11","Lina","Bouzid","22-04-2005","9 Rue Ibn Khaldoun","Algiers","16020","0665566778","021334455","lina.b@gmail.com"),
    ("12","Samir","Guelzim","17-10-2007","77 Bd. Krim Belkacem","Constantine","25020","0557766554","031223344","samir.g@gmail.com"),
    ("13","Sofia","Kacem","03-01-2006","5 Impasse de l’Indépendance","Annaba","202220","0667788990","038112233","sofia.k@gmail.com"),
    ("14","Karim","Bensaid","28-02-2007","19 Av. du Général","Oran","31030","0558899776","031445566","karim.b@gmail.com"),
    ("15","Amina","Djahid","11-11-2006","33 Rue de l’Industrie","Algiers","16030","0663344112","021556677","amina.d@gmail.com")
]

class StudentCRUD(BaseCRUD):

    
    #* Create Back Signal
    go_back=pyqtSignal()


    def __init__(self):
        super().__init__(["ID", "First Name", "Last Name", "dob", "address","city","zip_code","phone","fax","Email"])
        
        self.populate_table(TEST_DATA)
        self.back_btn.clicked.connect(self.go_back.emit)

