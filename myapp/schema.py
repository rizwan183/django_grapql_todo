import graphene
from graphene_django import DjangoObjectType
from myapp.models import Todo


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo


class Query(graphene.ObjectType):
    todos = graphene.List(TodoType)

    def resolve_todos(self, info, **kwargs):
        return Todo.objects.all()


class CreateTodo(graphene.Mutation):
    todo = graphene.Field(TodoType)

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)

    def mutate(self, info, title, description):
        todo = Todo(title=title, description=description)
        todo.save()
        return CreateTodo(todo=todo)


class UpdateTodo(graphene.Mutation):
    todo = graphene.Field(TodoType)

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=True)
        description = graphene.String(required=True)

    def mutate(self, info, id, title, description):
        todo = Todo.objects.get(pk=id)
        todo.title = title
        todo.description = description
        todo.save()
        return UpdateTodo(todo=todo)


class DeleteTodo(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        Todo.objects.get(pk=id).delete()
        return DeleteTodo(success=True)


class Mutation(graphene.ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
