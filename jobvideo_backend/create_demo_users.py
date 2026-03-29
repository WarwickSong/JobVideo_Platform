#!/usr/bin/env python3
from sqlalchemy.orm import Session

from app.auth.models import User, UserRole
from app.auth.utils import hash_password
from app.db import engine


DEMO_PASSWORD = "Demo123456"
DEMO_USERS = [
    {
        "username": "demo_seeker",
        "phone": "13800138001",
        "role": UserRole.seeker,
    },
    {
        "username": "demo_employer",
        "phone": "13800138002",
        "role": UserRole.employer,
    },
    {
        "username": "demo_seeker_2",
        "phone": "13800138003",
        "role": UserRole.seeker,
    },
]


def main():
    with Session(engine) as session:
        for item in DEMO_USERS:
            user = session.query(User).filter(User.username == item["username"]).first()
            if user:
                user.phone = item["phone"]
                user.role = item["role"]
                user.password_hash = hash_password(DEMO_PASSWORD)
                print(f"updated {item['username']}")
            else:
                session.add(
                    User(
                        username=item["username"],
                        phone=item["phone"],
                        role=item["role"],
                        password_hash=hash_password(DEMO_PASSWORD),
                    )
                )
                print(f"created {item['username']}")
        session.commit()


if __name__ == "__main__":
    main()
