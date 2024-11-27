from faker import Faker
import random

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

users = User.objects.all()


class Command(BaseCommand):
    help = "create posts"

    def add_arguments(self, parser):
        parser.add_argument("--post", type=int, default=10, help="number of posts")

    def handle(self, *args, **options):
        num_post = options["post"]
        faker = Faker("ko_KR")

        self.stdout.write(self.style.NOTICE(f"Creating {num_post} posts..."))

        for _ in range(num_post):
            Post.objects.create(
                image="https://search.pstatic.net/sunny/?src=https%3A%2F%2Fvelog.velcdn.com%2Fpost-images%2Fcity7310%2Fad95d5d0-2f83-11e9-acf7-e966133010d9%2Fhello-world.png&type=sc960_832",
                content=faker.sentence(nb_words=random.randint(5, 20)),
                author=random.choice(users),
            )

        self.stdout.write(self.style.SUCCESS("Posts created successfully"))
