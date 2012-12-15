from ilastik.applets.base.appletSerializer import AppletSerializer,\
    deleteIfPresent, getOrCreateGroup

class ObjectExtractionSerializer(AppletSerializer):
    """
    """
    def __init__(self, mainOperator, projectFileGroupName):
        super( ObjectExtractionSerializer, self ).__init__( projectFileGroupName )
        self.mainOperator = mainOperator

    def _serializeToHdf5(self, topGroup, hdf5File, projectFilePath):
        op = self.mainOperator.innerOperators[0]
        print "object extraction: serializeToHdf5", topGroup, hdf5File, projectFilePath
        print "object extraction: saving label image"
        src = op._opObjectExtractionBg._mem_h5
        deleteIfPresent( topGroup, "LabelImage")
        src.copy('/LabelImage', topGroup) 

        print "object extraction: saving region features"
        deleteIfPresent( topGroup, "samples")
        samples_gr = getOrCreateGroup( topGroup, "samples" )
        for t in op._opObjectExtractionBg._opRegFeats._cache.keys():
            t_gr = samples_gr.create_group(str(t))
            t_gr.create_dataset(name="RegionCenter", data=op._opObjectExtractionBg._opRegFeats._cache[t]['RegionCenter'])
            t_gr.create_dataset(name="Count", data=op._opObjectExtractionBg._opRegFeats._cache[t]['Count'])            
            

    def _deserializeFromHdf5(self, topGroup, groupVersion, hdf5File, projectFilePath):
        print "objectExtraction: deserializeFromHdf5", topGroup, groupVersion, hdf5File, projectFilePath

        print "objectExtraction: loading label image"
        dest = self.mainOperator.innerOperators[0]._opObjectExtractionBg._mem_h5        

        del dest['LabelImage']
        topGroup.copy('LabelImage', dest)

        print "objectExtraction: loading region features"
        if "samples" in topGroup.keys():
            cache = {}

            for t in topGroup["samples"].keys():
                cache[int(t)] = dict()
                if 'RegionCenter' in topGroup["samples"][t].keys():
                    cache[int(t)]['RegionCenter'] = topGroup["samples"][t]['RegionCenter'].value
                if 'Count' in topGroup["samples"][t].keys():                    
                    cache[int(t)]['Count'] = topGroup["samples"][t]['Count'].value                
            self.mainOperator.innerOperators[0]._opObjectExtractionBg._opRegFeats._cache = cache

    def isDirty(self):
        return True

    def unload(self):
        print "ObjExtraction.unload not implemented" 
