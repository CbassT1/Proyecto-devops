import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')
s3 = boto3.client('s3')

def aprovisionar_instancia():
    print("1. Aprovisionando nueva instancia EC2...")
    ami_id = 'ami-0ec10929233384c7f' 
    
    try:
        respuesta = ec2.run_instances(
            ImageId=ami_id,
            InstanceType='t2.micro',
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'Servidor-Automatizado-Python'}]
            }]
        )
        id_instancia = respuesta['Instances'][0]['InstanceId']
        print(f"Instancia creada exitosamente. ID: {id_instancia}")
    except Exception as e:
        print(f"Error al crear instancia: {e}")

def reporte_recursos():
    print("\n2. Generando reporte de instancias EC2...")
    try:
        respuesta = ec2.describe_instances()
        for reservacion in respuesta['Reservations']:
            for instancia in reservacion['Instances']:
                id_inst = instancia['InstanceId']
                estado = instancia['State']['Name']
                tipo = instancia['InstanceType']
                print(f"   - ID: {id_inst} | Tipo: {tipo} | Estado: {estado}")
    except Exception as e:
        print(f"Error al obtener instancias: {e}")

def reporte_s3():
    print("\n3. Listando Buckets S3 y sus objetos...")
    try:
        buckets = s3.list_buckets()['Buckets']
        if not buckets:
            print("   - No hay buckets creados en esta cuenta.")
        
        for bucket in buckets:
            nombre_bucket = bucket['Name']
            print(f"   Bucket: {nombre_bucket}")
            objetos = s3.list_objects_v2(Bucket=nombre_bucket)
            
            if 'Contents' in objetos:
                for obj in objetos['Contents']:
                    print(f"      -> Objeto: {obj['Key']} ({obj['Size']} bytes)")
            else:
                print("      -> (Bucket vacío)")
    except Exception as e:
        print(f"Error al obtener buckets: {e}")

if __name__ == "__main__":
    print("=== INICIANDO AUTOMATIZACIÓN CON BOTO3 ===\n")
    aprovisionar_instancia()
    reporte_recursos()
    reporte_s3()
    print("\n=== SCRIPT FINALIZADO ===")