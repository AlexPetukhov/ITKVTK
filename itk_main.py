
import sys
import itk

# if len(sys.argv) < 3:
#     print("Usage: " + sys.argv[0] + " <input1> <input2> <input3> ... <output>")
#     sys.exit(1)

InputDimension = 2
OutputDimension = 3

PixelType = itk.UC

InputImageType = itk.Image[PixelType, InputDimension]
OutputImageType = itk.Image[PixelType, OutputDimension]

reader = itk.ImageFileReader[InputImageType].New()

tileFilter = itk.TileImageFilter[InputImageType, OutputImageType].New()

layout = [1, 1, 0]
tileFilter.SetLayout(layout)

num_images = int(sys.argv[1])
input_images_folder = sys.argv[2]

for idx in range(num_images):
    reader.SetFileName(input_images_folder + "/{}.png".format(idx))
    reader.Update()

    inputImage = reader.GetOutput()
    inputImage.DisconnectPipeline()

    tileFilter.SetInput(idx, inputImage)

defaultValue = 128
tileFilter.SetDefaultPixelValue(defaultValue)
tileFilter.Update()

thresholdFilter = itk.BinaryThresholdImageFilter[OutputImageType, OutputImageType].New()
thresholdFilter.SetInput(reader.GetOutput())

thresholdFilter.SetLowerThreshold(args.lower_threshold)
thresholdFilter.SetUpperThreshold(args.upper_threshold)
thresholdFilter.SetOutsideValue(0)
thresholdFilter.SetInsideValue(1)


writer = itk.ImageFileWriter[OutputImageType].New()
writer.SetFileName(sys.argv[-1])
writer.SetInput(tileFilter.GetOutput())
writer.Update()

