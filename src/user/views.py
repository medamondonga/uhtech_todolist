from todolist.generic_crud import list_filter_by_related_field
from .models import User
from .serializers import UserSerializer




EmployeesByDepartement =list_filter_by_related_field(
    model=User,
    serializer=UserSerializer,
    param_name="poste_id",
    field_lookup="poste__departement"
)
