from proyeksi.models import Klimatologi, query_data_by_args

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from proyeksi.serializer import KlimatologiSerializer

# Klimatologi Viewset


class KlimatologiViewSet(viewsets.ModelViewSet):
    queryset = Klimatologi.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = KlimatologiSerializer

    def list(self, request):
        queryset = query_data_by_args(**request.query_params)
        serializer = KlimatologiSerializer(queryset['items'], many=True)
        result = {
            'data': serializer.data,
            'draw': queryset['draw'],
            'recordsTotal': queryset['total'],
            'recordsFiltered': queryset['count']
        }
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
