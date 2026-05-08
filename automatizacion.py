import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')
s3 = boto3.client('s3')
autoscaling = boto3.client('autoscaling', region_name='us-east-1')

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
        return id_instancia
    except Exception as e:
        print(f"Error al crear instancia: {e}")
        return None

def gestionar_autoescalado(id_instancia):
    print("\n2. Configurando Auto Scaling Group...")
    if not id_instancia:
        print("No hay ID de instancia valido para autoescalado.")
        return
    try:
        autoscaling.create_auto_scaling_group(
            AutoScalingGroupName='STF-AutoScalingGroup',
            InstanceId=id_instancia,
            MinSize=1,
            MaxSize=2,
            DesiredCapacity=1
        )
        print("Grupo de autoescalado creado con exito.")
    except Exception as e:
        print(f"Aviso por restricciones de Learner Lab en AutoScaling: {e}")

def reporte_recursos():
    print("\n3. Generando reporte de instancias EC2...")
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
    print("\n4. Listando Buckets S3 y sus objetos...")
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
                print("      -> (Bucket vacio)")
    except Exception as e:
        print(f"Error al obtener buckets: {e}")

if __name__ == "__main__":
    print("=== INICIANDO AUTOMATIZACION CON BOTO3 ===\n")
    id_nueva_instancia = aprovisionar_instancia()
    gestionar_autoescalado(id_nueva_instancia)
    reporte_recursos()
    reporte_s3()
    print("\n=== SCRIPT FINALIZADO ===")
