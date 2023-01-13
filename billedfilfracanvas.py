'''Dette er et script til at genere en billedfil fra canvaset'''


## iface.activeLayer().dataProvider().dataSourceUri() ## link til billeder

## QgsProject.instance().readPath("./") ## giver dig mappen programet arbejder i
billedindstillinger = QgsMapSettings() ## her sætter vi parametrene for, hvordan Qgs skal rendere en billedfil
billedindstillinger.setLayers([iface.activeLayer()]) ## iface tilgår de fleste af indstillingerne, lag på navne etc. Active layer, er markeret i venstre panel, iface funktionen sender så navnet til den ydre funktion
billedindstillinger.setOutputSize(QSize(iface.mapCanvas().size())) ## sætter størelsen på at være det samme som canvas
billedindstillinger.setExtent(iface.mapCanvas().extent()) ## extent objektet er dktm koordinater, dvs beder den ydre funkion, settings funktionen der formaterer til et billede format, om at tage koordinater fra canvaset

render = QgsMapRendererParallelJob(billedindstillinger)
def finished():
    billede = render.renderedImage()
    sti = QgsProject.instance().readPath("./")
    billede.save(sti+"/fraCanvas.png","png")
    print("gemt")
    
render.start()
render.finished.connect(finished)

