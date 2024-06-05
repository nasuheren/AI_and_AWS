import boto3
import os
import glob

def images_sending_to_aws():
    # IAM kullanıcısına ait "access key" ve "secret key" bilgileri
    aws_access_key_id = ''
    aws_secret_access_key = ''
    region_name = 'us-east-1'
    bucket_name = "nash-final-project"
    # Resimlerin olduğu klasör yolu
    folder_path = "C:\\Users\\nasuh\\Masaüstü\\AI_and_AWS\\error_images"

    # AWS hizmetine bağlanma
    client = boto3.client('s3', 
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=region_name)

    folder_path = "C:\\Users\\nasuh\\Masaüstü\\AI_and_AWS\\error_images"
    # Klasördeki tüm .jpg dosyalarını seçer
    jpg_files = glob.glob(os.path.join(folder_path, "*.jpg"))

    # Seçilen dosyaları kullanarak işlemleri gerçekleştirir
    for file in jpg_files:
        # print(file)
        image_files = file.split("\\")
        image_files = image_files[7]
        print(image_files)
        # Dosya yolu belirtilen resmi AWS'de ki bucket'a yollar
        with open("./error_images/" + image_files, "rb") as f:
            print(f.name)
            client.upload_fileobj(f, bucket_name, image_files)
