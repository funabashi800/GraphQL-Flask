import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, DepartmentModel, EmployeeModel
from graphql import GraphQLError

class Department(SQLAlchemyObjectType):
  class Meta(object):
    model = DepartmentModel

class Employee(SQLAlchemyObjectType):
  class Meta(object):
    model = EmployeeModel

class createEmployee(graphene.Mutation):
  employee = graphene.Field(Employee)
  
  class Arguments:
    name = graphene.String()
    department_id = graphene.String()

  def mutate(self, info, **kwargs):
    name = kwargs.get('name')
    department_id = kwargs.get('department_id')

    employee = EmployeeModel(name=name, department_id=department_id)
    db_session.add(employee)
    db_session.commit()
    return createEmployee(employee=employee)


class createDepartment(graphene.Mutation):
  department = graphene.Field(Department)
  
  class Arguments:
    name = graphene.String()

  def mutate(self, info, name=None):
    department = DepartmentModel(name=name)
    db_session.add(department)
    db_session.commit()
    return createDepartment(department=department)

class updateEmployee(graphene.Mutation):
  employee = graphene.Field(Employee)

  class Arguments:
    id = graphene.String()
    department_id = graphene.String()
  
  def mutate(self, info, id=None, department_id=None):
    employee = EmployeeModel.query.get(id)
    employee.department_id = department_id
    db_session.commit()
    return updateEmployee(employee=employee)

class deleteEmployee(graphene.Mutation):
  employee = graphene.Field(Employee)

  class Arguments:
    id = graphene.String()

  def mutate(self, info, id=None):
    employee = EmployeeModel.query.get(id)
    db_session.delete(employee)
    db_session.commit()
    return deleteEmployee(employee=employee)


class Query(graphene.ObjectType):
  employees = graphene.List(Employee, limit=graphene.Int())
  departments = graphene.List(Department, limit=graphene.Int())
  employee = graphene.Field(Employee, id=graphene.String())
  employee_by_name = graphene.List(Employee, name=graphene.String())

  def resolve_employees(self, info, limit=None):
   return EmployeeModel.query.all()[:limit]

  def resolve_departments(self, info, limit=None):
    return DepartmentModel.query.all()[:limit]

  def resolve_employee(self, info, id=None):
    return EmployeeModel.query.get(id)

  def resolve_employee_by_name(self, info, name=None):
    #return EmployeeModel.query.filter_by(name=name)
    return EmployeeModel.query.filter(DepartmentModel.name==name)

  

class Mutation(graphene.ObjectType):
  createDepartment = createDepartment.Field()
  createEmployee = createEmployee.Field()
  updateEmployee = updateEmployee.Field()
  deleteEmployee = deleteEmployee.Field()

schema =  graphene.Schema(query=Query, mutation=Mutation)
