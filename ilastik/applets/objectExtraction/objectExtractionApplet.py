from ilastik.applets.base.applet import Applet

from lazyflow.graph import OperatorWrapper
from ilastik.applets.objectExtraction.opObjectExtraction import OpObjectExtraction
from ilastik.applets.objectExtraction.objectExtractionSerializer import ObjectExtractionSerializer

class ObjectExtractionApplet( Applet ):
    def __init__( self, graph, guiName="Object Extraction", projectFileGroupName="ObjectExtraction" ):
        super(ObjectExtractionApplet, self).__init__( guiName )
        self._topLevelOperator = OperatorWrapper(OpObjectExtraction, graph=graph)        

        self._gui = None
        
        self._serializableItems = [ ObjectExtractionSerializer(self._topLevelOperator, projectFileGroupName) ]

    @property
    def topLevelOperator(self):
        return self._topLevelOperator

    @property
    def dataSerializers(self):
        return self._serializableItems

    @property
    def viewerControlWidget(self):
        return self._centralWidget.viewerControlWidget

    @property
    def gui(self):
        if self._gui is None:
            from objectExtractionGui import ObjectExtractionGui
            self._gui = ObjectExtractionGui(self._topLevelOperator)        
        return self._gui