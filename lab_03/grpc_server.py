import grpc
from concurrent import futures
import json
import message_service_pb2
import message_service_pb2_grpc

class MessageService(message_service_pb2_grpc.MessageServiceServicer):

    def ProcessMessage(self, request, context):
        text = request.text

        # ===== ЗАДАНИЕ 1: IoT температура =====
        try:
            data = json.loads(text)
            if "temperature" in data:
                temp = float(data["temperature"])
                result = "ALARM" if temp < 18 or temp > 25 else "NORMAL"
                return message_service_pb2.MessageResponse(processed_text=result)
        except:
            pass

        # ===== ЗАДАНИЕ 2: четность =====
        if text.isdigit():
            num = int(text)
            return message_service_pb2.MessageResponse(
                processed_text="EVEN" if num % 2 == 0 else "ODD"
            )

        # ===== ЗАДАНИЕ 3: объединение текста =====
        if "|" in text:
            parts = text.split("|")
            merged = "".join(parts)
            return message_service_pb2.MessageResponse(
                processed_text=merged
            )

        return message_service_pb2.MessageResponse(
            processed_text="UNKNOWN FORMAT"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_service_pb2_grpc.add_MessageServiceServicer_to_server(
        MessageService(), server
    )

    server.add_insecure_port('[::]:50051')
    print("gRPC server started on 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()