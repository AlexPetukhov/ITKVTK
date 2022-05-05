#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vtkmodules.all as vtk


def get_program_parameters():
    import argparse
    description = 'Read an unstructured grid file.'
    epilogue = ''''''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', default="data/itk_coubex.vtk")
    args = parser.parse_args()
    return args.filename


# volumeProperty = vtk.vtkVolumeProperty()


# skin = 105
skin = 90
# bone = 140
bone = 250
rgb = [[skin, 1.0, 0.0, 0.0],  # skin
       [bone, 1.0, 1.0, 1.0]]  # bone
opacity = [[skin, 0.1],  # skin
           [bone, 1.0]]  # bone


def keyPressed(caller, eventId):
    code = caller.GetKeyCode()
    delta = 1
    opdelta = 0.01
    if code == 'o':  # o,p control first color value
        rgb[0][0] -= delta
        opacity[0][0] = rgb[0][0]
        print('skin val', rgb[0][0])
    elif code == 'p':
        rgb[0][0] += delta
        opacity[0][0] = rgb[0][0]
        print('skin val', rgb[0][0])
    elif code == 'a':  # a,s control second color value
        rgb[1][0] -= delta
        opacity[1][0] = rgb[1][0]
        print('bone val', rgb[1][0])
    elif code == 's':
        rgb[1][0] += delta
        opacity[1][0] = rgb[1][0]
        print('bone val', rgb[1][0])
    elif code == 'r':  # r,t control first opacity value
        opacity[0][1] -= opdelta
        print('skin op', opacity[0][1])
    elif code == 't':
        opacity[0][1] += opdelta
        print('skin op', opacity[0][1])
    elif code == 'f':  # f,g control second opacity value
        opacity[1][1] -= opdelta
        print('bone op', opacity[1][1])
    elif code == 'g':
        opacity[1][1] += opdelta
        print('bone op', opacity[1][1])
    updateColorOpacity()


def updateColorOpacity():
    opacityFunction = vtk.vtkPiecewiseFunction()
    opacityFunction.AddPoint(0, 0.0)
    opacityFunction.AddPoint(opacity[0][0] - 10, 0.0)
    opacityFunction.AddPoint(opacity[0][0], opacity[0][1])  # skin
    opacityFunction.AddPoint(opacity[1][0], opacity[1][1])  # bone
    # for op in opacity:
    #  print "op",op[0],op[1]
    #  opacityFunction.AddPoint(op[0], op[1])
    colorFunction = vtk.vtkColorTransferFunction()
    colorFunction.AddRGBPoint(0, 0, 0, 0)
    colorFunction.AddRGBPoint(rgb[0][0] - 10, 0, 0, 0)
    colorFunction.AddRGBPoint(rgb[0][0], rgb[0][1], rgb[0][2], rgb[0][3])  # skin
    colorFunction.AddRGBPoint(rgb[1][0], rgb[1][1], rgb[1][2], rgb[1][3])  # bone
    # for c in rgb:
    # print 'rgb',c[0],c[1],c[2],c[3]
    # colorFunction.AddRGBPoint(c[0], c[1], c[2], c[3])
    # global volumeProperty
    # volumeProperty.SetColor(colorFunction)
    # volumeProperty.SetScalarOpacity(opacityFunction)
    # global volume
    # volume.Update()


def main():
    colors = vtk.vtkNamedColors()

    filename = get_program_parameters()
    reader = vtk.vtkStructuredPointsReader()
    reader.SetFileName(filename)
    reader.ReadAllScalarsOn()
    reader.ReadAllVectorsOn()
    reader.Update()


    # filter = vtk.vtkImageGaussianSmooth()
    # filter.SetInputConnection(reader.GetOutputPort())

    # data = reader.GetOutput()
    # updateColorOpacity()
    # composite function (using ray tracing)
    # compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
    # volumeMapper = vtk.vtkVolumeRayCastMapper()
    # volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
    # volumeMapper.SetVolumeRayCastFunction(compositeFunction)
    # volumeMapper.SetInput(data)
    volumeMapper = vtk.vtkSmartVolumeMapper()
    volumeMapper.SetInputConnection(reader.GetOutputPort())
    # make the volume
    # volume = vtk.vtkVolume()
    # global volume
    alphaChannelFunc = vtk.vtkPiecewiseFunction()
    alphaChannelFunc.AddPoint(0, 0.0)
    alphaChannelFunc.AddPoint(50, 0.05)
    alphaChannelFunc.AddPoint(100, 0.1)
    alphaChannelFunc.AddPoint(150, 0.2)

    # This class stores color data and can create color tables from a few color points.
    #  For this demo, we want the three cubes to be of the colors red green and blue.
    colorFunc = vtk.vtkColorTransferFunction()
    colorFunc.AddRGBPoint(50, 1.0, 0.0, 0.0)
    colorFunc.AddRGBPoint(100, 0.0, 1.0, 0.0)
    colorFunc.AddRGBPoint(150, 0.0, 0.0, 1.0)

    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorFunc)
    volumeProperty.SetScalarOpacity(alphaChannelFunc)

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    # With almost everything else ready, its time to initialize the renderer and window, as well as
    #  creating a method for exiting the application
    renderer = vtk.vtkRenderer()
    renderWin = vtk.vtkRenderWindow()
    renderWin.AddRenderer(renderer)
    renderInteractor = vtk.vtkRenderWindowInteractor()
    renderInteractor.SetRenderWindow(renderWin)

    # We add the volume to the renderer ...
    renderer.AddVolume(volume)
    renderer.SetBackground(colors.GetColor3d("MistyRose"))

    # ... and set window size.
    renderWin.SetSize(400, 400)

    # A simple function to be called when the user decides to quit the application.
    def exitCheck(obj, event):
        if obj.GetEventPending() != 0:
            obj.SetAbortRender(1)

    # Tell the application to use the function as an exit check.
    renderWin.AddObserver("AbortCheckEvent", exitCheck)

    renderInteractor.Initialize()
    # Because nothing will be rendered without any input, we order the first render manually
    #  before control is handed over to the main-loop.
    renderWin.Render()
    renderInteractor.Start()


if __name__ == '__main__':
    main()

#
# def main():
#     colors = vtk.vtkNamedColors()
#
#     filename = get_program_parameters()
#
#     reader = vtk.vtkStructuredPointsReader()
#     reader.SetFileName(filename)
#     reader.Update()
#     data = reader.GetOutput()
#     # updateColorOpacity()
#     # composite function (using ray tracing)
#     compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
#     volumeMapper = vtk.vtkVolumeRayCastMapper()
#     volumeMapper.SetVolumeRayCastFunction(compositeFunction)
#     volumeMapper.SetInput(data)
#     # make the volume
#     # volume = vtk.vtkVolume()
#     global volume
#     volume.SetMapper(volumeMapper)
#     volume.SetProperty(volumeProperty)
#     # renderer
#     renderer = vtk.vtkRenderer()
#     renderWin = vtk.vtkRenderWindow()
#     renderWin.AddRenderer(renderer)
#     renderInteractor = vtk.vtkRenderWindowInteractor()
#     renderInteractor.SetRenderWindow(renderWin)
#     renderInteractor.AddObserver(vtk.vtkCommand.KeyPressEvent, keyPressed)
#     renderer.AddVolume(volume)
#     renderer.SetBackground(0, 0, 0)
#     renderWin.SetSize(400, 400)
#     renderInteractor.Initialize()
#     renderWin.Render()
#     renderInteractor.Start()

# Read the source file.
# reader = vtk.vtkUnstructuredGridReader()
# reader = vtk.vtkDataReader()
# reader.SetFileName(filename)
# reader.ReadAllScalarsOn()
# reader.Update()
#
# writer = vtk.vtkUnstructuredGridWriter()
# writer.SetInputData(reader.GetOutput())
# writer.SetFileName("Output.vtk")
# writer.Write()

# output = reader.GetOutput()
# # scalar_range = output.GetScalarRange()
#
# # Create the mapper that corresponds the objects of the vtk.vtk file
# # into graphics elements
# mapper = vtk.vtkDataSetMapper()
# mapper.SetInputData(output)
# # mapper.SetScalarRange(scalar_range)
# mapper.ScalarVisibilityOff()
#
# # Create the Actor
# actor = vtk.vtkActor()
# actor.SetMapper(mapper)
# actor.GetProperty().EdgeVisibilityOn()
# actor.GetProperty().SetLineWidth(2.0)
# actor.GetProperty().SetColor(colors.GetColor3d("MistyRose"))
#
# backface = vtk.vtkProperty()
# backface.SetColor(colors.GetColor3d('Tomato'))
# actor.SetBackfaceProperty(backface)
#
# # Create the Renderer
# renderer = vtk.vtkRenderer()
# renderer.AddActor(actor)
# renderer.SetBackground(colors.GetColor3d('Wheat'))
#
# # Create the RendererWindow
# renderer_window = vtk.vtkRenderWindow()
# renderer_window.SetSize(640, 480)
# renderer_window.AddRenderer(renderer)
# renderer_window.SetWindowName('ReadUnstructuredGrid')
#
# # Create the RendererWindowInteractor and display the vtk_file
# interactor = vtk.vtkRenderWindowInteractor()
# interactor.SetRenderWindow(renderer_window)
# interactor.Initialize()
# interactor.Start()
#
#
# if __name__ == '__main__':
#     main()
