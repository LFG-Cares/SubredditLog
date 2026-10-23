from ninja import Field, ModelSchema, Router
from ninja.pagination import PageNumberPagination, paginate

from entries.models import Entry

router = Router()


class EntryOut(ModelSchema):
    moderator: str | None = Field(None, alias='moderator.username')

    class Meta:
        model = Entry
        fields = [
            'id',
            'date',
            'user',
            'rule',
            'action',
            'ban_length',
            'moderator',
            'notes',
        ]


@router.get('', response=list[EntryOut], auth=None)
@paginate(PageNumberPagination, page_size=20)
def list_entries(request):
    return Entry.objects.select_related('moderator')
