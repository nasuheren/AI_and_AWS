import boto3
import os
import glob

def images_sending_to_aws():
    # IAM kullanıcısına ait "access key" ve "secret key" bilgileri
    aws_access_key_id = 'AKIAYUO4FWZ57LJOIDHV'
    aws_secret_access_key = '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'
    region_name = 'us-east-1'
    bucket_name = "nash-final-project"
    # Resimlerin olduğu klasör yolu
    folder_path = "C:\\Users\\nasuh\\Masaüstü\\Python-Projeler\\Human-Detection\\resimler"

    # AWS hizmetine bağlanma
    client = boto3.client('s3', 
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=region_name)

    folder_path = "C:\\Users\\nasuh\\Masaüstü\\Python-Projeler\\Human-Detection\\resimler"
    # Klasördeki tüm .jpg dosyalarını seçer
    jpg_files = glob.glob(os.path.join(folder_path, "*.jpg"))

    # Seçilen dosyaları kullanarak işlemleri gerçekleştirir
    for file in jpg_files:
        # print(file)
        image_files = file.split("\\")
        image_files = image_files[7]
        print(image_files)
        # Dosya yolu belirtilen resmi AWS'de ki bucket'a yollar
        with open("./resimler/" + image_files, "rb") as f:
            print(f.name)
            client.upload_fileobj(f, bucket_name, image_files)