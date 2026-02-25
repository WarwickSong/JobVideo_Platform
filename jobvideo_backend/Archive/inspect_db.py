# 查看数据库表结构的脚本
# 功能：列出数据库中的所有表及其字段信息

from sqlalchemy import inspect
from app.db import engine, Base
from app.auth.models import User
from app.job.models import JobPost
from app.resume.models import Resume
from app.company.models import Company
from app.video.models import Video
from app.interactions.models import VideoView, VideoLike, VideoFavorite


def inspect_database():
    """
    查看数据库结构函数：
        打印所有表的结构信息
    """
    # 创建检查器
    inspector = inspect(engine)
    
    # 获取所有表名
    table_names = inspector.get_table_names()
    
    print("=" * 80)
    print(f"数据库文件: {engine.url}")
    print(f"表总数: {len(table_names)}")
    print("=" * 80)
    print()
    
    # 遍历每个表
    for table_name in table_names:
        print(f"表名: {table_name}")
        print("-" * 80)
        
        # 获取表的列信息
        columns = inspector.get_columns(table_name)
        print("字段:")
        for column in columns:
            print(f"  - {column['name']}: {column['type']}", end="")
            if column.get('primary_key'):
                print(" (主键)", end="")
            if not column.get('nullable'):
                print(" (非空)", end="")
            print()
        
        # 获取外键信息
        foreign_keys = inspector.get_foreign_keys(table_name)
        if foreign_keys:
            print("外键:")
            for fk in foreign_keys:
                print(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        
        # 获取索引信息
        indexes = inspector.get_indexes(table_name)
        if indexes:
            print("索引:")
            for index in indexes:
                print(f"  - {index['name']}: {index['column_names']}")
        
        print()


if __name__ == "__main__":
    inspect_database()
