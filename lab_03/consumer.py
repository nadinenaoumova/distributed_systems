import sys
import os

sys.path.append(os.path.abspath('../grpc_service'))

import pika
import grpc
import message_service_pb2
import message_service_pb2_grpc

def call_grpc(text):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = message_service_pb2_grpc.MessageServiceStub(channel)
        response = stub.ProcessMessage(
            message_service_pb2.MessageRequest(text=text)
        )
        return response.processed_text

def callback(ch, method, properties, body):
    msg = body.decode()
    print("[x] received:", msg)

    result = call_grpc(msg)
    print("[✓] result:", result)

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost', 5672, '/', credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    print("[*] waiting messages...")
    channel.start_consuming()

if __name__ == "__main__":
    main()