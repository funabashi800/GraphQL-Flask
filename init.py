from models import engine, db_session, Base, DepartmentModel, EmployeeModel

Base.metadata.create_all(bind=engine)

engineering = DepartmentModel(name="Engineering")
db_session.add(engineering)
hr = DepartmentModel(name="Human Resources")
db_session.add(hr)

peter = EmployeeModel(name="Peter", department=engineering)
db_session.add(peter)
roy = EmployeeModel(name="Roy", department=engineering)
db_session.add(roy)
tracy = EmployeeModel(name="Tracy", department=hr)
db_session.add(tracy)
db_session.commit()