import os
import SimpleITK as sitk
from radiomics import featureextractor
import pandas as pd

def load_image(image_path):
    if os.path.isdir(image_path):
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(image_path)
        reader.SetFileNames(dicom_names)
        image = reader.Execute()
    elif image_path.endswith(('.nii', '.nii.gz')):
        image = sitk.ReadImage(image_path)
    else:
        raise ValueError("지원하지 않는 이미지 형식입니다.")
    return image

def run_extraction(image_path, mask_path, param_path=None, output_csv=None):
    image = load_image(image_path)
    mask = sitk.ReadImage(mask_path)

    if param_path and os.path.exists(param_path):
        extractor = featureextractor.RadiomicsFeatureExtractor(param_path)
        print(f"설정파일 로드 완료: {param_path}")
    else:
        extractor = featureextractor.RadiomicsFeatureExtractor()
        print("기본 설정으로 실행")

    # 특징 추출
    result = extractor.execute(image, mask)

    # 출력
    print("\nRadiomics Features:")
    for key, val in result.items():
        print(f"{key}: {val}")

    # CSV 저장
    if output_csv:
        df = pd.DataFrame([result])
        df.to_csv(output_csv, index=False)
        print(f"\nCSV 저장 완료: {output_csv}")

def main():
    print("두근두근해지는 시간")
    image_path = input("CT 이미지 경로 적어줘임: ").strip()
    mask_path = input("마스크 경로 적어줘잉: ").strip()
    param_path = input("YAML 설정 경로 적어줘잉: ").strip()
    output_csv = input("저장할 CSV 파일명 적어줘잉: ").strip()

    run_extraction(
        image_path=image_path,
        mask_path=mask_path,
        param_path=param_path if param_path else None,
        output_csv=output_csv if output_csv else None
    )

if __name__ == "__main__":
    main()
