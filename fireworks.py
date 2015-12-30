#fireworks.py

import maya.cmds as cmds
import functools

#Set the playback options
cmds.playbackOptions(playbackSpeed = 0, maxPlaybackSpeed = 1)
cmds.playbackOptions(min = 1, max = 300)
cmds.currentTime(1)

#Removes old shader
trailShader = cmds.ls('trailShader*')
if len(trailShader) >0:
    cmds.delete(trailShader)

#Removes old gravity fields
rocketGravity = cmds.ls('rocketGravity*')
if len(rocketGravity) >0:
    cmds.delete(rocketGravity)
    
pGravityField = cmds.ls('pGravityField*')
if len(pGravityField) > 0:
    cmds.delete(pGravityField)

#Resets and removes old objects from the scene
fragmentEmitter = cmds.ls('fragmentEmitter*')
if len(fragmentEmitter) > 0:
    cmds.delete(fragmentEmitter)
    
fragmentParticles = cmds.ls('fragmentParticles*')
if len(fragmentParticles) > 0:
    cmds.delete(fragmentParticles)
    
sparkEmitter = cmds.ls('sparkEmitter*')
if len(sparkEmitter) > 0:
   cmds.delete(sparkEmitter)    
    
sparkParticles = cmds.ls('sparkParticles*')
if len(sparkParticles) > 0:
    cmds.delete(sparkParticles)

myEmitter = cmds.ls( 'myEmitter*' )
if len( myEmitter ) > 0:
    cmds.delete( myEmitter )
        
emittedParticles = cmds.ls( 'emittedParticles*' )
if len( emittedParticles ) > 0:
    cmds.delete( emittedParticles )
    
trailParticles = cmds.ls( 'trailParticles*' )
if len( trailParticles ) > 0:
    cmds.delete( trailParticles )  
        
myRamp = cmds.ls( 'ramp*' )
if len( myRamp ) > 0:
    cmds.delete( myRamp )
        
myArrayMapper = cmds.ls( 'arrayMapper*' )
if len( myArrayMapper ) > 0:
    cmds.delete( myArrayMapper )

my2dStructure = cmds.ls( 'place2dTexture*' )
if len( my2dStructure ) > 0:
    cmds.delete( my2dStructure )
        
myParticleSamplerInfo = cmds.ls( 'particleSamplerInfo*' )
if len( myParticleSamplerInfo ) > 0:
    cmds.delete( myParticleSamplerInfo )

#Creates the rocket emitter and its particles
cmds.emitter( dx=0, dy=1, dz=0, sp=0.3, spd=20, pos=(0, 0, 0), n='myEmitter', typ='direction', r=0.8 )
cmds.particle( n='emittedParticles' )
cmds.connectDynamic( 'emittedParticles', em='myEmitter' )

#Change render type to sphere
cmds.setAttr( 'emittedParticlesShape.particleRenderType', 4 )
#Add the attribute radius and set it to a value
cmds.addAttr( 'emittedParticlesShape', longName='radius', attributeType='float' )
cmds.setAttr( 'emittedParticlesShape.radius', 0.15 )

#Creates a gravity object and connects it to the emittedParticles
cmds.gravity(pos = (0,0,0), n = "rocketGravity")
cmds.connectDynamic( 'emittedParticles', f= 'rocketGravity')
#Set lifespan mode and time for the particles
cmds.setAttr( 'emittedParticlesShape.lifespanMode', 1 )
cmds.setAttr( 'emittedParticlesShape.lifespan', 2.5 )

#Creates emitter for first explosion and connects to particles
cmds.emitter('emittedParticles', spd = 8, srn = 2, n='fragmentEmitter' )
cmds.particle( n='fragmentParticles')
cmds.connectDynamic( 'fragmentParticles', em='fragmentEmitter' )
#Do the ramp for emitting particles at a later stage
cmds.addPP( 'emittedParticles', atr='rate' )
cmds.arrayMapper( target='emittedParticlesShape', destAttr='fragmentEmitterRatePP', inputV='ageNormalized', type='ramp' )

#Set interpolation to none
cmds.setAttr( 'ramp1.interpolation', 0 )
cmds.setAttr( 'arrayMapper1.maxValue', 300 )
#Set the positions of the ramp limits
cmds.setAttr( 'ramp1.colorEntryList[0].position', 0 )
cmds.setAttr( 'ramp1.colorEntryList[1].position', 0.90 )
cmds.setAttr( 'ramp1.colorEntryList[2].position', 1 )
#Sets color of the ramp
cmds.setAttr('ramp1.colorEntryList[0].color', 0, 0, 0, type = 'double3')
cmds.setAttr('ramp1.colorEntryList[1].color', 1, 1, 1, type = 'double3')
cmds.setAttr('ramp1.colorEntryList[2].color', 0, 0, 0, type = 'double3')
cmds.setAttr('emittedParticlesShape.visibility', 0 )

#Set conserve value for the fragmentshape
cmds.setAttr('fragmentParticlesShape.conserve', 0.9)

#Sets lifespan of the particles
cmds.setAttr('fragmentParticlesShape.lifespanMode', 2)
cmds.setAttr('fragmentParticlesShape.lifespan', 1.5)
cmds.setAttr('fragmentParticlesShape.lifespanRandom', 0.5)
#Set visibility to false
cmds.setAttr('fragmentParticlesShape.visibility', 0)
#Add a gravityField for the fragmentParticles
cmds.gravity(pos = (0,0,0), n = "pGravityField")
cmds.connectDynamic( 'fragmentParticles', f= 'pGravityField')
cmds.setAttr('pGravityField.magnitude', 2)

#Creates emitter for the trail from the rockets
cmds.emitter('emittedParticles', r=500, spd = 0.1, mxd = 0.1, n='trailEmitter' )
cmds.particle( n='trailParticles')
cmds.connectDynamic( 'trailParticles', em='trailEmitter' )
#Set particle render type
cmds.setAttr('trailParticlesShape.particleRenderType' , 8) #Particle type cloud
#Sets lifespan of the particles
cmds.setAttr('trailParticlesShape.lifespanMode', 2)
cmds.setAttr('trailParticlesShape.lifespan', 1)
cmds.setAttr('trailParticlesShape.lifespanRandom', 0.5)
#Set particle radius
cmds.addAttr('trailParticlesShape', ln = 'radius', at = 'float')
cmds.setAttr('trailParticlesShape.radius', 0.05)

#Add a sparkEmitter to the fragmentParticles and connect emitter to sparkParticles
cmds.emitter('fragmentParticles', spd=0.1, mxd=0.1, n='sparkEmitter' )
cmds.particle( n='sparkParticles')
cmds.connectDynamic('sparkParticles', em='sparkEmitter')
#Set particle render type
cmds.setAttr('sparkParticlesShape.particleRenderType' , 8) #Particle type cloud

#Sets lifespan of the particles
cmds.setAttr('sparkParticlesShape.lifespanMode', 2) #Random range
cmds.setAttr('sparkParticlesShape.lifespan', 1.5)
cmds.setAttr('sparkParticlesShape.lifespanRandom', 0.5)
#Set particle radius
cmds.addAttr('sparkParticlesShape', ln = 'radius', at = 'float')
cmds.setAttr('sparkParticlesShape.radius', 0.05)

#Created shading for particles
shader = cmds.shadingNode('particleCloud', asShader = True, name ='trailShader')
shadingGroup = (shader+'SG')
cmds.sets(renderable = True, noSurfaceShader = True, empty = True, name = shadingGroup)
cmds.defaultNavigation(connectToExisting=True, source = shader, destination = shadingGroup)
cmds.select(trailParticles)
cmds.sets(forceElement = shadingGroup)
cmds.setAttr( 'trailShader.glowIntensity', 0.5 )
cmds.setAttr( 'trailShader.color',0.915, 0.301816, 0.02928, type = 'double3' )

#Set transparency values from tRamp
cmds.shadingNode( 'ramp', asTexture = True , name = 'tRamp')
cmds.shadingNode( 'place2dTexture', asUtility = True )
cmds.connectAttr( 'place2dTexture1.outUV', 'tRamp.uv' )
cmds.connectAttr ( 'place2dTexture1.outUvFilterSize', 'tRamp.uvFilterSize' )
cmds.defaultNavigation( connectToExisting = True, navigatorDecisionString = 'particleSamplerInfo', destination = 'trailShader.transparency', source = 'tRamp' ) 

#Set life incandescence from incRamp values
cmds.shadingNode( 'ramp', asTexture = True, name = 'incRamp')
cmds.shadingNode( 'place2dTexture', asUtility = True )
cmds.connectAttr( 'place2dTexture1.outUV', 'incRamp.uv' )
cmds.connectAttr ( 'place2dTexture1.outUvFilterSize', 'incRamp.uvFilterSize' )
cmds.defaultNavigation( connectToExisting = True, navigatorDecisionString = 'particleSamplerInfo', destination = 'trailShader.incandescence', source = 'incRamp' ) 
cmds.setAttr('incRamp.colorEntryList[0].position', 1)
cmds.setAttr('incRamp.colorEntryList[1].position', 0)
cmds.setAttr('incRamp.colorEntryList[0].color', 0, 0, 0, type = 'double3')
cmds.setAttr('incRamp.colorEntryList[1].color', 1, 1, 1, type = 'double3')

#Add this shader to the sparkParticles also
cmds.select(sparkParticles)
cmds.sets(forceElement = shadingGroup)
#Add a shaderGlow to the particles and set its properties
cmds.select('shaderGlow1')
cmds.setAttr('shaderGlow1.haloType', 0)
cmds.setAttr('shaderGlow1.glowIntensity', 1.2)

# Create UI window
def createUI( pWindowTitle, pApplyCallback ):
    
    windowID = 'myWindowID'
    
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )
        
    cmds.window( windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True )
    
    cmds.rowColumnLayout()
    
    heightSlider = cmds.floatSliderGrp( label='Height', field=True, minValue=0.6, maxValue=1.0, value=1.0 )
    spreadSlider = cmds.floatSliderGrp( label='Spread', field=True, minValue=0.1, maxValue=0.3, value=0.3 )
    frameSlider = cmds.intSliderGrp( label='Frames', field=True, minValue=100, maxValue=500, value=300 )
    colorField = cmds.colorSliderGrp(label='Color', rgb=(0.915, 0.301816, 0.02928) )
    sizeGroup = cmds.floatSliderGrp( label='Explosion size', field=True, minValue=4.0, maxValue=10.0, value=7 )
            
    cmds.button( label='Apply', command=functools.partial( pApplyCallback, heightSlider, spreadSlider, frameSlider, colorField, sizeGroup ) )
    
    '''
    def cancelCallback( *pArgs ):
        if cmds.window( windowID, exists=True ):
            cmds.deleteUI( windowID )
    '''
    #cmds.button( label='Cancel', command=cancelCallback )
    
    cmds.showWindow()

#This happens when pressing the apply button
def applyCallback( heightSlider, spreadSlider, frameSlider, colorField, sizeGroup, *pArgs ):
    
    # print 'Apply button pressed.'
        
    height = cmds.floatSliderGrp( heightSlider, query=True, value=True )
    spreads = cmds.floatSliderGrp( spreadSlider, query=True, value=True )
    frames = cmds.intSliderGrp( frameSlider, query=True, value=True )
    
    print 'Height: %s' % ( height )
    print 'Spread: %s' % ( spreads )
    print 'Frames: %s' % ( frames )
    
    #Changes the height of the fireworks
    cmds.setAttr( 'myEmitter.spd', 20*height )
    cmds.setAttr( 'emittedParticlesShape.lifespan', 2.5*height )
    cmds.setAttr( 'trailParticlesShape.lifespan', height)
    cmds.setAttr( 'trailParticlesShape.lifespanRandom', 0.5*height)
    
    #CHanges the spread
    cmds.setAttr( 'myEmitter.spread', spreads )
    
    #Changes number of frames
    cmds.playbackOptions( max = frames )  
    #Changes firework color
    cmds.colorSliderGrp( colorField, e=True, query=True, vis=True)
    rgb = cmds.colorSliderGrp( colorField, query=True, rgb=True)
    cmds.setAttr("trailShader.color",rgb[0],rgb[1],rgb[2], type="double3" )
    #Changes explosion size
    explosionSize = cmds.floatSliderGrp( sizeGroup, query=True, value=True )
    cmds.setAttr('fragmentEmitter.spd', explosionSize)    
                            
#Call the createUI function
createUI( 'My firework', applyCallback )

cmds.select(shader)