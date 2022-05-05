import sys
import itk


def main():
    # run:
    # python3 itk_main.py 60 "data/cells3d_coubex" "data/itk_coubex.tiff"

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

    writer = itk.ImageFileWriter[OutputImageType].New()
    writer.SetFileName(sys.argv[-1])
    writer.SetInput(tileFilter.GetOutput())
    writer.Update()


if __name__ == '__main__':
    main()
