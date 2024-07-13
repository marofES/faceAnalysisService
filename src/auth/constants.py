from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    staff = "staff"
    user = "user"
    guest = "guest"
