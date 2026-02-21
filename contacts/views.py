@api_view(['POST'])
def submit_contact(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        try:
            send_mail(
                subject=f"New contact from {request.data.get('name')}",
                message=f"Name: {request.data.get('name')}\nEmail: {request.data.get('email')}\nMessage: {request.data.get('message')}",
                from_email=None,
                recipient_list=['henok.karvonen@utu.fi'],
            )
        except Exception as e:
            print(f"Email failed: {e}")
        return Response({'message': 'Message received!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)