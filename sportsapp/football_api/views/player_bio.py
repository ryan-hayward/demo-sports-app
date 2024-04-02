from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import PlayerBio
from ..serializers import PlayerSerializer

@api_view(['GET'])
# standard search
def get_player_bio(request):
    # should be the only param to
    player_id = request.GET.get('player_id')
    # use name and position to find player in database
    print(PlayerBio._meta.fields)
    if player_id == None:
        return Response(status=400)
    # get target data given target model
    tgt_data = PlayerBio.objects.filter(playerid=player_id)
    if tgt_data == None:
        return Response(status=400)
    # format data for return
    print(tgt_data)
    # @TODO change playerbio model draft field to be json
    serializer = PlayerSerializer(tgt_data, many=True)
    return Response(serializer.data)