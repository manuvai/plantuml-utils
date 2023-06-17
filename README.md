# Utlitaire pour les documentations UML

## Diagramme de classes

```
!includeurl https://raw.githubusercontent.com/manuvai/plantuml-utils/master/class_diagram_utils.puml

```

## Diagramme de cas d'utilisation

```
!includeurl https://raw.githubusercontent.com/manuvai/plantuml-utils/master/usecase_diagram_utils.puml

```
## Modèle organisationnel de flux

```
!includeurl https://raw.githubusercontent.com/manuvai/plantuml-utils/master/usecase_diagram_utils.puml

```

Exemple :
```

Client as user
"Agent (comissions)" as agent #Coral    
intern("Site internet", app)
extern("Vignerons", vignerons) 
extern("Restaurateurs", restaurant) 

' rectangle "Service \nprojet" as proj #TECHNOLOGY

together {
        
    uc("Consultation de vins", consult)
    uc("Informations sur les vignerons", infos)
    uc("Commande de vins", order)
}

together {
    uc("Renseigner leurs informations", vignerons_infos)
}

together {
    uc("Obtenir QR Code", qr_code)
    uc("Information sur les vins", wine_infos)
}

together {
    
    uc("Accord", approval)
    uc("Refus", denial)
    uc("Proposer partenariat", proposal)
}

event(user, app, consult, down, down)
event(user, app, order, down, down)
event(app, user, infos, up, up)
event(vignerons, app, vignerons_infos, up, up)
event(app, restaurant, qr_code)
event(restaurant, app, wine_infos, up, up)
event(agent, restaurant, proposal, up, up)
event(restaurant, agent, approval)
event(restaurant, agent, denial)
```
