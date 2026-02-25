# 重新创建数据库表结构
# 功能：删除现有数据库并重新创建所有表

from app.db import Base, engine
from app.job import models as job_models
from app.video import models as video_models
from app.interactions import models as interactions_models
from app.auth import models as auth_models
from app.resume import models as resume_models
from app.company import models as company_models


def recreate_database():
    """
    重新创建数据库函数：
        删除所有表并重新创建
    """
    print("正在删除所有表...")
    Base.metadata.drop_all(bind=engine)
    
    print("正在创建所有表...")
    Base.metadata.create_all(bind=engine)
    
    print("数据库表结构创建完成！")
    
    # 显示所有表
    from sqlalchemy import inspect
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    print(f"\n已创建的表: {len(table_names)} 个")
    for table_name in table_names:
        print(f"  - {table_name}")


if __name__ == "__main__":
    recreate_database()
