import os;
import SimpleITK as sitk
import pydicom
import numpy as np

def get_ct_image(file):
    reader = sitk.ImageFileReader()
    reader.SetFileName(file)
    image = reader.Execute()
    return image

def sort_by_origin(image: sitk.Image):
    o = image.GetOrigin()
    if o.size == 3:
        return o[2]
    print('Expected a origin vector with 3 elements')
    exit(1)

class Patient:

    def __init__(self):
        self.slices = []
        self.rtstruct = RTStruct()

class CTSlice:

    def __init__(self):
        self.rows = 0
        self.columns = 0
        self.pixel_spacing = [0.0,0.0]
        self.slice_location = 0
        self.slice_thickness = 0
        self.image_position_patient = [0.0, 0.0, 0.0]
        self.pixel_data = []

class RTStruct:

    def __init__(self):
        self.data = []

if __name__ == "__main__":
    dirs = []
    training_dir = os.path.join("data", "Stanford_training")
    test_dir = os.path.join("data", "Stanford_testing")

    for d in os.listdir(training_dir):
            dirs.append(os.path.join(training_dir, d))

    patients = []
    for d in dirs:
        images = []
        patient = Patient()
        for f in os.listdir(d):
            fn = os.path.join(d, f)
            ds = pydicom.read_file(fn)
            if ds.Modality == "CT":
                slice = CTSlice()
                slice.rows = float(ds.Rows)
                slice.columns = float(ds.Columns)
                slice.slice_location = float(ds.SliceLocation)
                slice.slice_thickness = float(ds.SliceThickness)
                slice.pixel_spacing[0] = float(ds.PixelSpacing[0])
                slice.pixel_spacing[1] = float(ds.PixelSpacing[1])
                slice.image_position_patient = [0.0, 0.0, 0.0]
                slice.image_position_patient[0] = float(ds.ImagePositionPatient[0])
                slice.image_position_patient[1] = float(ds.ImagePositionPatient[1])
                slice.image_position_patient[2] = float(ds.ImagePositionPatient[2])
                slice.pixel_data = ds.pixel_array
                patient.slices.append(slice)
            elif ds.Modality == "RTSTRUCT":
                contour = RTStruct()
                for roi_contour_item in ds.ROIContourSequence:
                    for contour_item in roi_contour_item.ContourSequence:
                        contour.data.append(contour_item.ContourData)

                patient.rtstruct = contour
                print("Number of contour points: " + str(len(contour.data)))

        patients.append(patient)

        # images.sort(key=sort_by_origin)

    print("Number of patients: " + str(len(patients)))

