import os
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import SimpleITK as sitk

def load_dicom_folder(dicom_folder):
    try:
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(dicom_folder)
        reader.SetFileNames(dicom_names)
        image = reader.Execute()
        return sitk.GetArrayFromImage(image)  
    except Exception as e:
        print(f"DICOM 파일이 아닌 거 아닐까!: {e}")
        return None

def load_nifti_mask(mask_path):
    try:
        data = nib.load(mask_path).get_fdata()
        return np.transpose(data, (2, 1, 0))  ##SimpleITK가 갖고 있는 좌표는 Z, Y, X라는 걸 확인
    except Exception as e:
        print(f"마스크 파일이 아닌 거 아닐까!: {e}")
        return None

def main():
    print("HU Histogram from DICOM + NIfTI")

    dicom_folder = input("CT DICOM 폴더 경로를 입력하세요: ").strip('"').strip()
    mask_path = input("마스크 NIfTI 파일 경로를 입력하세요 (.nii or .nii.gz): ").strip('"').strip()

    if not os.path.exists(dicom_folder):
        print("DICOM 폴더 경로가 존재하지 않습니다.")
        return
    if not os.path.exists(mask_path):
        print("마스크 파일 경로가 존재하지 않습니다.")
        return

    ct_data = load_dicom_folder(dicom_folder)
    mask_data = load_nifti_mask(mask_path)

    if ct_data is None or mask_data is None:
        return

    if ct_data.shape != mask_data.shape:
        print(f"CT({ct_data.shape})와 마스크({mask_data.shape})의 shape이 다릅니다.")
        return

    hu_values = ct_data[mask_data > 0]

    if hu_values.size == 0:
        print("이게 뭔 소리야 마스크가 없다니")
        return
    bins = np.arange(-200, 1001, 1)
    hist_counts, hist_bins = np.histogram(hu_values, bins=bins)
    hist_portions = hist_counts/hist_counts.sum()
    hist_centers = (hist_bins[:-1]+hist_bins[1:])/2
    df = pd.DataFrame({'Bin Center': hist_centers.astype(int), 'Portions': hist_portions})
    df.to_csv(output_path, index=False)
  
if __name__ == "__main__":
    main()
