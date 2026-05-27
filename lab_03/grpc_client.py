import grpc
import message_service_pb2
import message_service_pb2_grpc

def run():

    with grpc.insecure_channel('localhost:50051') as channel:

        stub = message_service_pb2_grpc.MessageServiceStub(channel)

        text = input("Введите сообщение: ")

        response = stub.ProcessMessage(
            message_service_pb2.MessageRequest(text=text)
        )

        print("Результат:", response.processed_text)

if __name__ == '__main__':
    run()