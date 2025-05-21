import os
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import SimpleITK as sitk
import pandas as pd

def load_dicom_folder(dicom_folder):
    try:
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(dicom_folder)
        reader.SetFileNames(dicom_names)
        image = reader.Execute()
        return sitk.GetArrayFromImage(image)  # (z, y, x)
    except Exception as e:
        print(f"DICOM 로딩 실패: {e}")
        return None

def load_nifti_mask(mask_path):
    try:
        data = nib.load(mask_path).get_fdata()
        return np.transpose(data, (2, 1, 0))  # (x, y, z) → (z, y, x)
    except Exception as e:
        print(f"마스크 로딩 실패: {e}")
        return None
    
def load_dcmnii(dcmnii_path):
    try:
        datadcm = nib.load(dcmnii_path).get_fdata()
        return datadcm
    except Exception as e:
        print(f"CT 마스크 로딩 실패: {e}")
        return None
    
def load_nifti_mask2(mask_path):
    try:
        data2 = nib.load(mask_path).get_fdata()
        return data2
    except Exception as e:
        print(f'마스크2 로딩 실패: {e}')
        return None
    
def main():
    print("HU Histogram from DICOM + NIfTI")

    dicom_folder = input("CT DICOM 폴더 경로를 입력하세요: ").strip('"').strip()
    mask_path = input("마스크 NIfTI 파일 경로를 입력하세요 (.nii or .nii.gz): ").strip('"').strip()
    dcmnii_path = input("CT NIfTI 파일 경로를 입력하세요 (.nii or .nii.gz): ").strip('"').strip()

    if not os.path.exists(dicom_folder):
        print("DICOM 폴더 경로가 존재하지 않습니다.")
        return
    if not os.path.exists(mask_path):
        print("마스크 파일 경로가 존재하지 않습니다.")
        return
    if not os.path.exists(dcmnii_path):
        print("CT_NIfTI 폴더 경로가 존재하지 않습니다.")
        return

    ct_data = load_dicom_folder(dicom_folder)
    mask_data = load_nifti_mask(mask_path)
    ct_nii_data = load_dcmnii(dcmnii_path)
    mask_data2 = load_nifti_mask2(mask_path)

    if ct_data is None or mask_data is None:
        return

    if ct_data.shape != mask_data.shape:
        print(f"CT({ct_data.shape})와 마스크({mask_data.shape})의 shape이 다릅니다.")
        return

    hu_values = ct_data[mask_data > 0]

    if hu_values.size == 0:
        print("마스크된 영역이 없습니다.")
        return
    
    hu_values2 = ct_nii_data[mask_data2 > 0]
    if hu_values2.size == 0:
        print("마스크된 영역이 없습니다.")
        return
    bins = np.arange(-200, 1000 , 1)
    plt.figure(figure=(7, 5))
    plt.hist(hu_values, bins=bins, color = 'red' )
    plt.hist(hu_values2, bins=bins, color = 'blue')
    plt.xlabel('HU')
    plt.ylabel('Voxels')
    plt.grid()
    plt.show()
  
    

if __name__ == "__main__":
    main()
