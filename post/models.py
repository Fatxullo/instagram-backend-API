from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from users.models import User
from shared.models import BaseModel





# Post class
class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_images', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic'])])
    caption = models.TextField(validators=[MaxLengthValidator(2000)])
    
    class Meta:
        db_table = 'posts'
        verbose_name = 'post'
        verbose_name_plural = 'posts'
    
    
    def __str__(self):
        return f'{self.author} - post about - {self.caption}'





# Post-Like class
class PostLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    
    class Meta:
        constraints = [             # this for user that user cannot like one post two times
            UniqueConstraint(
                fields=['author', 'post'],
                name='PostLikeUnique'
            )
        ]





#Post-Comment class
class PostComment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child', null=True, blank=True)
    
    def __str__(self):
        return f'{self.author}`s comment -- {self.comment}'




#Comment Like
class CommentLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='likes')
    
    class Meta:
        constraints = [                     # this for user that user cannot like one comment  two times
            UniqueConstraint(
                fields=['author', 'comment'],
                name='CommentLikeUnique'
            )
        ]
    




