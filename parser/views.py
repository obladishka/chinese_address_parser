from parser.services import parse_address

from rest_framework.response import Response
from rest_framework.views import APIView


class ParserView(APIView):
    def get(self, params):
        address = self.request.query_params.get("address")
        response = parse_address(address)
        return Response(response)
