import boto3

region = 'us-east-1'
dynamodb = boto3.client('dynamodb', region_name=region)
s3 = boto3.client('s3', region_name=region)

def gestionar_dynamodb():
    table_name = 'STF_Usuarios'
    print("Iniciando DynamoDB")
    try:
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{'AttributeName': 'id_usuario', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id_usuario', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName=table_name)
        print("Tabla creada")

        dynamodb.put_item(
            TableName=table_name,
            Item={
                'id_usuario': {'S': 'USR-001'},
                'nombre': {'S': 'Usuario STF'},
                'rol': {'S': 'DevOps Engineer'}
            }
        )
        print("Registro insertado")

        dynamodb.update_item(
            TableName=table_name,
            Key={'id_usuario': {'S': 'USR-001'}},
            UpdateExpression="SET rol = :r",
            ExpressionAttributeValues={':r': {'S': 'Lead DevOps Engineer'}}
        )
        print("Registro modificado")

        dynamodb.delete_item(
            TableName=table_name,
            Key={'id_usuario': {'S': 'USR-001'}}
        )
        print("Registro eliminado")

    except Exception as e:
        print(f"Aviso en base de datos: {e}")

def gestionar_s3():
    print("\nIniciando S3")
    bucket_name = 'stf-bucket-sdmt-040801' 
    nombre_archivo = 'log_auditoria_stf.txt'
    
    try:
        with open(nombre_archivo, 'w') as f:
            f.write("Registro de auditoria automatizado para Soluciones Tecnologicas del Futuro.")
        
        s3.upload_file(nombre_archivo, bucket_name, f"logs/{nombre_archivo}")
        print(f"Archivo subido a S3: {bucket_name}/logs/")
        
    except Exception as e:
        print(f"Error S3: {e}")

if __name__ == '__main__':
    gestionar_dynamodb()
    gestionar_s3()