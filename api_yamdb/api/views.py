from rest_framework import viewsets

from .serializers import ReviewSerializer, CommentSerializer
from reviews.models import Review, Comment
from .permissions import IsOwnerModerAdminOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerModerAdminOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerModerAdminOrReadOnly,)

    def get_queryset(self):
        comment_id = self.kwargs.get("comment_id")
        new_queryset = Comment.objects.filter(id=comment_id)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

